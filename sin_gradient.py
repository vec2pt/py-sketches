"""
20200913

Sin Gradient

"""

import numpy as np
from PIL import Image


def gradient(
    width: int = 50,
    height: int = 50,
    factor1_min: float = 1,
    factor1_max: float = 1,
    factor2_min: float = 1,
    factor2_max: float = 1,
) -> np.ndarray:
    grid = np.indices((height, width))
    grid_min, grid_max = grid.min(), grid.max()

    row = np.interp(grid[0], (grid_min, grid_max), (0, np.pi))
    col = np.interp(grid[1], (grid_min, grid_max), (0, np.pi))

    factor_template = np.arange(0, width, 1)
    factor1 = np.interp(factor_template, (0, width), (factor1_min, factor1_max))
    factor1 = np.repeat(factor1, height).reshape(height, width)

    factor2 = np.interp(factor_template, (0, width), (factor2_min, factor2_max))
    factor2 = np.repeat(factor2, height).reshape(height, width)

    gradient_array = np.sin(row * factor1) + np.sin(col * factor2)
    min_val = np.min(gradient_array)
    max_val = np.max(gradient_array)
    scaled_gradient = (gradient_array - min_val) / (max_val - min_val)

    return scaled_gradient


if __name__ == "__main__":
    gradient_array = gradient(
        factor2_min=5,
        factor2_max=5,
    )
    img = Image.fromarray((gradient_array * 255).astype(np.uint8), "L")
    img.save("sin_gradient.png")
