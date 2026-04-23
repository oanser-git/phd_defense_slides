from pathlib import Path

import matplotlib.pyplot as plt
import scienceplots  # noqa: F401


YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
COSTS = [3.86, 3.92, 3.86, 4.24, 4.35, 4.45, 4.88]


def main() -> None:
    out_dir = Path(__file__).resolve().parent

    plt.style.use(["science", "no-latex"])
    plt.rcParams.update(
        {
            "figure.figsize": (6.2, 3.0),
            "figure.dpi": 200,
            "axes.labelsize": 11,
            "xtick.labelsize": 10.5,
            "ytick.labelsize": 10.5,
            "legend.fontsize": 10,
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    fig, ax = plt.subplots()
    color = "#2f7ed8"

    ax.plot(
        YEARS,
        COSTS,
        color=color,
        linewidth=2.2,
        marker="o",
        markersize=6.8,
        markerfacecolor="white",
        markeredgewidth=1.8,
        markeredgecolor=color,
        zorder=3,
    )

    ax.set_xlim(2017.55, 2024.45)
    ax.set_ylim(3.45, 5.02)
    ax.set_xticks(YEARS)
    ax.set_yticks([3.5, 4.0, 4.5, 5.0])
    ax.set_ylabel("USD millions")
    ax.tick_params(axis="both", which="both", top=False, right=False)
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")

    for year, cost in zip(YEARS, COSTS):
        dy = 10 if year in {2019, 2021} else -15
        va = "bottom" if dy > 0 else "top"
        ax.annotate(
            f"{cost:.2f}",
            (year, cost),
            textcoords="offset points",
            xytext=(0, dy),
            ha="center",
            va=va,
            fontsize=10,
            color="#2f2f2f",
        )

    ax.grid(True, axis="y", color="#d4d4d4", linewidth=0.8, alpha=0.8)
    ax.grid(False, axis="x")

    fig.tight_layout()
    fig.savefig(
        out_dir / "cost_of_breach_scienceplots.pdf",
        bbox_inches="tight",
        transparent=True,
    )
    fig.savefig(
        out_dir / "cost_of_breach_scienceplots.png",
        bbox_inches="tight",
        transparent=True,
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
