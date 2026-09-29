# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib==3.11.2", "numpy>=2,<3"]
# ///
"""Render the manuscript's data-scale and acquisition-cost figure with Matplotlib.

Run with `uv run report/plot_scales.py`. The PGF output is embedded between
the PYPLOT markers in robotoken.tex; SVG and PNG outputs serve the website.
The measurements and scenario inputs are transcribed from the manuscript,
not newly collected evidence. The two public releases are not an industry census.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import NullLocator


REPORT = Path(__file__).resolve().parent
WEB = REPORT.parent / "website/public/figures"
INK = "#25282b"
MUTED = "#62696f"
GRID = "#e4e7e9"
BLUE = "#285e7d"
PALE_BLUE = "#e7eff4"
AMBER = "#a7652a"

# Manuscript refs: gpt3, deepseekv3, qwen3, deepseekv41 (trillion exposures).
MODELS = ["GPT-3", "DeepSeek-V3", "Qwen3", "DeepSeek-V4.1-Flash"]
TOKENS = [0.3, 14.8, 36, 45]
# Manuscript refs: droid and agibot (retained definitions differ by source).
DATASETS = ["DROID", "AgiBot World"]
HOURS = [350, 2976.4]

# Five-year, one-operator-per-station scenarios from the report's input table.
YEARS, STAFFED_HOURS, PURCHASES = 5, 2000, 2
SCENARIOS = {
    "Low": (20, 5, 32000, 0.10, 0.60),
    "Base": (45, 15, 100000, 0.15, 0.40),
    "High": (70, 30, 200000, 0.20, 0.20),
}
RATES = {
    name: (YEARS * STAFFED_HOURS * (wage + overhead)
           + hardware * (PURCHASES + YEARS * maintenance))
    / (YEARS * STAFFED_HOURS * retention)
    for name, (wage, overhead, hardware, maintenance, retention)
    in SCENARIOS.items()
}
REFERENCE_HOURS = 2e12 / (3600 * 10)
REFERENCE_BILLIONS = REFERENCE_HOURS * RATES["Base"] / 1e9


def style_axes(ax, grid_axis="x"):
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#aeb5ba")
    ax.spines["bottom"].set_linewidth(0.65)
    ax.tick_params(axis="both", length=0, pad=5, colors=MUTED)
    ax.xaxis.set_minor_locator(NullLocator())
    ax.yaxis.set_minor_locator(NullLocator())
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.55, zorder=0)
    ax.set_axisbelow(True)


def comparison(ax, labels, values, value_labels, ticks, tick_labels, limits,
               xlabel, mobile):
    """A labeled dot plot; stems are guides, not zero-based magnitude bars."""
    positions = np.arange(len(values))[::-1]
    ax.set_xscale("log")
    ax.set_xlim(*limits)
    ax.set_ylim(-0.6, len(values) - (0.1 if mobile else 0.5))
    ax.set_xticks(ticks, tick_labels)
    ax.set_xlabel(xlabel, labelpad=7, color=MUTED)
    style_axes(ax)
    for y, name, value, label in zip(positions, labels, values, value_labels):
        ax.hlines(y, limits[0], value, color="#b6c7d3", linewidth=1.0)
        ax.plot(value, y, "o", color=BLUE, markersize=4.6, zorder=3)
        ax.annotate(label, (value, y), xytext=(7, 0),
                    textcoords="offset points", va="center", color=BLUE,
                    fontsize=8.3)
        if mobile:
            ax.text(0, y + 0.32, name, transform=ax.get_yaxis_transform(),
                    ha="left", va="bottom", fontsize=8.5, color=INK)
    if mobile:
        ax.set_yticks([])
    else:
        ax.set_yticks(positions, labels, color=INK)
        ax.tick_params(axis="y", pad=12)


def make_figure(mobile=False):
    fig = plt.figure(figsize=(3.6, 8.8) if mobile else (6.35, 6.2), facecolor="white")
    title_x = 0.03 if mobile else 0.015

    # Fixed panel geometry preserves whitespace and avoids long-label collisions.
    if mobile:
        model_box, robot_box, cost_box = (
            [0.12, 0.690, 0.81, 0.232],
            [0.12, 0.475, 0.81, 0.104],
            [0.16, 0.150, 0.56, 0.210],
        )
        title_positions = [0.972, 0.634, 0.416]
    else:
        model_box, robot_box, cost_box = (
            [0.31, 0.733, 0.61, 0.181],
            [0.31, 0.523, 0.61, 0.083],
            [0.13, 0.140, 0.68, 0.252],
        )
        title_positions = [0.970, 0.656, 0.452]

    for text, y in zip(
        ["A   Language-model pretraining", "B   Public robot datasets",
         "C   Five-year acquisition cost"], title_positions
    ):
        fig.text(title_x, y, text, fontsize=10, weight="bold", va="top", color=INK)

    ax_a = fig.add_axes(model_box)
    comparison(ax_a, MODELS, TOKENS, ["0.3T", "14.8T", "36T", "45T"],
               [0.3, 1, 10, 100], ["0.3", "1", "10", "100"], (0.2, 110),
               "Trillion token exposures  (log scale)", mobile)

    ax_b = fig.add_axes(robot_box)
    comparison(ax_b, DATASETS, HOURS, ["350 h", "2,976.4 h"],
               [100, 1000, 10000], ["100", "1,000", "10,000"], (100, 14000),
               "Robot interaction hours  (log scale)", mobile)

    ax = fig.add_axes(cost_box)
    x = np.geomspace(0.1, 1000, 200)  # Millions of newly retained robot-hours.
    costs = {name: x * rate / 1000 for name, rate in RATES.items()}
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.1, 1000)
    ax.set_ylim(0.003, 1600)
    ax.set_xticks([0.1, 1, 10, 100, 1000], ["0.1", "1", "10", "100", "1,000"])
    ax.set_yticks([0.01, 0.1, 1, 10, 100, 1000],
                  ["0.01", "0.1", "1", "10", "100", "1,000"])
    style_axes(ax, "y")
    ax.set_xlabel("Million retained robot-hours", labelpad=8, color=MUTED)
    if mobile:
        ax.text(0, 1.07, "Acquisition cost (USD billions)", transform=ax.transAxes,
                fontsize=8, color=MUTED)
    else:
        ax.set_ylabel("Acquisition cost (USD billions)", labelpad=8, color=MUTED)
    ax.fill_between(x, costs["Low"], costs["High"], color=PALE_BLUE, zorder=1)
    for name in ["High", "Base", "Low"]:
        base = name == "Base"
        ax.plot(x, costs[name], color=BLUE if base else "#91a8b8",
                lw=1.6 if base else 0.75, ls="-" if base else (0, (4, 2)), zorder=3)
        ax.annotate(f"{name} " + rf"$\${RATES[name]:.0f}$/h",
                    (1000, costs[name][-1]), xytext=(6, 0), textcoords="offset points",
                    ha="left", va="center", color=BLUE if base else MUTED,
                    fontsize=7.7, linespacing=1.35, weight="bold" if base else "normal")

    for budget in [1, 10]:
        ax.axhline(budget, color="#858c91", lw=0.7, ls=(0, (2, 3)), zorder=2)
        ax.annotate(rf"$\${budget}$B budget", (0.1, budget), xytext=(4, 4),
                    textcoords="offset points", color=MUTED, fontsize=7,
                    bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.3})

    reference_x = REFERENCE_HOURS / 1e6
    ax.vlines(reference_x, 0.003, REFERENCE_BILLIONS,
              color=AMBER, ls=(0, (3, 3)), lw=0.85, zorder=4)
    ax.plot(reference_x, REFERENCE_BILLIONS, "D", color=AMBER,
            markersize=4.6, markeredgecolor="white", markeredgewidth=0.7, zorder=5)
    ax.annotate("2T accounting scenario\n" + rf"55.6M hours / $\${REFERENCE_BILLIONS:.1f}$B",
                (reference_x, REFERENCE_BILLIONS), xytext=(0.28, 0.96),
                textcoords="axes fraction", color=AMBER, fontsize=7.7,
                va="top", linespacing=1.4,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5},
                arrowprops={"arrowstyle": "-", "color": AMBER, "lw": 0.75,
                            "connectionstyle": "angle,angleA=0,angleB=90,rad=0",
                            "shrinkA": 4, "shrinkB": 5})

    note = ("Both axes use log scales. Shading spans cost scenarios, not a confidence interval.\n"
            "2T assumes 10 Hz, one pass and all-new robot data. Training compute is excluded.")
    if mobile:
        note = ("Log scales. Shading shows low/high cost scenarios,\n"
                "not a confidence interval. 2T: 10 Hz, one pass,\n"
                "all-new robot data. Training compute excluded.\n"
                "No capability equivalence assumed.")
    fig.text(title_x, 0.018, note, fontsize=6.9, color=MUTED, va="bottom", linespacing=1.5)
    return fig


def main():
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans"], "font.size": 8.3,
        "axes.labelsize": 8, "xtick.labelsize": 7.6, "ytick.labelsize": 8.3,
        "svg.fonttype": "path", "svg.hashsalt": "robotoken-scales-cost",
        "mathtext.fontset": "dejavusans", "pgf.texsystem": "pdflatex",
        "pgf.rcfonts": False,
        "pgf.preamble": r"\usepackage[T1]{fontenc}\usepackage{helvet}",
    })
    WEB.mkdir(parents=True, exist_ok=True)
    figures = REPORT / "figures"
    figures.mkdir(exist_ok=True)
    for mobile in [False, True]:
        fig = make_figure(mobile)
        name = "scales-cost-mobile" if mobile else "scales-cost"
        fig.savefig(WEB / f"{name}.svg", metadata={"Date": None})
        fig.savefig(WEB / f"{name}.png", dpi=240)
        if not mobile:
            fig.savefig(figures / "scales-cost.pgf", backend="pgf")
        plt.close(fig)
    print(f"Rates: {RATES}; 2T: {REFERENCE_HOURS:,.3f} h / USD {REFERENCE_BILLIONS:.3f}B")
    print(f"Wrote desktop/mobile SVG and PNG to {WEB}; vector PGF to {figures}")


if __name__ == "__main__":
    main()
