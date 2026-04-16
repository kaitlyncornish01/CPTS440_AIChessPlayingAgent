import argparse
import csv
from collections import defaultdict

import matplotlib.pyplot as plt


DEFAULT_INPUT_FILE = "results.csv"
DEFAULT_RUNTIME_PLOT = "runtime_vs_depth.png"
DEFAULT_NODES_PLOT = "nodes_vs_depth.png"


def load_results(input_file):
    grouped_results = defaultdict(lambda: {"time_seconds": [], "nodes": []})

    with open(input_file, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            key = (row["algorithm"], int(row["depth"]))
            grouped_results[key]["time_seconds"].append(float(row["time_seconds"]))
            grouped_results[key]["nodes"].append(float(row["nodes"]))

    return grouped_results


def average(values):
    return sum(values) / len(values) if values else 0.0


def build_series(grouped_results, metric_name):
    series = defaultdict(lambda: {"depths": [], "values": []})

    for (algorithm, depth), metrics in sorted(grouped_results.items()):
        series[algorithm]["depths"].append(depth)
        series[algorithm]["values"].append(average(metrics[metric_name]))

    return series


def plot_metric(series, ylabel, title, output_file):
    plt.figure()

    for algorithm, data in series.items():
        plt.plot(data["depths"], data["values"], marker="o", label=algorithm)

    plt.xlabel("Search Depth")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(sorted({depth for data in series.values() for depth in data["depths"]}))
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate experiment plots from a CSV results file."
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT_FILE,
        help="CSV file produced by experiment.py.",
    )
    parser.add_argument(
        "--runtime-output",
        default=DEFAULT_RUNTIME_PLOT,
        help="Output file for the runtime plot.",
    )
    parser.add_argument(
        "--nodes-output",
        default=DEFAULT_NODES_PLOT,
        help="Output file for the nodes-expanded plot.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    grouped_results = load_results(args.input)

    runtime_series = build_series(grouped_results, "time_seconds")
    nodes_series = build_series(grouped_results, "nodes")

    plot_metric(
        runtime_series,
        ylabel="Average Runtime (seconds)",
        title="Search Runtime vs Depth",
        output_file=args.runtime_output,
    )
    plot_metric(
        nodes_series,
        ylabel="Average Nodes Expanded",
        title="Nodes Expanded vs Depth",
        output_file=args.nodes_output,
    )
