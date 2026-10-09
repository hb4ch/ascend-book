#!/usr/bin/env python3
"""CH19 离线复算：仅用仓内 README 数字。口径=add_high_performance 总表。
读带宽 BW_read=D_read/T_mte2（case0-3）；混合 BW=(2读+1写)/T_mte2（case4-6）。README L519-523。"""
D = 8192*8192*2  # bytes/tensor (half)
A2 = {2:(306.58,215.485,'read'),3:(268.5,184.369,'read'),
      4:(264.02,250.528,'mix'),5:(187.68,175.997,'mix'),6:(184.52,171.611,'mix')}
REF = {2:1.2457,3:1.4560,4:1.6072,5:2.2755,6:2.3456}
print('== A2 复算 vs 总表 ==')
for c,(task,mte,mode) in A2.items():
    bw=(2 if mode=='read' else 3)*D/(mte*1e-6)/1e12
    print(f'case{c} {mode}: calc={bw:.4f} table={REF[c]} diff={bw-REF[c]:+.4f}')
print('== 有效吞吐(3D/TaskDur,另一口径,非带宽实测) ==')
for c,task in [(4,264.02),(5,187.68),(6,184.52)]:
    print(f'  case{c}: {3*D/(task*1e-6)/1e12:.3f} TB/s')
print('== 百分比/倍数 ==')
print('0->1 Task降: %.2f%% (源表179.4x)'%((1-6909.6/1239689.1)*100))
print('1->2: %.4f%% (源表95.5为近似表达)'%((1-306.58/6909.6)*100))
print('case0->6: %.2fx (源表6718.5x)'%(1239689.1/184.52))
print('case0 scalar实现/向量理论: %.1fx'%(1233742.494/283.405))
print('== 理论vector ==')
print('A2: %.3fus  950: %.3fus'%(8192*8192/(128*1.85e9*48)*1e6,8192*8192/(128*1.65e9*64)*1e6))
print('== 均值算例(48核:47x5+1x50) ==')
print('mean = %.4f us'%((47*5+1*50)/48))
print('case4 ratio和: %.3f'%(0.973+0.33+0.05+0.011))
