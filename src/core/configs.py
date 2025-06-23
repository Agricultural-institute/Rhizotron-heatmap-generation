import os
from pathlib import Path
from typing import Optional

import typer

from src.core.logger import setup_logger

logger = setup_logger()

BASE_DIR = Path(__file__).parent.parent.parent.absolute()
DATA_DIR = BASE_DIR / "data"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)


def get_experiment_path(experiment_name: str) -> Path:
    experiment_path = DATA_DIR / experiment_name
    if not experiment_path.exists():
        logger.error(f"Experiment path {experiment_path} does not exist.")
        raise typer.Exit(code=1)
    return experiment_path


def get_points_path(experiment_name: str, image_name: Optional[str] = None) -> Path:
    if not image_name:
        points_file = DATA_PROCESSED_DIR / experiment_name / "points"
        os.makedirs(points_file, exist_ok=True)
    else:
        points_file = (
            DATA_PROCESSED_DIR / experiment_name / "points" / f"{image_name}.parquet"
        )
        os.makedirs(points_file.parent, exist_ok=True)
    return points_file


def get_matx_path(experiment_name: str, image_name: Optional[str]) -> Path:
    if not image_name:
        matx_file = DATA_PROCESSED_DIR / experiment_name / "matx"
        os.makedirs(matx_file, exist_ok=True)
    else:
        matx_file = DATA_PROCESSED_DIR / experiment_name / "matx" / f"{image_name}.npy"
        os.makedirs(matx_file.parent, exist_ok=True)
    return matx_file
