import numpy as np
import typer
from PIL import Image
from siapy.entities.pixels import Pixels
from siapy.transformations import corregistrator
from siapy.utils.plots import pixels_select_click

from src.core import configs
from src.core.logger import setup_logger

app = typer.Typer()

logger = setup_logger()


@app.command()
def extract_points(experiment_name: str, idx_start: int = 0):
    experiment_path = configs.get_experiment_path(experiment_name)
    logger.info(f"Extracting points from experiment: {experiment_name}")

    for img_path in sorted(experiment_path.glob("*.jpg"))[idx_start:]:
        logger.info(f"Processing image: {img_path.name}")

        img = Image.open(img_path)
        pixels = pixels_select_click(img)
        pixels.save_to_parquet(configs.get_points_path(experiment_name, img_path.stem))


@app.command()
def calculate_transformation_matrix(experiment_name: str):
    points_path = configs.get_points_path(experiment_name)
    logger.info(f"Calculating transformation matrix for experiment: {experiment_name}")

    pixels_map = {}
    for points_path in sorted(points_path.glob("*.parquet")):
        logger.info(f"Processing points file: {points_path.name}")
        pixels = Pixels.load_from_parquet(points_path)
        pixels_map[points_path.stem] = pixels

    name0 = list(pixels_map.keys())[0]
    for image_name, pixels in pixels_map.items():
        # align all to the first one
        matx, _ = corregistrator.align(pixels_map[name0], pixels, plot_progress=False)
        matx_path = configs.get_matx_path(experiment_name, image_name)
        np.save(matx_path, matx)


if __name__ == "__main__":
    app()
