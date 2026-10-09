# -*- coding: utf-8 -*-
"""CH27 独立 CPU 数学参考冒烟：sparse_flash_attention（SFA）golden，CPU-only。

非 NPU 验证：本脚本只运行仓内 CPU golden（tests/pytest/sparse_flash_attention_golden.py
的 generate_input_tensors + compute_cpu），验证数学参考可在纯 CPU 路径执行并给出统计；
不调用 torch_npu、不编译、不运行任何设备代码。

数据来源：ops-transformer/sparse_flash_attention tests/pytest 参数集第 0 组
（sfa_bsnd_basic，BSND，B=1 S1=5 S2=262144 N1=8 N2=1 D=512，fp16）。
按 utils.convert_param_combination_to_cs_format 的 BSND 分支手工展开
（utils.py 依赖 pytest/torch_npu，本机不可导入，故不复用其函数；展开字段逐一对照源码）。
"""
import sys
sys.dont_write_bytecode = True  # 源仓只读：不落 pyc
import time, json
sys.path.insert(0, '/mnt/SATASSDEXT4/cann/ops-transformer/attention/sparse_flash_attention/tests/pytest')
import torch
import sparse_flash_attention_golden as G
import sparse_flash_attention_paramset as P

comb = P.ENABLED_PARAMS[0]
P1 = {k: (v[0] if isinstance(v, list) else v) for k, v in comb.items()}
K = P1['K']; sbs = P1['sparse_block_size']
assert P1['layout_kv'] == 'BSND'
shape_input = {
    "query": [P1['B'], P1['S1'], P1['N1'], P1['D']],
    "key": [P1['B'], P1['S2'], P1['N2'], P1['D']],
    "value": [P1['B'], P1['S2'], P1['N2'], P1['D']],
    "sparse_indices": [P1['B'], P1['S1'], P1['N2'], int(K / sbs)],
    "block_table": [P1['B']],
    "query_cache": [P1['B'], P1['S1'], P1['N1'], P1['D'] + P1['rope_head_dim']],
    "key_cache": [P1['B'], P1['S2'], P1['N2'], P1['D'] + P1['rope_head_dim']],
    "value_cache": [P1['B'], P1['S2'], P1['N2'], P1['D'] + P1['rope_head_dim']],
    "query_rope": [P1['B'], P1['S1'], P1['N1'], P1['rope_head_dim']],
    "key_rope": [P1['B'], P1['S2'], P1['N2'], P1['rope_head_dim']],
    "sinks": [P1['N1']],
}
dtype_input = {"query": "fp16", "key": "fp16", "value": "fp16", "sparse_indices": "int32",
               "block_table": "int32", "query_rope": "fp16", "key_rope": "fp16", "sinks": "fp32"}
params = {
    "case_name": P1['Testcase_Prefix'],
    "layout_query": P1['layout_query'], "layout_kv": P1['layout_kv'],
    "actualseqlengths": P1['actual_seq_q'][0] if isinstance(P1['actual_seq_q'][0], list) else P1['actual_seq_q'],
    "actualseqlengthskv": P1['actual_seq_kv'][0] if isinstance(P1['actual_seq_kv'][0], list) else P1['actual_seq_kv'],
    "scalevalue": P1['scale_value'], "sparsemode": P1['sparse_mode'],
    "sparse_blocksize": sbs, "shape_input": shape_input, "dtype_input": dtype_input,
    "range_input": {"query": [-10.0, 100.0], "key": [5.0, 100.0], "sparse_indices": [-10, 10],
                    "block_table": [0, 1], "query_rope": [-10.0, 10.0], "key_rope": [-10.0, 10.0]},
    "shape_output": {"attn_out": [P1['B'], P1['S1'], P1['N1'], P1['D']],
                     "softmax_max": [P1['B'], P1['N2'], P1['S1'], int(P1['N1'] / P1['N2'])],
                     "softmax_sum": [P1['B'], P1['N2'], P1['S1'], int(P1['N1'] / P1['N2'])]},
    "dtype_output": ["fp16"], "rope_head_dim": P1['rope_head_dim'],
    "attention_mode": P1['attention_mode'], "return_softmax_lse": P1['return_softmax_lse'],
    "use_sinks": False, "block_size": P1.get('block_size', 256),
}
print('case:', params['case_name'], 'layout', params['layout_query'], 'B', P1['B'], 'S1', P1['S1'],
      'S2', P1['S2'], 'N1', P1['N1'], 'N2', P1['N2'], 'D', P1['D'], 'K', K, flush=True)
t0 = time.time()
inp = G.generate_input_tensors(params)
print('generate_input_tensors OK %.1fs' % (time.time() - t0), flush=True)
t0 = time.time()
out, _, _ = G.compute_cpu(inp, params)
dt = time.time() - t0
print('compute_cpu OK %.1fs' % dt, flush=True)
# compute_golden 返回 (attn_out, shape)；0 号即注意力输出
attn = out[0] if isinstance(out, tuple) else out
assert torch.is_tensor(attn), type(attn)
f = attn.float()
print('attn_out: shape=%s dtype=%s mean=%.6f std=%.6f nan=%s' % (
    tuple(attn.shape), attn.dtype, f.mean(), f.std(), bool(torch.isnan(f).any())), flush=True)
print('CPU golden smoke done (NOT an NPU verification).', flush=True)
