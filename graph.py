"""Plot measurements, filtered estimates, and Kalman gain from the C benchmark."""

from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_EXECUTABLE = PROJECT_ROOT / "build" / "bench_kalman.exe"
DEFAULT_OUTPUT = PROJECT_ROOT / "convergence_plot.png"


def read_benchmark_output(executable: Path) -> tuple[list[int], list[float], list[float], list[float]]:
    """Run the benchmark and parse its CSV-like stdout."""
    completed = subprocess.run(
        [str(executable)],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    rows = csv.DictReader(completed.stdout.splitlines(), skipinitialspace=True)
    steps: list[int] = []
    measurements: list[float] = []
    estimates: list[float] = []
    gains: list[float] = []

    for row in rows:
        steps.append(int(row["Step"]))
        measurements.append(float(row["Measurement"]))
        estimates.append(float(row["EstimatedState"]))
        gains.append(float(row["KalmanGain"]))

    if not steps:
        raise ValueError("The benchmark produced no data rows")

    return steps, measurements, estimates, gains


def create_plot(
    steps: list[int],
    measurements: list[float],
    estimates: list[float],
    gains: list[float],
    output: Path,
) -> None:
    """Create and save the convergence plot."""
    plt.style.use("dark_background")
    figure, signal_axis = plt.subplots(figsize=(8, 4.5), dpi=300)

    measurement_color = "#888888"
    estimate_color = "#00E5FF"
    gain_color = "#FF5252"

    signal_axis.set_xlabel("Time Step (k)", fontsize=11, fontweight="medium")
    signal_axis.set_ylabel("Signal Amplitude", color=estimate_color, fontsize=11)
    measurement_plot = signal_axis.scatter(
        steps,
        measurements,
        color=measurement_color,
        s=40,
        label="Measurement ($z_k$)",
    )
    estimate_plot, = signal_axis.plot(
        steps,
        estimates,
        color=estimate_color,
        linewidth=2,
        label="Filtered State ($\\hat{x}_k$)",
    )
    signal_axis.tick_params(axis="y", labelcolor=estimate_color)
    signal_axis.grid(True, linestyle="--", alpha=0.3)

    gain_axis = signal_axis.twinx()
    gain_axis.set_ylabel("Kalman Gain ($K_k$)", color=gain_color, fontsize=11)
    gain_plot, = gain_axis.plot(
        steps,
        gains,
        color=gain_color,
        linestyle=":",
        linewidth=2,
        label="Gain ($K_k$)",
    )
    gain_axis.tick_params(axis="y", labelcolor=gain_color)

    plots = [measurement_plot, estimate_plot, gain_plot]
    signal_axis.legend(plots, [plot.get_label() for plot in plots], loc="center right", framealpha=0.8)
    signal_axis.set_title("Discrete Scalar Kalman Filter: Step Response & Gain Convergence", fontsize=12, pad=12)

    figure.tight_layout()
    figure.savefig(output)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot the Kalman filter benchmark output.")
    parser.add_argument("--executable", type=Path, default=DEFAULT_EXECUTABLE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()

    if not arguments.executable.exists():
        raise SystemExit(
            f"Benchmark executable not found: {arguments.executable}\n"
            "Build it first with: cmake --build build"
        )

    data = read_benchmark_output(arguments.executable)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    create_plot(*data, arguments.output)
    print(f"Saved plot to {arguments.output}")


if __name__ == "__main__":
    main()
