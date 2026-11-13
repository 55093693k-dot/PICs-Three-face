# -*- coding: utf-8 -*-
"""plot_geometry.py -- draw the device geometry straight from sketch_v15.txt.

The sketch is a plain-text description of every polygon (same file the FDTD model is built
from), so this picture cannot drift from the simulated structure.

Layers drawn: silicon (blue) and the etched holes (white).
Requires only numpy + matplotlib:   python plot_geometry.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon

# CJK so the Chinese captions render instead of tofu boxes
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC",
                                   "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
SI, HOLE = "#2f5f9e", "#ffffff"


def parse(path):
    out = []
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split()
        kind = parts[0]
        if kind in ("RECT", "CLADR"):
            out.append((kind, parts[1], *[float(v) for v in parts[2:6]]))
        elif kind == "RING":
            out.append((kind, parts[1], *[float(v) for v in parts[2:6]]))
        elif kind == "POLY":
            vs = [tuple(float(v) for v in p.split(",")) for p in parts[2:]]
            out.append((kind, parts[1], vs))
    return out


def draw(ax, objs):
    for o in objs:
        k, nm = o[0], o[1]
        if k == "RECT":
            _, _, xc, yc, w, h = o
            ax.add_patch(plt.Rectangle((xc - w / 2, yc - h / 2), w, h,
                                       facecolor=SI, edgecolor="none", zorder=2))
        elif k == "POLY":
            ax.add_patch(Polygon(o[2], closed=True, facecolor=SI, edgecolor="none",
                                 zorder=2))
        elif k == "RING":
            _, _, xc, yc, r, w = o
            t = np.linspace(0, 2 * np.pi, 240)
            ax.add_patch(Polygon(np.c_[np.r_[xc + (r - w / 2) * np.cos(t),
                                            xc + (r + w / 2) * np.cos(t)[::-1]],
                                       np.r_[yc + (r - w / 2) * np.sin(t),
                                            yc + (r + w / 2) * np.sin(t)[::-1]]],
                                 closed=True, facecolor=SI, edgecolor="none", zorder=3))
        elif k == "CLADR":
            _, _, xc, yc, w, h = o
            ax.add_patch(plt.Rectangle((xc - w / 2, yc - h / 2), w, h,
                                       facecolor=HOLE, edgecolor="#9fb4cc", lw=0.35,
                                       zorder=4))


def main():
    objs = parse(os.path.join(HERE, "sketch_v15.txt"))
    fig, axs = plt.subplots(1, 2, figsize=(12.6, 6.2), dpi=120)

    ax = axs[0]
    draw(ax, objs)
    ax.add_patch(plt.Rectangle((-15, -15), 30, 30, fill=False, ec="#1663d6",
                               ls=(0, (6, 3)), lw=1.1, zorder=6))
    ax.set_xlim(-16, 16)
    ax.set_ylim(-16, 16)
    ax.set_aspect("equal")
    ax.set_title("整体：30×30 µm 版图（虚线为画布边界）", fontsize=10)
    ax.set_xlabel("x (µm)")
    ax.set_ylabel("y (µm)")

    ax = axs[1]
    draw(ax, objs)
    ax.set_xlim(5.0, 10.0)
    ax.set_ylim(-2.6, 2.6)
    ax.set_aspect("equal")
    ax.set_title("光子晶体十字缺陷（中心 4 孔移除，形成 0.16 µm 通道）", fontsize=10)
    ax.set_xlabel("x (µm)")

    fig.tight_layout()
    out = os.path.join(HERE, "..", "figures", "structure.png")
    fig.savefig(os.path.abspath(out))
    print("wrote", os.path.abspath(out))


if __name__ == "__main__":
    main()
