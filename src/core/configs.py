import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent.absolute()
DATA_DIR = BASE_DIR / "data"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
