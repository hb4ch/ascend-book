#!/usr/bin/env python3
"""CH24 图②/正文偏移复算：主例 aMat 布局（显式 ColMajor 块 + RowMajor 块内，512B 分形）。

对应 pto-isa/include/pto/common/pto_tile.hpp `GetTileOffset` 的 is_Nz_layout 分支
（!RowMajor块 && boxed && InnerRowMajor）。几何：32×16 float，块 16×8 float=512B，2×2 块。
运行：python3 ch24-tile-offset-compute.py
"""
T = 4  # sizeof(float)
InnerRows, InnerCols = 16, 32 // T      # boxed+InnerRowMajor: fixedRowSize=16, alignedSize/sizeof=8
assert InnerRows * InnerCols * T == 512  # 每块 512B
Rows, Cols = 32, 16                      # aMat = Tile<Mat,float,32,16,ColMajor,valid 32×16,RowMajor,512>
BlockRows, BlockCols = Rows // InnerRows, Cols // InnerCols

def off(r, c):
    br, bc, ir, ic = r // InnerRows, c // InnerCols, r % InnerRows, c % InnerCols
    return (BlockRows * bc + br) * InnerRows * InnerCols + ir * InnerCols + ic

if __name__ == "__main__":
    print(f"inner block: {InnerRows}x{InnerCols} float = {InnerRows*InnerCols*T} bytes")
    print(f"blocks: {BlockRows}x{BlockCols}; capacity {Rows}x{Cols} float = {Rows*Cols*T} bytes")
    for (r, c) in [(0, 0), (0, 1), (1, 0), (1, 1), (31, 15)]:
        print(f"elem({r:2d},{c:2d}) -> storage offset {off(r,c):4d} (float), byte {off(r,c)*T:5d}")
    kK = 16
    print(f"GM row-major elem(1,1) offset: {1*kK+1} (stride kK,1)")
