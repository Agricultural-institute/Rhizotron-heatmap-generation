from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from scipy.stats import gaussian_kde
from siapy.entities.pixels import PixelCoordinate


def save_pixel_map_to_csv(
    transformed_pixel_map: dict[str, list[PixelCoordinate]], filename: Path
) -> pd.DataFrame:
    csv_data = []

    for exp_name, coordinates in transformed_pixel_map.items():
        for point_index, (x, y) in enumerate(coordinates):
            csv_data.append(
                {
                    "exp_name": exp_name,
                    "point_index": point_index,
                    "x_coordinate": x,
                    "y_coordinate": y,
                }
            )

    df = pd.DataFrame(csv_data)
    df.to_csv(filename, index=False)
    return df


def create_kde_heatmap_overlay(
    df: pd.DataFrame,
    image: Image.Image,
    experiment_name: str,
    output_path: Path,
    figsize: tuple[int, int] = (14, 10),
    resolution: int = 300,
    alpha: float = 0.6,
    cmap: str = "hot",
    show_plot: bool = True,
) -> tuple:
    """
    Create a KDE-based heatmap visualization overlaying positions on the reference image.
    Uses the best possible visualization method with smooth density estimation.

    Args:
        df: DataFrame with columns 'exp_name', 'x_coordinate', 'y_coordinate'
        image: Reference image to use as background
        experiment_name: Name of the experiment for the title
        output_path: Path where to save the heatmap image
        figsize: Figure size (width, height)
        resolution: Grid resolution for KDE evaluation
        alpha: Transparency of the heatmap overlay
        cmap: Colormap for the heatmap
        show_plot: Whether to display the plot

    Returns:
        Figure and axes objects
    """
    # Create KDE-based heatmap
    fig, ax = plt.subplots(figsize=figsize)

    # Display background image with correct coordinate system
    # Use extent=(left, right, bottom, top) and origin='upper' to match image coordinates
    ax.imshow(image, extent=(0, 1, 1, 0), aspect="auto", alpha=0.8, origin="upper")

    # Extract coordinates
    x = df["x_coordinate"].values
    y = df["y_coordinate"].values

    # Create KDE for smooth density estimation
    xy = np.vstack([np.array(x), np.array(y)])
    kde = gaussian_kde(xy)
    kde.set_bandwidth(bw_method="scott")  # Automatic bandwidth selection

    # Create high-resolution grid for evaluation
    xi = np.linspace(0, 1, resolution)
    yi = np.linspace(0, 1, resolution)
    x_grid, y_grid = np.meshgrid(xi, yi)

    # Evaluate KDE on grid
    zi = kde(np.vstack([x_grid.flatten(), y_grid.flatten()]))
    z_grid = zi.reshape(x_grid.shape)

    # Create smooth contour heatmap overlay
    levels = 20
    contour = ax.contourf(x_grid, y_grid, z_grid, levels=levels, cmap=cmap, alpha=alpha)

    # Add scatter points for exact positions with experiment-specific colors
    exp_names = df["exp_name"].unique()
    colors = ["white", "cyan", "yellow", "lime", "magenta"]

    for i, exp in enumerate(exp_names):
        exp_data = df[df["exp_name"] == exp]
        ax.scatter(
            exp_data["x_coordinate"],
            exp_data["y_coordinate"],
            c=colors[i % len(colors)],
            s=25,
            alpha=0.9,
            edgecolors="black",
            linewidth=0.8,
            label=exp,
        )

    # Customize plot
    ax.set_xlim(0, 1)
    ax.set_ylim(
        1, 0
    )  # Invert y-axis to match image coordinate system (top-left origin)
    ax.set_xlabel("X Coordinate (normalized)", fontsize=12)
    ax.set_ylabel("Y Coordinate (normalized)", fontsize=12)
    ax.set_title(
        f"Position Density Heatmap - {experiment_name}",
        fontsize=14,
        fontweight="bold",
    )

    # Add legend for experiments
    if len(exp_names) > 1:
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=10)

    # Add colorbar for density
    cbar = plt.colorbar(contour, ax=ax, shrink=0.8, aspect=20)
    cbar.set_label("Point Density", rotation=270, labelpad=20, fontsize=12)

    # Improve layout
    plt.tight_layout()

    # Save the plot
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")

    # Show the plot
    if show_plot:
        plt.show()

    return fig, ax
