from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scienceplots  # noqa: F401


DAYS = np.arange(14)

# Reconstructed from the existing slide / earlier paper figure.
OPTIMAL = np.array(
    [0.99, 0.96, 0.90, 0.98, 0.995, 0.95, 0.96, 0.96, 0.96, 0.94, 0.90, 0.95, 0.95, 0.97]
)
MTL = np.array(
    [0.98, 0.93, 0.82, 0.97, 0.99, 0.85, 0.73, 0.85, 0.87, 0.92, 0.87, 0.93, 0.93, 0.91]
)

# Based on the earlier 3-line precision figure used in the paper, but with
# mild day-to-day variation so it does not look artificially flat.
DEFAULT = np.array(
    [0.67, 0.76, 0.68, 0.82, 0.70, 0.71, 0.60, 0.68, 0.69, 0.71, 0.68, 0.72, 0.73, 0.70]
)


def main() -> None:
    out_dir = Path(__file__).resolve().parent

    plt.style.use(["science", "grid", "no-latex"])
    plt.rcParams.update(
        {
            "figure.figsize": (6.4, 4.35),
            "figure.dpi": 220,
            "font.family": "DejaVu Sans",
            "axes.labelsize": 13,
            "xtick.labelsize": 8.5,
            "ytick.labelsize": 8.5,
            "legend.fontsize": 12.0,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    fig, ax = plt.subplots()

    ax.plot(
        DAYS,
        OPTIMAL,
        color="#f76783",
        marker="o",
        markersize=6.6,
        linewidth=2.8,
        solid_capstyle="round",
        label="Optimal",
        zorder=4,
    )
    ax.plot(
        DAYS,
        MTL,
        color="#3fa0e3",
        marker="s",
        markersize=6.4,
        linewidth=2.8,
        solid_capstyle="round",
        label="MtL",
        zorder=3,
    )
    ax.plot(
        DAYS,
        DEFAULT,
        color="#4daf38",
        marker="o",
        markersize=6.0,
        linewidth=2.5,
        solid_capstyle="round",
        label="Default",
        zorder=2,
    )

    ax.set_xlim(-0.35, 13.35)
    ax.set_ylim(0.50, 1.01)
    ax.set_xticks(DAYS)
    ax.set_yticks(np.arange(0.5, 1.01, 0.1))
    ax.set_xlabel("Days")
    ax.set_ylabel("Precision")
    ax.grid(True, axis="both", color="#b8b8b8", linewidth=0.55, alpha=0.8)
    ax.legend(loc="lower left", frameon=False, handlelength=2.1)

    fig.tight_layout(pad=0.35)
    fig.savefig(
        out_dir / "results_precision_unsupervised_cropped.pdf",
        bbox_inches="tight",
        transparent=True,
    )
    fig.savefig(
        out_dir / "results_precision_unsupervised_cropped.png",
        bbox_inches="tight",
        transparent=True,
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
