from pathlib import Path

import pandas as pd
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
