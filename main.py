import typer
from PIL import Image
from siapy.utils.plots import pixels_select_click

from src.core.configs import DATA_DIR, DATA_PROCESSED_DIR
from src.core.logger import setup_logger

app = typer.Typer()

logger = setup_logger()


@app.command()
def extract_points(experiment_name: str):
    experiment_path = DATA_DIR / experiment_name

    if not experiment_path.exists():
        logger.error(f"Experiment path {experiment_path} does not exist.")
        raise typer.Exit(code=1)

    logger.info(f"Extracting points from experiment: {experiment_name}")
    for img_path in experiment_path.glob("*.jpg"):
        logger.info(f"Processing image: {img_path.name}")

        img = Image.open(img_path)
        pixels = pixels_select_click(img)
        pass


@app.command()
def calculate_transformation_matrix():
    pass


if __name__ == "__main__":
    app()
