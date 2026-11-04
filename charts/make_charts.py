# -*- coding: utf-8 -*-
"""TikTok 北美广告业务分析 - 图表生成（面试案例版）

本地复现：python make_charts.py （输出 PNG + SVG 到 charts/）
依赖：matplotlib
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["svg.fonttype"] = "none"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(OUT, exist_ok=True)

C_MAIN = "#FE2C55"   # TikTok red
C_DARK = "#25F4EE"   # TikTok cyan
C_GREY = "#9aa0a6"
C_BLUE = "#4267B2"
C_BLACK = "#111418"

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=160, bbox_inches="tight", facecolor="white")
    fig.savefig(os.path.join(OUT, name.replace(".png", ".svg")), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)

# 图1 TikTok 美国广告收入 2021-2027E（数据来源：eMarketer 2025.09）
years = ["2021", "2022", "2023", "2024", "2025E", "2026F", "2027F"]
rev = [2.10, 5.96, 8.75, 12.29, 14.03, 17.17, 21.43]
fig, ax = plt.subplots(figsize=(8, 4.5))
colors = [C_MAIN]*5 + [C_GREY]*2
bars = ax.bar(years, rev, color=colors, width=0.62)
for b, v in zip(bars, rev):
    ax.text(b.get_x()+b.get_width()/2, v+0.35, f"{v:.2f}", ha="center", fontsize=10, fontweight="bold")
growth = [None, 183.8, 46.8, 40.5, 14.2, 22.3, 24.8]
for i, g in enumerate(growth):
    if g:
        ax.text(i, rev[i]/2, f"+{g:.0f}%", ha="center", fontsize=9, color="white", fontweight="bold")
ax.set_title("TikTok 美国广告收入：高基数下增速换挡，2026 年起再加速\n（十亿美元，eMarketer 2025年9月预测口径）", fontsize=12, fontweight="bold")
ax.set_ylabel("十亿美元")
ax.spines[["top", "right"]].set_visible(False)
ax.set_ylim(0, 24)
save(fig, "01_us_ad_revenue.png")

# 图2 美国数字广告大盘 2025（数据来源：IAB/PwC FY2025）与 TikTok 位置
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.3), gridspec_kw={"width_ratios": [1.2, 1]})
cats = ["社交", "搜索", "展示", "数字视频", "商业媒体"]
vals = [117.7, 114.2, 81.6, 78.0, 63.4]
ax1.barh(cats[::-1], vals[::-1], color=[C_BLUE if c != "社交" else C_MAIN for c in cats[::-1]])
for i, v in enumerate(vals[::-1]):
    ax1.text(v+1.5, i, f"{v:.1f}", va="center", fontsize=10)
ax1.set_title("美国数字广告分赛道收入 2025（十亿美元，IAB）\n注：按格式/渠道统计口径存在交叉", fontsize=11, fontweight="bold")
ax1.spines[["top", "right"]].set_visible(False)
share_vals = [14.03, 117.7-14.03]
ax2.pie(share_vals, labels=["TikTok\n$14.0B (11.9%)", "其他社交平台\n$103.7B"], colors=[C_MAIN, "#e8eaed"],
        startangle=90, wedgeprops=dict(width=0.42), textprops={"fontsize": 10})
ax2.set_title("TikTok 占美国社交广告支出份额 2025", fontsize=11, fontweight="bold")
fig.tight_layout()
save(fig, "02_market_context.png")

# 图3 ARPU 与时长错配（数据来源：eMarketer 2024/2025）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))
plats = ["Instagram", "Facebook", "TikTok"]
arpu = [223, 191, 109]
bars = ax1.bar(plats, arpu, color=[C_BLUE, C_BLUE, C_MAIN], width=0.55)
for b, v in zip(bars, arpu):
    ax1.text(b.get_x()+b.get_width()/2, v+4, f"${v}", ha="center", fontsize=11, fontweight="bold")
ax1.set_title("美国单用户年广告收入 ARPU（美元，eMarketer 2024）", fontsize=11, fontweight="bold")
ax1.spines[["top", "right"]].set_visible(False)
mins = [35, 30, 52]
bars2 = ax2.bar(plats, mins, color=[C_BLUE, C_BLUE, C_MAIN], width=0.55)
for b, v in zip(bars2, mins):
    ax2.text(b.get_x()+b.get_width()/2, v+1, f"{v} 分钟", ha="center", fontsize=11, fontweight="bold")
ax2.set_title("美国成人单日使用时长（分钟，eMarketer 2025）", fontsize=11, fontweight="bold")
ax2.spines[["top", "right"]].set_visible(False)
fig.suptitle("时长领先 49%，ARPU 仅为 Instagram 的 49% —— 注意力变现效率缺口", fontsize=12.5, fontweight="bold", y=1.03)
fig.tight_layout()
save(fig, "03_monetization_gap.png")

# 图4 TikTok Shop 美国 GMV（Momentum Works/eMarketer）与货币化率（本报告估算）
fig, ax = plt.subplots(figsize=(8, 4.5))
yrs = ["2024", "2025", "2026F"]
gmv = [9.0, 15.1, 23.4]
bars = ax.bar(yrs, gmv, color=[C_DARK, C_DARK, C_GREY], width=0.5, edgecolor=C_BLACK, linewidth=0.5)
for b, v in zip(bars, gmv):
    ax.text(b.get_x()+b.get_width()/2, v+0.4, f"{v:.1f}", ha="center", fontsize=11, fontweight="bold")
ax2 = ax.twinx()
attach = [8.0, 10.0, 11.0]  # 估算：商家广告支出/GMV
ax2.plot(yrs, attach, "o-", color=C_MAIN, linewidth=2.5, markersize=8)
for i, a in enumerate(attach):
    ax2.text(i, a+0.35, f"{a:.0f}%（E）", ha="center", fontsize=10, color=C_MAIN, fontweight="bold")
ax.set_ylabel("美国 TikTok Shop GMV（十亿美元）")
ax2.set_ylabel("电商广告货币化率（GMV Max 等广告支出 / GMV，估算）", color=C_MAIN)
ax2.set_ylim(0, 15)
ax.set_ylim(0, 27)
ax.set_title("电商闭环成为广告第二增长曲线：GMV 扩张 × 货币化率提升\n（GMV：Momentum Works/eMarketer；货币化率为本报告估算 E）", fontsize=12, fontweight="bold")
ax.spines[["top"]].set_visible(False)
save(fig, "04_shop_gmv.png")

# 图5 2025→2027F 收入增长桥（总量锚定 eMarketer，结构分解为本报告估算）
fig, ax = plt.subplots(figsize=(9.5, 4.8))
steps = ["2025\n基线", "电商闭环广告\n(GMV Max)", "监管折价修复\n预算回流", "效果广告自动化\n(Smart+提效)", "搜索/新库存\n(Search/Pulse)", "时长下滑与\n转型摩擦", "2027F"]
lefts = [0, 14.03, 16.93, 18.73, 20.33, 21.63, 0]
heights = [14.03, 2.9, 1.8, 1.6, 1.3, -0.2, 21.43]
colors = [C_MAIN, C_DARK, C_DARK, C_DARK, C_DARK, "#e8710a", C_BLUE]
for i, (l, h, c) in enumerate(zip(lefts, heights, colors)):
    bottom = l if h >= 0 else l + h
    ax.bar(i, abs(h), bottom=bottom, color=c, width=0.62, edgecolor="white")
    label = f"{h:+.1f}" if 0 < i < len(steps)-1 else f"{h:.1f}"
    ax.text(i, bottom+abs(h)+0.25, label, ha="center", fontsize=10, fontweight="bold")
ax.set_xticks(range(len(steps)))
ax.set_xticklabels(steps, fontsize=9)
ax.set_ylabel("十亿美元")
ax.set_title("美国广告收入增长桥 2025→2027F：增量约 74% 来自电商闭环与监管修复\n（总量锚定 eMarketer 基准预测，结构分解为本报告估算 E）", fontsize=12, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
save(fig, "05_growth_bridge.png")

# 图6 三情景预测
fig, ax = plt.subplots(figsize=(8, 4.5))
yrs = ["2024", "2025E", "2026F", "2027F"]
bear = [12.29, 14.03, 15.5, 18.0]
base = [12.29, 14.03, 17.17, 21.43]
bull = [12.29, 14.03, 18.5, 24.5]
x = np.arange(len(yrs))
ax.plot(x, bull, "o--", color=C_DARK, linewidth=2, label="乐观：监管修复+电商超预期 $24.5B")
ax.plot(x, base, "o-", color=C_MAIN, linewidth=2.5, label="基准（eMarketer）$21.4B")
ax.plot(x, bear, "o--", color=C_GREY, linewidth=2, label="保守：转型摩擦+时长下滑 $18.0B")
ax.fill_between(x[2:], bear[2:], bull[2:], alpha=0.12, color=C_MAIN)
for xi, v in zip(x, base):
    ax.text(xi, v+0.5, f"{v:.1f}", ha="center", fontsize=10, fontweight="bold", color=C_MAIN)
ax.set_xticks(x)
ax.set_xticklabels(yrs)
ax.set_ylabel("美国广告收入（十亿美元）")
ax.set_title("三情景预测 2026-2027：基准 22-25% 增速，悲观情形仍有双位数增长", fontsize=12, fontweight="bold")
ax.legend(fontsize=9, loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
ax.set_ylim(10, 27)
save(fig, "06_scenarios.png")

# 图7 监管事件时间线
fig, ax = plt.subplots(figsize=(10, 3.6))
events = [
    ("2024.04", "《保护美国人免受外国对手\n控制应用侵害法》签署", -1),
    ("2025.01.19", "短暂停服 14 小时\n广告预算即时转向 Meta", 1),
    ("2025.09.25", "行政令 14352 批准\n合资框架", -1),
    ("2026.01.22", "TikTok USDS 合资公司交割\n($14B, 美方控股 80%)", 1),
    ("2026.03", "NewFronts 2026\nPulse 高级库存扩张", -1),
    ("2026.05", "TikTok World 2026\nSmart+ Auto Selection", 1),
]
for i, (d, t, side) in enumerate(events):
    ax.scatter(i, 0, s=120, color=C_MAIN, zorder=3)
    ax.annotate(f"{d}\n{t}", (i, 0), xytext=(i, 0.55*side), ha="center",
                fontsize=8.5, va="center",
                arrowprops=dict(arrowstyle="-", color=C_GREY, lw=1))
ax.axhline(0, color=C_BLACK, lw=1.5)
ax.set_xlim(-0.6, len(events)-0.4)
ax.set_ylim(-1.1, 1.1)
ax.axis("off")
ax.set_title("监管不确定性出清：从封禁危机到合资落地（2024-2026）", fontsize=12, fontweight="bold")
save(fig, "07_timeline.png")

print("ALL DONE")
