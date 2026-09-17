#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ascend A5 (950/3510) vs A3 (910C/2201) 网络通信对比 PPT 生成器
- 原生可编辑 .pptx（python-pptx），全部用形状绘制，无位图
- 第1页：总览对比（左 A3 / 右 A5）
- 第2页：四大差异详览（逐行左右对照）
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------- 主题色 ----------
BG      = RGBColor(0x0F, 0x14, 0x1C)   # 深底
CARD_A3 = RGBColor(0x17, 0x2A, 0x3A)   # A3 卡片浅蓝
CARD_A5 = RGBColor(0x1B, 0x25, 0x33)   # A5 卡片浅灰蓝
ACC_A3  = RGBColor(0x4F, 0x9D, 0xE0)   # A3 强调蓝
ACC_A5  = RGBColor(0xE8, 0xA0, 0x3C)   # A5 强调橙
TXT     = RGBColor(0xE6, 0xEC, 0xF3)
SUB     = RGBColor(0x9F, 0xB0, 0xC2)
LINE    = RGBColor(0x35, 0x48, 0x5C)
GREEN   = RGBColor(0x6F, 0xC7, 0x8F)
RED     = RGBColor(0xE0, 0x6A, 0x6A)

FONT = "Microsoft YaHei"

SW, SH = Inches(13.333), Inches(7.5)

prs = Presentation()
prs.slide_width, prs.slide_height = SW, SH


def set_bg(slide, color=BG):
    r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    r.fill.solid(); r.fill.fore_color.rgb = color
    r.line.fill.background()
    r.shadow.inherit = False
    return r


def txt(shape, text, size=12, color=TXT, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.color.rgb = color; r.font.bold = bold
    r.font.name = FONT
    return shape


def box(slide, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.10):
    sp = slide.shapes.add_shape(shape, x, y, w, h)
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(1)
    sp.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            sp.adjustments[0] = radius
        except Exception:
            pass
    return sp


def label(slide, x, y, w, text, size=12, color=TXT, bold=False, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(x, y, w, Inches(0.4))
    return txt(tb, text, size=size, color=color, bold=bold, align=align)


def multi_txt(shape, lines):
    """lines: list of (text, size, color, bold)"""
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    for i, (t, s, c, b) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run(); r.text = t
        r.font.size = Pt(s); r.font.color.rgb = c; r.font.bold = b
        r.font.name = FONT
    return shape


def connect(slide, x1, y1, x2, y2, color=LINE, width=1.0, dash=False, arrow=False):
    conn = slide.shapes.add_connector(1, x1, y1, x2, y2)  # 1 = STRAIGHT
    conn.line.color.rgb = color
    conn.line.width = Pt(width)
    if dash:
        conn.line.dash_style = 2  # DASH
    if arrow:
        # 给结尾加箭头
        ln = conn.line._get_or_add_ln()
        he = ln.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'med', 'len': 'med'})
        ln.append(he)
    return conn


# ================= 通用：一侧面板 =================
def side_panel(slide, x, w, acc, chip, tagline):
    """返回 dict 存基准坐标"""
    y = Inches(1.15)
    hdr = box(slide, x, y, w, Inches(0.62), fill=acc, radius=0.15)
    txt(hdr, chip, size=17, color=BG, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tag = label(slide, x, y + Inches(0.68), w, tagline, size=11, color=SUB, align=PP_ALIGN.CENTER)
    return {"x": x, "w": w, "acc": acc, "hdr_y": y, "y": y + Inches(1.15)}


# ================= 第1页：总览对比 =================
s1 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s1)

# 标题
t = box(s1, Inches(0), Inches(0.12), SW, Inches(0.9), fill=None)
multi_txt(t, [
    ("A5 vs A3 · 网络通信能力对比", 25, RGBColor(0xFF, 0xFF, 0xFF), True),
    ("Ascend 950 (NPU arch 3510)  vs  Ascend 910C (arch 2201)  ·  灵衢 UnifiedBus 2.0 带来「面向超节点的内存语义通信」", 11, SUB, False),
])

LX, LW = Inches(0.35), Inches(6.25)
RX, RW = Inches(6.75), Inches(6.25)
TOP = Inches(1.18)

P = side_panel(s1, LX, LW, ACC_A3, "Ascend A3 · 910C", "scale-up 由 HCCS 承载 · scale-out 走 RoCE · 消息式集合通信")
Q = side_panel(s1, RX, RW, ACC_A5, "Ascend A5 · 950", "灵衢 UnifiedBus(UB) 2.0 全光直连 · URMA 单边 + Load/Store 内存语义")

def kpi_tiles(slide, x, w, y, items, acc):
    """items: list of (value, unit_label)"""
    n = len(items)
    gap = Inches(0.12)
    tw = (w - gap * (n - 1)) / n
    for i, (v, l) in enumerate(items):
        tx = x + i * (tw + gap)
        tile = box(slide, tx, y, tw, Inches(0.92), fill=CARD_A3 if acc == ACC_A3 else CARD_A5, line=acc, radius=0.12)
        multi_txt(tile, [
            (v, 20, acc, True),
            (l, 9, SUB, False),
        ])
    return y + Inches(1.05)

# A3 KPI
kpi_tiles(s1, LX, LW, P["y"], [
    ("784 GB/s", "HCCS 聚合互联带宽"),
    ("微秒级", "单跳链路时延"),
    ("384", "CloudMatrix 集群 (NPU)"),
], ACC_A3)
# A5 KPI
kpi_tiles(s1, RX, RW, Q["y"], [
    ("2 TB/s", "互联带宽 ≈ 2.5× 910C"),
    ("200 ns", "单跳时延 ≈ 降低 10×"),
    ("8192", "Atlas 950 超节点 (NPU)"),
], ACC_A5)

# 拓扑示意图区域：用清晰的垂直分带（标题带 / 图形带 / 说明带），避免文字重叠
def draw_topology(slide, x, y, w, h, acc, mode):
    """mode: 'a3'=HCCS+RoCE; 'a5'=UB-Mesh 超节点"""
    panel = box(slide, x, y, w, h, fill=RGBColor(0x12, 0x1A, 0x24), line=LINE, radius=0.08)
    label(slide, x + Inches(0.14), y + Inches(0.05), w - Inches(0.28), "互 联 拓 扑", size=11, color=acc, bold=True)
    cx = x + w / 2
    # 图形带：y+0.38 .. y+1.50 ；说明带：y+1.58
    if mode == "a3":
        # 顶部：一行 4 个 NPU（HCCS 板内环）+ 下方 1 个 RoCE 交换机
        chip_w = Inches(1.02); chip_h = Inches(0.42); n = 4; gap = Inches(0.20)
        total = chip_w * n + gap * (n - 1)
        startx = cx - total / 2
        top_y = y + Inches(0.40)
        chips = []
        for i in range(n):
            px = startx + i * (chip_w + gap)
            c = box(slide, px, top_y, chip_w, chip_h, fill=CARD_A3, line=acc, radius=0.15)
            label(slide, px, top_y + Inches(0.11), chip_w, f"NPU {i}", size=10, color=TXT, bold=True, align=PP_ALIGN.CENTER)
            chips.append((px + chip_w / 2, top_y + chip_h / 2))
        # HCCS 环
        for i in range(n):
            connect(slide, chips[i][0], chips[i][1], chips[(i + 1) % n][0], chips[(i + 1) % n][1], color=acc, width=1.4)
        label(slide, x + Inches(0.14), top_y + Inches(0.44), w * 0.5, "HCCS 板内直连 (~784 GB/s)", size=9, color=acc, bold=True)
        # 交换机（居中下带）
        sw_w = Inches(1.5); sw_h = Inches(0.44)
        sw = box(slide, cx - sw_w / 2, y + Inches(1.20), sw_w, sw_h, fill=RGBColor(0x1A, 0x24, 0x30), line=acc, radius=0.15)
        label(slide, cx - sw_w / 2, y + Inches(1.27), sw_w, "RoCE 交换机", size=10, color=TXT, align=PP_ALIGN.CENTER)
        connect(slide, chips[0][0], chips[0][1], cx, y + Inches(1.20), color=RGBColor(0x6F, 0x7A, 0x86), width=1.0, dash=True, arrow=True)
        connect(slide, chips[2][0], chips[2][1], cx, y + Inches(1.20), color=RGBColor(0x6F, 0x7A, 0x86), width=1.0, dash=True, arrow=True)
        label(slide, x + Inches(0.14), y + h - Inches(0.42), w - Inches(0.28),
              "RoCEv2 (100G×2) scale-out · 跨机箱需交换机，多跳", size=9, color=SUB)
    else:
        # 顶部：一行 5 个 NPU（UB-Mesh）+ 下方 1 个域内共享内存池（URMA 单边读写）
        slot_w = Inches(0.86); slot_h = Inches(0.40); n = 5; gap = Inches(0.14)
        total = slot_w * n + gap * (n - 1)
        startx = cx - total / 2
        top_y = y + Inches(0.40)
        chips = []
        for i in range(n):
            px = startx + i * (slot_w + gap)
            c = box(slide, px, top_y, slot_w, slot_h, fill=CARD_A5, line=acc, radius=0.15)
            label(slide, px, top_y + Inches(0.10), slot_w, f"NPU {i}", size=9, color=TXT, bold=True, align=PP_ALIGN.CENTER)
            chips.append((px + slot_w / 2, top_y + slot_h / 2))
        # UB-Mesh 直连环
        for i in range(n - 1):
            connect(slide, chips[i][0], chips[i][1], chips[i + 1][0], chips[i + 1][1], color=acc, width=1.4)
        connect(slide, chips[0][0], chips[0][1], chips[2][0], chips[2][1], color=acc, width=1.0)
        connect(slide, chips[2][0], chips[2][1], chips[-1][0], chips[-1][1], color=acc, width=1.0)
        # 域内共享内存池（统一编址远端 HBM）
        pool_w = Inches(2.9); pool_h = Inches(0.46)
        pool = box(slide, cx - pool_w / 2, y + Inches(1.18), pool_w, pool_h, fill=CARD_A5, line=GREEN, radius=0.15)
        label(slide, cx - pool_w / 2, y + Inches(1.25), pool_w, "域内统一编址内存池（远端 HBM）", size=9, color=GREEN, bold=True, align=PP_ALIGN.CENTER)
        connect(slide, chips[0][0], chips[0][1], cx - Inches(0.7), y + Inches(1.18), color=GREEN, width=1.4, arrow=True)
        connect(slide, chips[-1][0], chips[-1][1], cx + Inches(0.7), y + Inches(1.18), color=GREEN, width=1.4, arrow=True)
        label(slide, x + Inches(0.14), y + h - Inches(0.42), w - Inches(0.28),
              "UB-Mesh 递归直连 · 单柜 64 卡 → 8192 卡超节点 · URMA 单边读写远端内存", size=9, color=SUB)

draw_topology(s1, LX, P["y"] + Inches(1.02), LW, Inches(2.15), ACC_A3, "a3")
draw_topology(s1, RX, Q["y"] + Inches(1.02), RW, Inches(2.15), ACC_A5, "a5")

# 底部一句话
b1 = box(s1, LX, Inches(5.92), LW, Inches(0.72), fill=RGBColor(0x14, 0x20, 0x2C), line=ACC_A3, radius=0.10)
multi_txt(b1, [
    ("定位：以「算」为核心", 12, ACC_A3, True),
    ("跨节点依赖交换机 + 消息式通信；KV/权重需多跳或回 CPU 内存", 10, SUB, False),
])
b2 = box(s1, RX, Inches(5.92), RW, Inches(0.72), fill=RGBColor(0x18, 0x20, 0x2A), line=ACC_A5, radius=0.10)
multi_txt(b2, [
    ("定位：以「域」为核心（类比：超节点 ≈ 一台大机器）", 12, ACC_A5, True),
    ("互联即内存：URMA 单边 + 统一编址，直接读写远端 HBM", 10, SUB, False),
])

# 来源脚注
label(s1, Inches(0.35), Inches(6.82), Inches(12.6),
      "口径来源：华为官方超节点/灵衢 2.0 白皮书、Hot Chips 2025 UB-Mesh、CANN 面向 950 架构详解；本图为本 side-quest 科普对比，非 ASCEND 书源码结论，数字为公开口径。",
      size=8.5, color=RGBColor(0x6C, 0x7A, 0x88))


# ================= 第2页：四大差异详览 =================
s2 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s2)

t = box(s2, Inches(0), Inches(0.10), SW, Inches(0.86), fill=None)
multi_txt(t, [
    ("A5 vs A3 · 网络通信四大差异", 24, RGBColor(0xFF, 0xFF, 0xFF), True),
    ("世界变了：从「板内小互联」到「超节点大互联」——通信从消息式走向单边内存语义", 11, SUB, False),
])

# 表头
hcol = Inches(0.35); hw = Inches(2.35)
ax = Inches(2.85); aw = Inches(4.65)
bx = Inches(7.65); bw = Inches(5.3)
# 列头
label(s2, hcol, Inches(1.05), hw, "差异维度", size=12, color=SUB, bold=True)
hdr_a3 = box(s2, ax, Inches(0.98), aw, Inches(0.44), fill=ACC_A3, radius=0.12)
txt(hdr_a3, "Ascend A3 · 910C (arch 2201)", size=13, color=BG, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
hdr_a5 = box(s2, bx, Inches(0.98), bw, Inches(0.44), fill=ACC_A5, radius=0.12)
txt(hdr_a5, "Ascend A5 · 950 (arch 3510)", size=13, color=BG, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

rows = [
    ("① 互联总线\n与拓扑",
     "HCCS 板内直连（~784 GB/s）\nscale-out 走 RoCEv2/PCIe，需交换机",
     "灵衢 UnifiedBus(UB) 2.0 全光直连（2 TB/s）\nUB-Mesh 递归全网状，三级（板/柜/架）",
     ACC_A3, ACC_A5),
    ("② 通信模型\n与语义",
     "消息传递为主：HCCL/HCOMM 集合通信\n(AllReduce/ReduceScatter/AllGather)",
     "URMA 单边 (one-sided) 读写\n同时支持 Load/Store 同步 & URMA 异步消息双语义",
     ACC_A3, ACC_A5),
    ("③ 内存/地址\n语义",
     "无跨卡统一编址\n远端访问=多跳/显式消息，KV/权重常回 CPU",
     "SHMEM 全域内存语义 + 统一编址/内存池化\nKV Cache 可放远端 HBM，一条 URMA Read 拉回",
     ACC_A3, ACC_A5),
    ("④ 时延与\n带宽量级",
     "单跳 ~2µs、跨柜 ~7µs\n互联带宽 784 GB/s",
     "单跳 ~200 ns（↓10×，仅指单跳）、跨柜 ~3 µs\n互联带宽 2 TB/s（≈ 2.5× 910C）",
     ACC_A3, ACC_A5),
]

row_h = Inches(1.05)
ry = Inches(1.56)
for (dim, a3, a5, c3, c5) in rows:
    rc = box(s2, hcol, ry, hw, row_h, fill=RGBColor(0x15, 0x1F, 0x2B), line=LINE, radius=0.08)
    txt(rc, dim, size=12, color=TXT, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    ba = box(s2, ax, ry, aw, row_h, fill=CARD_A3, line=RGBColor(0x2A, 0x45, 0x5E), radius=0.08)
    multi_txt(ba, [(a3, 11, TXT, False)])
    bb = box(s2, bx, ry, bw, row_h, fill=CARD_A5, line=RGBColor(0x3A, 0x35, 0x28), radius=0.08)
    multi_txt(bb, [(a5, 11, TXT, False)])
    ry += row_h + Inches(0.10)

# 底部总结条
sumb = box(s2, hcol, Inches(6.16), SW - Inches(0.7), Inches(0.64), fill=RGBColor(0x14, 0x20, 0x2C), line=ACC_A5, radius=0.10)
multi_txt(sumb, [
    ("一句话总结：", 12, ACC_A5, True),
    ("A5 的「网络」不再只是外围通信管道，更像超节点的循环系统（类比）——通过 UB 2.0 + URMA/SHMEM 把多台机器变成统一编址的「一台大机器」，通信从消息式转向内存语义，这是 A3→A5 最本质的网络变化。", 11, TXT, False),
])

label(s2, Inches(0.35), Inches(7.02), Inches(12.6),
      "来源：华为官方超节点/灵衢 2.0、Hot Chips 2025 UB-Mesh 演讲、CANN 面向 950 架构详解（URMA/Entity/UMMU/UBFM）；hcomm(ascend950 CCU/mc2) 与 hixl 本地仓佐证。",
      size=8.5, color=RGBColor(0x6C, 0x7A, 0x88))

out = "Ascend_A5_vs_A3_网络通信对比.pptx"
prs.save(out)
print("saved:", out)
