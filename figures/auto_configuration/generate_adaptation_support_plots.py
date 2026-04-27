from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scienceplots  # noqa: F401


KDD_ALGOS = ["RF", "DT", "MLP", "l2-LR", "l1-LR", "LinReg", "SVM"]
KDD_BENIGN_SHIFT = [99.53, 97.55, 95.90, 93.35, 92.75, 99.92, 11.94]
KDD_MALICIOUS_SHIFT = [33.54, 40.98, 20.61, 16.86, 19.71, 0.00, 77.98]

QIAO_LABELS = [
    "CNN\nC1 static",
    "CNN\nC3 static",
    "CNN\nadapted avg",
    "LSTM\nadapted avg",
]
QIAO_VALUES = [99.20, 34.67, 98.23, 97.06]
QIAO_COLORS = ["#7f8c8d", "#d62728", "#2ca25f", "#1f77b4"]


def configure_style() -> None:
    plt.style.use(["science", "grid", "no-latex"])
    plt.rcParams.update(
        {
            "figure.dpi": 220,
            "font.family": "DejaVu Sans",
            "axes.labelsize": 8.5,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def plot_kdd(out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.0, 2.05))

    y = np.arange(len(KDD_ALGOS))[::-1]
    for yi, benign, malicious in zip(y, KDD_BENIGN_SHIFT, KDD_MALICIOUS_SHIFT):
        ax.plot([malicious, benign], [yi, yi], color="#bfc8cf", linewidth=2.0, zorder=1)
    ax.scatter(KDD_BENIGN_SHIFT, y, s=38, color="#1f77b4", zorder=3)
    ax.scatter(KDD_MALICIOUS_SHIFT, y, s=38, color="#d95f02", zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(KDD_ALGOS)
    ax.set_xlim(-2, 105)
    ax.set_xlabel("Accuracy (%)")
    ax.grid(True, axis="x", color="#d4d4d4", linewidth=0.7, alpha=0.75)
    ax.grid(False, axis="y")
    ax.tick_params(axis="both", pad=1.5)
    fig.tight_layout(pad=0.3)
    fig.savefig(
        out_dir / "kdd_distribution_shift.pdf", bbox_inches="tight", transparent=True
    )
    fig.savefig(
        out_dir / "kdd_distribution_shift.png", bbox_inches="tight", transparent=True
    )
    plt.close(fig)


def plot_qiao(out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.0, 2.05))
    x = np.arange(len(QIAO_LABELS))
    bars = ax.bar(x, QIAO_VALUES, color=QIAO_COLORS, width=0.62, zorder=3)
    ax.set_ylim(0, 105)
    ax.set_ylabel("Accuracy (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(QIAO_LABELS)
    ax.grid(True, axis="y", color="#d4d4d4", linewidth=0.7, alpha=0.75)
    ax.grid(False, axis="x")
    ax.tick_params(axis="both", pad=1.5)
    for bar, value in zip(bars, QIAO_VALUES):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 2.0,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=7.5,
            color="#2f2f2f",
        )
    fig.tight_layout(pad=0.3)
    fig.savefig(
        out_dir / "qiao_concept_drift.pdf", bbox_inches="tight", transparent=True
    )
    fig.savefig(
        out_dir / "qiao_concept_drift.png", bbox_inches="tight", transparent=True
    )
    plt.close(fig)


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    configure_style()
    plot_kdd(out_dir)
    plot_qiao(out_dir)


if __name__ == "__main__":
    main()
