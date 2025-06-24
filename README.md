# Rhizotron Heatmap Generation

This project enables spatial analysis by registering and merging location data from multiple experimental images into a unified coordinate space. The system uses linear affine transformations based on manually selected corresponding reference points to align images.

## Applications

This tool is particularly useful for:

- Root growth analysis in rhizotron studies
- Temporal tracking of biological specimens across multiple imaging sessions
- Spatial density analysis of organisms or features in experimental setups
- Multi-timepoint image registration and analysis

## Installation

Run installation script:

```bash
./scripts/install-dev.sh
```

The dependencies are locked in `uv.lock` file to ensure reproducible installations. The project dependencies are defined in `pyproject.toml`.

## How to Use

This guide provides step-by-step instructions for the complete workflow from image preparation to heatmap generation.

### Prerequisites

- Images should be from the same experimental setup (rhizotron) captured at different time points
- All images should have similar camera position
- Reference image should be named to appear first alphabetically (e.g., using `_` prefix)

### Example Dataset

The repository includes an example dataset `3-Octanone-A.lineatus` to help you follow these instructions.

---

### Step 1: Prepare Your Data

Create a directory structure for your experiment:

```text
data/
└── your-experiment-name/
    ├── _reference_image.jpg      # Reference image (prefix ensures first position)
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

**Important**: The reference image (first alphabetically) will be used as the coordinate space for all other images.

---

### Step 2: Extract Calibration Points

Select corresponding reference points across all images for spatial registration.

```bash
uv run main.py extract-points-calibration "experiment-name"

# Example:
uv run main.py extract-points-calibration "3-Octanone-A.lineatus"
```

**Calibration Point Selection Guidelines:**

- Select **minimum 6 points** per image
- Choose the **same points in the same order** across all images
- Recommended points for rhizotron studies:
  1. Seed/root crown positions (2 points)
  2. Rhizotron corners (4+ points)
- Points should be easily identifiable in all images
- More points = better registration accuracy

**Interactive Process:**

- Click on each calibration point in the displayed image
- Follow the same order for all images
- Points are automatically saved when you press ENTER

---

### Step 3: Extract Organism/Feature Points

Select the objects or features of interest that you want to track and analyze.

```bash
uv run main.py extract-points-organism "experiment-name"

# Example:
uv run main.py extract-points-organism "3-Octanone-A.lineatus"
```

**Feature Selection Guidelines:**

- Select all organisms/features you want to include in the analysis
- These points will be transformed to the reference image space
- Click on each organism position in every image
- The number of points can vary between images

---

### Step 4: Generate Results and Heatmap

Process all data and automatically generate the final heatmap visualization:

```bash
uv run main.py generate-results "experiment-name"

# Example:
uv run main.py generate-results "3-Octanone-A.lineatus"
```

**This command automatically:**

1. Calculates transformation matrices using calibration points
2. Transforms organism points to the reference coordinate space
3. Normalizes coordinates between 0 and 1
4. Exports data as CSV file
5. Generates a heatmap visualization
6. Saves results in `data/processed/"experiment-name"`

---

### Output Files

**CSV Structure:**

- `exp_name`: Experiment name
- `point_index`: Sequential point number
- `x_coordinate`: Normalized X position (0-1)
- `y_coordinate`: Normalized Y position (0-1)

**Heatmap Features:**

- KDE-based smooth density visualization
- Reference image as background
- Color-coded experimental replicates
- High-resolution (300 DPI) publication-ready output

---

### Tips for Best Results

1. **Consistent Calibration**: Use the same calibration points across all images
2. **Good Reference Points**: Choose points that are clearly visible and stable
3. **Adequate Coverage**: Distribute calibration points across the entire image area
4. **Quality Control**: Visually inspect the generated heatmap for proper alignment
5. **Multiple Replicates**: Include multiple experimental replicates for robust analysis

---

> **Note:** Life's a mess, might as well dance in it 💃🕺lol
