# -*- coding: utf-8 -*-
"""CH27 独立数学对拍：SFA golden(CPU) vs 本书独立 numpy 参考实现。

场景（缩小版主例条件，全部显式）：
  layout TND/TND、q/k fp16、sparse_mode=0（threshold=act_kv）、attention_mode=2、
  sparse_block_size=1、B=1、act_q=[3]/T1=3、act_kv=[10]/T2=16(pad)、N1=4、N2=1(g=4)、
  D=512、rope=64（同主例 D；golden 隐含 D=512，见下）、K=8、scale=0.25（固定值，本书声明）。

golden 语义要点（本书逐行核实 sparse_flash_attention_golden.py 后在参考实现中复刻）：
  (1) preprocessing 把 q_rope/k_rope 沿 D 维 concat 进 Q/K（L58-100 区段）→ 点积维=D+rope=576；
  (2) _t_increattention_bnsd L688：v_bnsd = k_bnsd[..., :512] —— v 输入在该路径被 k 截断顶替，
      隐含 D=512 假设（D≠512 时 out shape 与 bmm2 结果不一致，本书实测）；
  (3) sparse_indices 由 golden 用未固定种子的 randperm 重新生成并覆盖输入（本书 seed 后从
      返回 dict 读回实际生效索引供参考实现使用)；
  (4) mode0：threshold=act_kv；索引块裁剪到 [begin, min(end,act)]，遇 -1 终止；
  (5) softmax 带最大值平移；bmm2 前 softmax cast fp16（本书参考全程 fp64，差异源，宽容差)。
非 NPU 验证；rope 不另作位置编码，仅 concat（golden 即如此）。
"""
import sys
sys.dont_write_bytecode = True  # 源仓只读：不落 pyc
import math
import numpy as np
import torch
sys.path.insert(0, '/mnt/SATASSDEXT4/cann/ops-transformer/attention/sparse_flash_attention/tests/pytest')
import sparse_flash_attention_golden as G

SEED = 20261010
np.random.seed(SEED)
torch.manual_seed(SEED)

# ---- 场景常量 ----
T1, T2 = 3, 16
ACT_Q, ACT_KV = [3], [10]
N1, N2, D, R, K = 4, 1, 512, 64, 8
BS, SCALE = 1, 0.25
g = N1 // N2
assert N1 % N2 == 0

def r(*shape):
    return torch.from_numpy(np.random.uniform(-1.0, 1.0, shape).astype(np.float16))

input_tensor_dict = {
    "query": r(T1, N1, D), "key": r(T2, N2, D), "value": r(T2, N2, D),
    "sparse_indices": torch.full((T1, N2, K), -1, dtype=torch.int32),  # 会被 golden 重生成
    "block_table": torch.zeros(1, dtype=torch.int32),
    "query_rope": r(T1, N1, R), "key_rope": r(T2, N2, R),
    "sinks": None, "scale_value": SCALE, "sparse_block_size": BS,
    "layout_query": "TND", "layout_kv": "TND", "sparse_mode": 0,
}
params = {
    "case_name": "ch27_tnd_refcheck", "layout_query": "TND", "layout_kv": "TND",
    "actualseqlengths": ACT_Q, "actualseqlengthskv": ACT_KV,
    "scalevalue": SCALE, "sparsemode": 0, "sparse_blocksize": BS,
    "shape_input": {"query": [T1, N1, D], "key": [T2, N2, D], "value": [T2, N2, D],
                    "sparse_indices": [T1, N2, K], "block_table": [1],
                    "query_rope": [T1, N1, R], "key_rope": [T2, N2, R], "sinks": [N1]},
    "dtype_input": {"query": "fp16", "key": "fp16", "value": "fp16", "sparse_indices": "int32",
                    "block_table": "int32", "query_rope": "fp16", "key_rope": "fp16", "sinks": "fp32"},
    "range_input": {"query": [-1.0, 1.0], "key": [-1.0, 1.0], "sparse_indices": [-1, K - 1],
                    "block_table": [0, 0], "query_rope": [-1.0, 1.0], "key_rope": [-1.0, 1.0]},
    "shape_output": {"attn_out": [T1, N1, D], "softmax_max": [N2, T1, g], "softmax_sum": [N2, T1, g]},
    "dtype_output": ["fp16"], "rope_head_dim": R, "attention_mode": 2,
    "return_softmax_lse": False, "use_sinks": False, "block_size": 256,
}

out, input_dict_back, _ = G.compute_cpu(input_tensor_dict, params)
assert out is not None, 'golden failed'
golden_y = out[0].float().numpy()            # (T1, N1, D)（B=1）
eff_idx = input_dict_back["sparse_indices"].numpy()  # golden 重生成后的实际索引 (T1,N2,K)
print('golden attn_out', golden_y.shape, 'finite', bool(np.isfinite(golden_y).all()))

# ---- 独立 numpy 参考（不 import golden 的任何计算函数；规则见文件头）----
DT = D + R
q = torch.cat([input_dict_back['query'], input_dict_back['query_rope']], -1).numpy().astype(np.float64)
kk = torch.cat([input_dict_back['key'], input_dict_back['key_rope']], -1).numpy().astype(np.float64)
vv = kk[..., :D]  # golden L688 同款规则：v := k 截断前 D 列
act = ACT_KV[0]
ref = np.zeros((T1, N1, D))
for s1 in range(T1):
    sel = []
    for i in range(min(K, math.ceil(act / BS))):
        idx = int(eff_idx[s1, 0, i])
        if idx == -1:
            break
        b0, b1 = idx * BS, min((idx + 1) * BS, act)
        if b0 >= act:
            continue
        sel.extend(range(b0, b1))
    assert sel, f'empty selection at s1={s1}'
    logits = q[s1] @ kk[sel, 0, :].T * SCALE                # (N1, S) 点积维 D+rope
    logits -= logits.max(axis=1, keepdims=True)
    p = np.exp(logits); p /= p.sum(axis=1, keepdims=True)
    ref[s1] = p @ vv[sel, 0, :]

# ---- 断言与差异报告 ----
assert golden_y.shape == (T1, N1, D) == ref.shape
assert np.isfinite(golden_y).all() and np.isfinite(ref).all()
diff = np.abs(golden_y - ref)
rel = diff / (np.abs(ref) + 1e-12)
print('max abs diff %.3e; mean abs %.3e; max rel %.3e' % (diff.max(), diff.mean(), rel.max()))
print('std golden %.4f / ref %.4f' % (golden_y.std(), ref.std()))
# 阈值依据（可解释）：输出元素为 v 的凸组合且 |v|<=1，故 |out|<=1；主要舍入源是
# golden 在 bmm2 前把 softmax 概率 cast fp16（单个权重相对误差 ~2^-11≈4.9e-4），
# 叠加两侧 fp32 累加次序差；取 2e-3 为宽容上界。本输入实测见上，不外推所有输入。
TOL = 2e-3
assert diff.max() < TOL, 'exceed tolerance %g' % TOL
print('PASS: this input max abs %.3e < tol %.1e; seed %d' % (diff.max(), TOL, SEED))
print('NOT an NPU verification. golden regenerated sparse_indices (unseeded randperm; global seed set here)')
print('and replaces v by k[...,:512] (D=512 assumption) -- both documented in CH27-EVIDENCE.')
# 覆盖如实声明：本输入实触达/未触达的参考分支
print('coverage: index-subset YES; -1 terminator NOT exercised (regen indices fill all K=%d slots, no -1);' % K)
print('coverage: out-of-range clip NOT exercised (max idx %d < act %d); empty-selection NOT exercised (sel nonempty)' % (K - 1, ACT_KV[0]))
