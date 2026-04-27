from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scienceplots  # noqa: F401


SYSTEMS = [
    "SIGL",
    "ThreatRace",
    "NodLink",
    "Magic",
    "Kairos",
    "Flash",
    "R-CAID",
    "Orthrus",
]
TUNED = [0.005, 0.02, 0.96, 0.06, 0.01, 0.34, 0.44, 1.00]
UNTUNED = [0.002, 0.01, 0.54, 0.02, 0.01, 0.12, 0.18, 0.45]


def main() -> None:
    out_dir = Path(__file__).resolve().parent

    plt.style.use(["science", "grid", "no-latex"])
    plt.rcParams.update(
        {
            "figure.figsize": (6.2, 3.0),
            "figure.dpi": 220,
            "font.family": "DejaVu Sans",
            "axes.labelsize": 9,
            "xtick.labelsize": 7.8,
            "ytick.labelsize": 8.0,
            "legend.fontsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    x = np.arange(len(SYSTEMS))
    width = 0.34

    fig, ax = plt.subplots()
    bars1 = ax.bar(
        x - width / 2, TUNED, width, color="#2f7ed8", label="Tuned", zorder=3
    )
    bars2 = ax.bar(
        x + width / 2, UNTUNED, width, color="#b7c9e6", label="Untuned", zorder=3
    )

    ax.set_ylabel("Detection performance")
    ax.set_ylim(0, 1.08)
    ax.set_xticks(x)
    ax.set_xticklabels(SYSTEMS, rotation=28, ha="right")
    ax.grid(True, axis="y", color="#d4d4d4", linewidth=0.7, alpha=0.75)
    ax.grid(False, axis="x")
    ax.legend(
        loc="upper left", frameon=False, ncol=2, handlelength=1.4, columnspacing=1.2
    )

    for bar, value in zip(bars1, TUNED):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.02,
            f"{value:.3f}" if value < 0.01 else f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=7,
            color="#2f2f2f",
        )

    for bar, value in zip(bars2, UNTUNED):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.02,
            f"{value:.3f}" if value < 0.01 else f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=7,
            color="#4b5d67",
        )

    fig.tight_layout(pad=0.5)
    fig.savefig(
        out_dir / "bilot_hpo_importance.pdf", bbox_inches="tight", transparent=True
    )
    fig.savefig(
        out_dir / "bilot_hpo_importance.png", bbox_inches="tight", transparent=True
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
