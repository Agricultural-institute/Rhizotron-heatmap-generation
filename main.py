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

    pixels_list = []
    for points_path in sorted(points_path.glob("*.parquet")):
        logger.info(f"Processing points file: {points_path.name}")
        pixels = Pixels.load_from_parquet(points_path)
        pixels_list.append(pixels)

    matx, _ = corregistrator.align(pixels_list[0], pixels_list[1], plot_progress=False)


if __name__ == "__main__":
    app()
