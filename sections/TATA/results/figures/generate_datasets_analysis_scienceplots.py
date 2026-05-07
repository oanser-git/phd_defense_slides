from pathlib import Path

import matplotlib.pyplot as plt
import scienceplots  # noqa: F401


# Reconstructed from the exported figure because the raw plotting data/source is
# not present in the repository. Values are approximate digitizations from the
# image and are meant to provide an editable figure that can later be updated
# cleanly for CIC-IDS 2017 and CSE-CIC-IDS 2018.

DATASETS = [
    "NSL-KDD",
    "CTU-13",
    "ISCX IDS 2012",
    "UNSW-NB15",
    "CIC-UNSW",
    "ISCX Tor 2016",
    "ISCX VPN-NONVPN 2016",
    "CIC-IDS 2017 (with errors)",
    "CIC-IDS 2017",
    "CSE-CIC-IDS 2018 (with errors)",
    "CSE-CIC-IDS 2018",
    "Bot-IoT",
    "CIC-DDoS 2019",
    "ToN-IoT",
    "MNIST",
    "CIFAR",
]

LEFT_DATASETS = DATASETS[:14]
RIGHT_DATASETS = ["MNIST", "CIFAR", "TATA"]

LEFT_X = list(range(1, len(LEFT_DATASETS) + 1))
RIGHT_X = [16, 17, 18]
XTICKS = LEFT_X + RIGHT_X
XTICKLABELS = LEFT_DATASETS + RIGHT_DATASETS

SERIES = {
    "Proximity": {
        "color": "black",
        "values": [0.244, 0.256, 0.267, 0.248, 0.191, 0.214, 0.252, 0.382, 0.221, 0.313, 0.191, 0.218, 0.275, 0.244, 0.573, 0.786],
        "err_low": [0.023, 0.027, 0.008, 0.027, 0.008, 0.008, 0.031, 0.023, 0.031, 0.023, 0.031, 0.027, 0.023, 0.031, 0.023, 0.023],
        "err_high": [0.031, 0.027, 0.031, 0.027, 0.008, 0.015, 0.031, 0.031, 0.023, 0.031, 0.023, 0.027, 0.023, 0.031, 0.023, 0.023],
    },
    "Diversity": {
        "color": "red",
        "values": [0.050, 0.053, 0.050, 0.397, 0.313, 0.050, 0.050, 0.168, 0.122, 0.050, 0.115, 0.088, 0.092, 0.061, 0.408, 0.531],
        "err_low": [0.010, 0.008, 0.010, 0.053, 0.038, 0.010, 0.010, 0.038, 0.023, 0.010, 0.023, 0.034, 0.015, 0.015, 0.027, 0.027],
        "err_high": [0.010, 0.008, 0.010, 0.061, 0.053, 0.010, 0.010, 0.038, 0.023, 0.010, 0.023, 0.034, 0.038, 0.015, 0.027, 0.027],
    },
    "Scarcity": {
        "color": "blue",
        "values": [0.191, 0.137, 0.221, 0.187, 0.229, 0.183, 0.180, 0.092, 0.324, 0.069, 0.260, 0.298, 0.057, 0.176, 0.481, 0.618],
        "err_low": [0.038, 0.038, 0.038, 0.027, 0.031, 0.031, 0.027, 0.031, 0.034, 0.038, 0.031, 0.031, 0.027, 0.031, 0.031, 0.031],
        "err_high": [0.023, 0.023, 0.015, 0.027, 0.023, 0.015, 0.027, 0.023, 0.042, 0.023, 0.031, 0.038, 0.011, 0.031, 0.023, 0.023],
    },
}

# Fill this dictionary once the revised metric values are available.
# Example:
# UPDATED_POINTS = {
#     "CIC-IDS 2017": {"Proximity": 0.35, "Diversity": 0.18, "Scarcity": 0.30},
#     "CSE-CIC-IDS 2018": {"Proximity": 0.29, "Diversity": 0.12, "Scarcity": 0.26},
# }
UPDATED_POINTS = {}

TATA_POINT = {
    "Proximity": {"value": 0.61, "err_low": 0.05, "err_high": 0.05},
    "Diversity": {"value": 0.65, "err_low": 0.04, "err_high": 0.04},
    "Scarcity": {"value": 0.78, "err_low": 0.06, "err_high": 0.06},
}


def apply_plot_style() -> None:
    plt.style.use(["science", "no-latex"])
    plt.rcParams.update(
        {
            "figure.figsize": (5.1, 3.55),
            "figure.dpi": 220,
            "font.family": "DejaVu Sans",
            "axes.labelsize": 9.5,
            "xtick.labelsize": 8.2,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "axes.spines.top": True,
            "axes.spines.right": True,
            "axes.linewidth": 1.0,
        }
    )


def plot_series(ax: plt.Axes) -> None:
    for label, series in SERIES.items():
        ax.errorbar(
            LEFT_X,
            series["values"][: len(LEFT_X)],
            yerr=[
                series["err_low"][: len(LEFT_X)],
                series["err_high"][: len(LEFT_X)],
            ],
            fmt="-o",
            color=series["color"],
            linewidth=1.25,
            markersize=4,
            elinewidth=0.9,
            capsize=3,
            capthick=0.9,
            label=label,
            zorder=3,
        )

        # Right-side comparison targets remain disconnected from the benchmark
        # sequence so the separator explicitly marks a different comparison space.
        right_values = [series["values"][14], series["values"][15], TATA_POINT[label]["value"]]
        right_err_low = [series["err_low"][14], series["err_low"][15], TATA_POINT[label]["err_low"]]
        right_err_high = [series["err_high"][14], series["err_high"][15], TATA_POINT[label]["err_high"]]
        ax.errorbar(
            RIGHT_X,
            right_values,
            yerr=[right_err_low, right_err_high],
            fmt="o",
            color=series["color"],
            linewidth=0,
            markersize=4,
            elinewidth=0.9,
            capsize=3,
            capthick=0.9,
            zorder=3,
        )


def plot_updated_points(ax: plt.Axes) -> None:
    for dataset, metrics in UPDATED_POINTS.items():
        if dataset not in DATASETS:
            continue

        index = DATASETS.index(dataset)
        x = index + 1 if index < len(LEFT_X) else RIGHT_X[index - len(LEFT_X)]

        for metric_name, value in metrics.items():
            series = SERIES[metric_name]
            old_value = series["values"][index]
            color = series["color"]

            ax.plot(
                [x, x],
                [old_value, value],
                color=color,
                linestyle=":",
                linewidth=1.0,
                alpha=0.9,
                zorder=4,
            )
            ax.scatter(
                [x],
                [value],
                s=28,
                marker="D",
                facecolors="white",
                edgecolors=color,
                linewidths=1.0,
                zorder=5,
            )


def main() -> None:
    out_dir = Path(__file__).resolve().parent

    apply_plot_style()
    fig, ax = plt.subplots()

    plot_series(ax)
    plot_updated_points(ax)

    ax.axvline(15, color="black", linestyle="--", linewidth=1.0, zorder=2)
    ax.set_xlim(0.5, 18.5)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Score")
    ax.set_xlabel("Datasets")
    ax.set_xticks(XTICKS)
    ax.set_xticklabels(XTICKLABELS, rotation=50, ha="right")
    ax.set_yticks([0.0, 0.25, 0.50, 0.75, 1.00])
    ax.tick_params(axis="both", which="both", direction="in", top=True, right=True)
    ax.grid(False)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.22),
        ncol=3,
        frameon=False,
        handlelength=1.8,
        columnspacing=1.4,
        handletextpad=0.5,
    )

    fig.tight_layout(pad=0.35)
    fig.savefig(
        out_dir / "datasets_analysis_scienceplots.pdf",
        bbox_inches="tight",
        transparent=True,
    )
    fig.savefig(
        out_dir / "datasets_analysis_scienceplots.png",
        bbox_inches="tight",
        transparent=True,
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
