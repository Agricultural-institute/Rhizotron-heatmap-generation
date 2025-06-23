import numpy as np
import typer
from PIL import Image
from siapy.entities.pixels import Pixels
from siapy.transformations import corregistrator
from siapy.utils.plots import (
    display_multiple_images_with_areas,
    pixels_select_click,
    pixels_select_lasso,
)

from src.core import configs
from src.core.logger import setup_logger
from src.misc.utils import save_pixel_map_to_csv

app = typer.Typer()

logger = setup_logger()


@app.command()
def extract_points_calibration(experiment_name: str, idx_start: int = 0):
    experiment_path = configs.get_experiment_path(experiment_name)
    logger.info(f"Extracting points from experiment: {experiment_name}")

    for img_path in sorted(experiment_path.glob("*.jpg"))[idx_start:]:
        logger.info(f"Processing image: {img_path.name}")
        img = Image.open(img_path)
        logger.info(f"Select points on image: {img_path.name}")
        pixels = pixels_select_click(img)
        logger.info(f"Saving number of points: {len(pixels)}")
        pixels.save_to_parquet(
            configs.get_points_calibration_path(experiment_name, img_path.stem)
        )


@app.command()
def extract_points_organism(experiment_name: str, idx_start: int = 0):
    experiment_path = configs.get_experiment_path(experiment_name)
    logger.info(f"Extracting points from experiment: {experiment_name}")

    for img_path in sorted(experiment_path.glob("*.jpg"))[idx_start:]:
        logger.info(f"Processing image: {img_path.name}")
        img = Image.open(img_path)
        logger.info(f"Select points on image: {img_path.name}")
        pixels = pixels_select_click(img)
        logger.info(f"Saving number of points: {len(pixels)}")
        pixels.save_to_parquet(
            configs.get_points_organism_path(experiment_name, img_path.stem)
        )


@app.command()
def calculate_transformation_matrix(experiment_name: str, alignment_mode: int = 0):
    points_path = configs.get_points_calibration_path(experiment_name)
    logger.info(f"Calculating transformation matrix for experiment: {experiment_name}")

    pixels_map = {}
    for points_path in sorted(points_path.glob("*.parquet")):
        logger.info(f"Processing points file: {points_path.name}")
        pixels = Pixels.load_from_parquet(points_path)
        pixels_map[points_path.stem] = pixels

    pixels0 = pixels_map[list(pixels_map.keys())[0]]
    for image_name, pixels in pixels_map.items():
        # align all to the first one
        if alignment_mode == 0:
            matx, _ = corregistrator.align(pixels0, pixels, plot_progress=False)
        else:
            matx, _ = corregistrator.align(pixels, pixels0, plot_progress=False)

        matx_path = configs.get_matx_path(experiment_name, image_name)
        np.save(matx_path, matx)


@app.command()
def test_calculate_transformation_matrix(experiment_name: str):
    calculate_transformation_matrix(experiment_name, alignment_mode=1)
    experiment_path = configs.get_experiment_path(experiment_name)
    matx_paths = configs.get_matx_path(experiment_name)
    logger.info(f"Testing transformation matrix for experiment: {experiment_name}")

    matx_map = {}
    for matx_path in sorted(matx_paths.glob("*.npy")):
        logger.info(f"Processing matrix file: {matx_path.name}")
        matx = np.load(matx_path)
        matx_map[matx_path.stem] = matx

    images_map = {}
    for img_path in sorted(experiment_path.glob("*.jpg")):
        logger.info(f"Processing image: {img_path.name}")
        images_map[img_path.stem] = Image.open(img_path)

    image0 = images_map[list(images_map.keys())[0]]
    logger.info(f"Select areas on image: {str(image0.filename)}")
    selected_areas_0 = pixels_select_lasso(image0)

    areas_map = {}
    for name, matx in matx_map.items():
        logger.info(f"Transforming image: {name}")
        selected_areas_transformed = [
            corregistrator.transform(pixels, matx) for pixels in selected_areas_0
        ]
        areas_map[name] = selected_areas_transformed

    for name, areas in areas_map.items():
        logger.info(f"Displaying image: {name} with areas")
        image = images_map[name]
        display_multiple_images_with_areas(
            [
                (image0, selected_areas_0),
                (image, areas),
            ],
            plot_interactive_buttons=False,
        )


@app.command()
def generate_results(experiment_name: str):
    calculate_transformation_matrix(experiment_name, alignment_mode=0)
    experiment_path = configs.get_experiment_path(experiment_name)
    points_path = configs.get_points_organism_path(experiment_name)
    matx_paths = configs.get_matx_path(experiment_name)
    results_path = configs.get_results_path(experiment_name)
    logger.info(f"Generating results for experiment: {experiment_name}")

    image0 = Image.open(sorted(experiment_path.glob("*.jpg"))[0])

    matx_map = {}
    for matx_path in sorted(matx_paths.glob("*.npy")):
        logger.info(f"Processing matrix file: {matx_path.name}")
        matx = np.load(matx_path)
        matx_map[matx_path.stem] = matx

    pixels_map = {}
    for points_path in sorted(points_path.glob("*.parquet")):
        logger.info(f"Processing points file: {points_path.name}")
        pixels = Pixels.load_from_parquet(points_path)
        pixels_map[points_path.stem] = pixels

    transformed_pixels_map = {}
    for name in pixels_map.keys():
        if name not in matx_map:
            logger.warning(f"Matrix for {name} not found, skipping.")
            continue

        pixels = pixels_map[name]
        matx = matx_map[name]
        transformed_pixels = corregistrator.transform(pixels, matx)
        normalized_pixels = transformed_pixels.to_numpy() / np.array(
            image0.size
        )  # Normalize to (0, 1) range
        transformed_pixels_map[name] = normalized_pixels

    save_pixel_map_to_csv(
        transformed_pixels_map,
        results_path / f"{experiment_name}_transformed_pixels.csv",
    )


if __name__ == "__main__":
    app()
