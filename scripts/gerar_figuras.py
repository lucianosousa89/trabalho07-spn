import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
sys.path.insert(0, ".")
from dados import JUPITER

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
BLUE, DARK = "#2a78d6", "#12407f"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"
plt.rcParams.update({
    "font.size": 7, "axes.labelsize": 6.5, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
    "axes.linewidth": 0.6, "figure.facecolor": SURF, "axes.facecolor": SURF,
    "pdf.fonttype": 42, "ps.fonttype": 42,
})
# (índice, título, unidade, casas decimais por faixa)
PAIN = [(5, "Probabilidade de descarte", "(%)"), (6, "Vazão", "(req/s)"),
        (7, "Utilização dos servidores", "(%)"), (8, "Tempo médio de resposta", "(ms)")]


def fmt(idx, v):
    if idx == 5:
        t = f"{v:.3f}" if v < 0.1 else (f"{v:.2f}" if v < 1 else f"{v:.1f}")
        if v < 0.0005: t = "0"
    elif idx == 8:
        t = f"{v:.0f}"
    else:
        t = f"{v:.1f}"
    return t.replace(".", ",")


def serie(exp):
    return [l for l in JUPITER if l[0] == exp]


def figura(exp, xs, xlabel, nome, ref_idx, bars=False, xlabels=None, extra=None):
    linhas = serie(exp)
    fig, axs = plt.subplots(1, 4, figsize=(7.2, 2.55), dpi=300)
    for ax, (idx, titulo, un) in zip(axs, PAIN):
        ys = [l[idx] * (1000 if idx == 8 else 1) for l in linhas]
        pos = list(range(len(ys))) if bars else xs
        top = max(ys) * 1.28 if max(ys) > 0 else 1
        if bars:
            cores = [DARK if i == ref_idx else BLUE for i in range(len(ys))]
            ax.bar(pos, ys, width=0.55, color=cores, edgecolor="none", zorder=3)
            ax.set_xticks(pos); ax.set_xticklabels(xlabels)
        else:
            ax.plot(pos, ys, color=BLUE, lw=1.5, marker="o", ms=4, mfc=BLUE, mec=SURF, mew=0.8, zorder=3)
            ax.scatter([pos[ref_idx]], [ys[ref_idx]], s=48, facecolors="none", edgecolors=INK, linewidths=1.1, zorder=4)
            ax.set_xticks(xs); ax.margins(x=0.1)
        for x, y in zip(pos, ys):
            ax.annotate(fmt(idx, y), (x, y), textcoords="offset points", xytext=(0, 4),
                        ha="center", va="bottom", fontsize=5.8, color=INK2, zorder=6,
                        bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9))
        ax.set_ylim(0, top)
        ax.set_title(titulo, fontsize=6.8, color=INK, pad=3)
        ax.set_ylabel(un); ax.set_xlabel(xlabel)
        ax.grid(axis="y", color=GRID, lw=0.5); ax.set_axisbelow(True)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
    h = [Line2D([], [], color=BLUE, lw=1.5, marker="o", ms=4, label="Simulação (Jupiter)")] if not bars else \
        [Patch(color=BLUE, label="Simulação (Jupiter)")]
    h.append(Line2D([], [], color=INK, marker="o", mfc="none", ls="", ms=6, label="Cenário de referência") if not bars
             else Patch(color=DARK, label="Cenário de referência (B)"))
    fig.legend(handles=h, loc="lower center", ncol=len(h), frameon=False, fontsize=6.5, handlelength=1.6, columnspacing=1.4)
    fig.tight_layout(pad=0.5, w_pad=0.9, rect=(0, 0.085, 1, 1))
    for ext in ("pdf", "png"):
        fig.savefig(f"{OUT}/{nome}.{ext}", dpi=300)
    plt.close(fig)


def e1_extra(ax, idx, ys, top):
    ax.axvline(60, color=INK2, lw=0.7, ls=(0, (3, 2)), zorder=2)  # ρ = 1
    if idx == 6:
        ax.axhline(60, color=INK2, lw=0.7, ls=(0, (3, 2)), zorder=2)
        ax.text(21, 58.5, "c·μ = 60", fontsize=5.8, color=INK2, va="top")
        top = max(top, 74)
    if idx == 5:
        ax.text(61.5, top * 0.9, "ρ = 1", fontsize=5.8, color=INK2)
    if idx == 8:
        ax.axhline(100, color=INK2, lw=0.7, ls=(0, (3, 2)), zorder=2)
        ax.text(99, 104, "100 ms", fontsize=5.8, color=INK2, va="bottom", ha="right")
    return top


def e2_extra(ax, idx, ys, top):
    if idx == 8:
        ax.axhline(100, color=INK2, lw=0.7, ls=(0, (3, 2)), zorder=2)
        ax.text(3.98, 104, "100 ms", fontsize=5.8, color=INK2, va="bottom", ha="right")
    return top


figura("E1", [20, 40, 60, 80, 100], "λ (req/s)", "fig_E1_demanda", 1, extra=e1_extra)
figura("E2", [2, 3, 4], "Servidores c", "fig_E2_servidores", 1, extra=e2_extra)
figura("E3", [5, 10, 20], "Capacidade K", "fig_E3_capacidade", 2)
figura("E4", None, "Cenário (λ req/s, c)", "fig_E4_combinado", 1, bars=True, xlabels=["A\n(20, 2)", "B\n(40, 3)", "C\n(80, 5)"])
print("ok")
