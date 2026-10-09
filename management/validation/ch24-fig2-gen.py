#!/usr/bin/env python3
"""CH24 图②：aMat 32×16 float 三层布局（ColMajor 块序 + 块内 row-major + elem(1,1) 偏移）。
运行：python3 ch24-fig2-gen.py  # 写 docs/figures/ch24-tile-layout.svg"""
W,H = 620,452
def rect(x,y,w,h,fill,stroke,sw=1,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
def text(x,y,s,size=12,anchor="start",weight="normal",fill="#111"):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}" font-family="sans-serif">{s}</text>'
P=[]
P.append(rect(0,0,W,H,"#ffffff","none"))
P.append(text(16,24,"主例 aMat：32 行 × 16 列 float（容量 2048B）",14,"start","bold"))
# 左：整矩阵 2×2 分块。cell 7px → 112 宽 ×224 高
mx,my,cw,ch=40,56,7,7; MW,MH=16*cw,32*ch
P.append(rect(mx,my,MW,MH,"#f8fafc","#334155",2))
for br in range(2):
    for bc in range(2):
        bx,by=mx+bc*8*cw,my+br*16*ch
        idx=2*bc+br  # ColMajor 块序：(BlockNumRow*BlockCol+BlockRow)
        P.append(rect(bx,by,8*cw,16*ch,"none","#2563eb",2 if idx==0 else 1.2))
        P.append(text(bx+4*cw,by+8*ch+4,f"块#{idx}",12,"middle","bold",("#2563eb" if idx==0 else "#1e40af")))
# 高亮 elem(1,1)：全局 row1,col1
P.append(rect(mx+1*cw,my+1*ch,cw,ch,"#f59e0b","#b45309",1.5))
P.append(text(mx+MW+10,my+14,"块边界：每块 16 行×8 列 float＝512B",11))
P.append(text(mx+MW+10,my+32,"块#编号＝ColMajor 存储序",11,"start","bold","#2563eb"))
P.append(text(mx+MW+10,my+50,"高亮格＝elem(1,1)",11,"start","normal","#b45309"))
# 右：放大块#0，cell 13px → 104×208
zx,zy,cz=368,72,13; ZW,ZH=8*cz,16*cz
P.append(text(zx,zy-14,"块 #0 放大：每行 8 float",12,"start","bold"))
P.append(rect(zx,zy,ZW,ZH,"#eff6ff","#1e40af",1.5))
for r in range(1,16): P.append(f'<line x1="{zx}" y1="{zy+r*cz}" x2="{zx+ZW}" y2="{zy+r*cz}" stroke="#cbd5e1" stroke-width="0.6"/>')
for c in range(1,8):  P.append(f'<line x1="{zx+c*cz}" y1="{zy}" x2="{zx+c*cz}" y2="{zy+ZH}" stroke="#cbd5e1" stroke-width="0.6"/>')
P.append(rect(zx+1*cz,zy+1*cz,cz,cz,"#f59e0b","#b45309",1.5))
P.append(text(40,340,"elem(1,1)：块 (0,0)，块内 (1,1)",11,"start","bold","#b45309"))
P.append(text(40,364,"块内偏移 = 1×8＋1 ＝ 9",11))
P.append(text(40,390,"存储偏移（元素）：块#×128 ＋ 块内行×8 ＋ 块内列",10,fill="#475569"))
# 底注：GM 对照
P.append(text(40,H-26,"GM 侧同元素：按行存放，偏移 = 1×kK＋1 ＝ 17（跨行步长 kK＝16）",12,"start","bold"))
P.append(text(40,H-10,"动态收缩有效区域须 DYNAMIC 模板＋SetValidShape（主例 valid＝全量，未用）",10,fill="#475569"))
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'+" ".join(P)+"</svg>"
open("/home/robertpeng/ascend-book/docs/figures/ch24-tile-layout.svg","w").write(svg)
print("written",len(svg),"bytes")
