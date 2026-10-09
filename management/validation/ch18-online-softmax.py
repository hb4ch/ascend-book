#!/usr/bin/env python3
"""CH18 数学对拍：online softmax 递推 vs 全量参照。
仅数学验证（NumPy 双精度），非 NPU/kernel 验证。
形状按任务书：S1=S2=4, D=2 -> Q/K/V 均为 4x2；KV 分块大小=2（两块）。
对应 CANN 真码：
  - FlashUpdateNew 文档注释: dstTensor = preTensor * expMaxTensor + curTensor
    (attention/common/op_kernel/arch35/vf/vf_flashupdate_new.h L14)
    即未归一化累计 O_partial *= exp(m_old - m_new)；归一化除 l 在输出阶段。
  - m/l 更新: m_new=max(m_old,rowmax); l_new=l_old*exp(m_old-m_new)+rowsum(exp(s-m_new))
"""
import numpy as np
rng = np.random.default_rng(20261009)

S, D, BLK = 4, 2, 2
Q = rng.normal(size=(S, D)).astype(np.float64)
K = rng.normal(size=(S, D)).astype(np.float64)
V = rng.normal(size=(S, D)).astype(np.float64)
scale = 1.0 / np.sqrt(D)

# ---- 参照：全量 softmax(QK^T*scale)V ----
S_full = Q @ K.T * scale
P_full = np.exp(S_full - S_full.max(axis=1, keepdims=True))
P_full /= P_full.sum(axis=1, keepdims=True)
O_ref = P_full @ V

# ---- online 递推：KV 按 BLK 分块（未归一化累计 + 末块归一化）----
O_acc = np.zeros((S, D)); m_prev = np.full(S, -np.inf); l_prev = np.zeros(S)
trace = []
for t in range(0, S, BLK):
    S_blk = Q @ K[t:t+BLK].T * scale                 # 本块分数 (S,blk)
    m_blk = S_blk.max(axis=1)                        # rowmax
    m_new = np.maximum(m_prev, m_blk)                # ① m 更新
    P_blk = np.exp(S_blk - m_new[:, None])           # 本块 exp（按新 max）
    corr  = np.exp(m_prev - m_new)                   # expMaxTensor：旧累计 correction
    l_new = l_prev * corr + P_blk.sum(axis=1)        # ② l 更新（未归一化和）
    O_new = O_acc * corr[:, None] + P_blk @ V[t:t+BLK]  # ③ O 重缩放累计 == FlashUpdateNew
    trace.append((t, m_prev.copy(), m_new.copy(), corr.copy(), l_prev.copy(), l_new.copy()))
    m_prev, l_prev, O_acc = m_new, l_new, O_new

O_online = O_acc / l_prev[:, None]                   # 末块归一化（除 l）

# ---- 对角 ----
dO = np.abs(O_ref - O_online).max()
dP = np.abs(P_full - (np.exp(S_full - m_prev[:, None]) / l_prev[:, None])).max()
print(f"shape S={S} D={D} blk={BLK}  seed=20261009")
print(f"max|O_ref - O_online| = {dO:.3e}")
print(f"max|P_ref - P_online| = {dP:.3e}")
assert dO < 1e-12 and dP < 1e-12, "online != full"
# ---- 逐步迹（供正文引用）----
for t, mo, mn, corr, lo, ln in trace:
    print("blk s2=[%d,%d)  m:%s->%s  corr:%s  l:%s->%s" % (t,t+BLK,np.round(mo,4),np.round(mn,4),np.round(corr,4),np.round(lo,4),np.round(ln,4)))
np.set_printoptions(precision=6, suppress=True)
print("Q=\n", Q); print("K=\n", K); print("V=\n", V)
print("O_ref=\n", O_ref); print("O_online=\n", O_online)
print("P_online=\n", (np.exp(S_full - m_prev[:, None]) / l_prev[:, None]))
print("PASS: online recurrence == full softmax (fp64, tol 1e-12)")
