from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import scienceplots  # noqa: F401


# Values reconstructed from the official ANSSI 2024 map on page 5.
# Corsica is displayed as "<1%" in the source figure; 0.8 is used only for plotting.
REGION_DATA = [
    ("Ile-de-France", 42.0, ">10%"),
    ("Auvergne-Rhone-Alpes", 8.0, "6 to 10%"),
    ("Occitanie", 7.0, "6 to 10%"),
    ("Hauts-de-France", 6.0, "6 to 10%"),
    ("Nouvelle-Aquitaine", 6.0, "6 to 10%"),
    ("PACA", 6.0, "6 to 10%"),
    ("Grand Est", 5.0, "0 to 5%"),
    ("Outre-mer", 5.0, "0 to 5%"),
    ("Pays de la Loire", 4.0, "0 to 5%"),
    ("Bretagne", 3.0, "0 to 5%"),
    ("Normandie", 3.0, "0 to 5%"),
    ("Centre-Val de Loire", 3.0, "0 to 5%"),
    ("Bourgogne-Franche-Comte", 3.0, "0 to 5%"),
    ("Corse", 0.8, "0 to 5%"),
]

COLORS = {
    ">10%": "#8E5737",
    "6 to 10%": "#D88961",
    "0 to 5%": "#F5A07A",
}


def main() -> None:
    out_dir = Path(__file__).resolve().parent

    data = sorted(REGION_DATA, key=lambda item: item[1], reverse=True)
    labels = [item[0] for item in data]
    values = [item[1] for item in data]
    colors = [COLORS[item[2]] for item in data]

    plt.style.use(["science", "no-latex"])
    plt.rcParams.update(
        {
            "figure.figsize": (6.2, 3.3),
            "figure.dpi": 200,
            "font.family": "DejaVu Sans",
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 8.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    fig, ax = plt.subplots()
    bars = ax.barh(
        labels, values, color=colors, edgecolor="none", height=0.72, zorder=3
    )
    ax.invert_yaxis()

    ax.set_xlim(0, 45)
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.set_xlabel("Share of incidents (%)")
    ax.tick_params(axis="both", which="both", top=False, right=False)
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")
    ax.grid(True, axis="x", color="#d4d4d4", linewidth=0.8, alpha=0.8)
    ax.grid(False, axis="y")

    for label, value, bar in zip(labels, values, bars):
        value_text = "<1" if label == "Corse" else f"{int(value)}"
        ax.text(
            value + 0.6,
            bar.get_y() + bar.get_height() / 2,
            value_text,
            va="center",
            ha="left",
            fontsize=8.5,
            color="#2f2f2f",
        )

    legend_items = [
        Patch(facecolor=COLORS[">10%"], label=">10%"),
        Patch(facecolor=COLORS["6 to 10%"], label="6 to 10%"),
        Patch(facecolor=COLORS["0 to 5%"], label="0 to 5%"),
    ]
    ax.legend(
        handles=legend_items,
        loc="lower right",
        frameon=False,
        fontsize=8,
        handlelength=1.3,
        borderpad=0.2,
    )

    fig.tight_layout()
    fig.savefig(
        out_dir / "anssi_regions_scienceplots.pdf",
        bbox_inches="tight",
        transparent=True,
    )
    fig.savefig(
        out_dir / "anssi_regions_scienceplots.png",
        bbox_inches="tight",
        transparent=True,
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
