#!/usr/bin/env python3
"""CH20 R1 数学核验 v2：地址落点（物理bank+group）/UB覆盖/H144,128全列/L2与混编复算。
纯地址与算术；不预测周期。拓扑据 nd2nz README（A2 48bank/16g L123、950 16bank/8g L299区）。"""
import math
from fractions import Fraction

def bank_of(db, banks, base_db=0): return (base_db + db) % banks
def group_of(db, banks, groups, base_db=0): return bank_of(db, banks, base_db) % groups

def spread(stride, banks, groups, base_db=0, cols=8):
    return [(bank_of(i*stride, banks, base_db), group_of(i*stride, banks, groups, base_db)) for i in range(cols)]

print('== 1) 落点：物理bank与group并列（idx0..7） ==')
for name, banks, groups in (('A2',48,16),('950',16,8)):
    for stride in (144,145):
        s=spread(stride,banks,groups)
        print(f'{name} stride={stride}: banks={[b for b,_ in s]} groups={[g for _,g in s]} -> {len(set(g for _,g in s))}组')
s=spread(145,16,8,base_db=8)
print(f'950 stride145 baseDb=+8db(bank8起步): banks={[b for b,_ in s]} groups={[g for _,g in s]} -> {len(set(g for _,g in s))}组')
# C0Cols 扩展检查（R1-4）：cols=16
for name,banks,groups in (('A2',48,16),('950',16,8)):
    for stride in (144,145):
        g={g for _,g in spread(stride,banks,groups,cols=16)}
        print(f'cols=16 {name} stride={stride}: {len(g)}组 {sorted(g)}')

print('== 2) gcd 判定 ==')
for a,b in ((144,16),(145,16),(144,8),(145,8)): print(f'gcd({a},{b})={math.gcd(a,b)}',end='  ')
print()

print('== 3) UB 覆盖（整块+尾块全列） ==')
tileH,tileW,totalM,C0,COLS=144,128,8192,16,8
nT=math.ceil(totalM/tileH); lastH=totalM-(nT-1)*tileH
assert (nT,lastH)==(57,128) and totalM%C0==0
for stride,alloc in ((144,1152),(145,1160)):
    for H in (144,128):
        need=(COLS-1)*stride+H
        tag='整块' if H==144 else '尾块'
        assert need<=alloc,(stride,H,need)
        print(f'stride{stride} {tag}H={H}: need={need}<=alloc{alloc} ok; MTE3 srcStride={stride-H}')
assert 56*144+128==totalM; print('GM末端 56*144+128==8192 ok')

print('== 4) L2 命中率复算（data_copy README 数字） ==')
a2=(212+217)/(212+217+4718595+4718592)
print(f'A2场景5=(212+217)/(429+4718595+4718592)={a2:.6%}={a2*1000:.4f}‰（表载0.005%）')
h,m,v=31346,8358412,529720
print(f'950场景5=hit/(hit+miss+victim)={h}/{h}+{m}+{v}={h/(h+m+v):.4%}（表载0.35%）')
h2,m2,v2=5943026,2446732,528797
print(f'950场景6={h2/(h2+m2+v2):.4%}（表载66.64%）')
print(f'0.005%->75%倍数={75/0.005:.0f}倍=log10={math.log10(75/0.005):.2f}数量级')
print(f'A2 L2场景Task 828.06->365.74: {(365.74-828.06)/828.06:.2%}')

print('== 5) 混编百分比复算（FloorMod） ==')
print(f'Task 538.098->463.179: {(463.179-538.098)/538.098:.2%}')
print(f'vec 501.605->301.474: {(301.474-501.605)/501.605:.2%}')
print(f'mte2 527.987->437.055: {(437.055-527.987)/527.987:.2%}；case1 mte2=217.341')
print('结论：地址/占比复算；不预测周期。')