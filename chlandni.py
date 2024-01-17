"""
20240116

Chladni Patterns

Links:
    https://en.wikipedia.org/wiki/Chladni%27s_law
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def chlandni_func(
    x: np.ndarray,
    y: np.ndarray,
    m: float = 1,
    n: float = 1,
    a: float = 1,
    b: float = 1,
) -> np.ndarray:
    """Chlandni function

    Args:
        x (np.ndarray): X array
        y (np.ndarray): Y array
        m (float, optional): m parameter. Defaults to 1.
        n (float, optional): n parameter. Defaults to 1.
        a (float, optional): a parameter. Defaults to 1.
        b (float, optional): b parameter. Defaults to 1.

    Returns:
        np.ndarray: Output array
    """
    return abs(
        a * np.sin(np.pi * n * x) * np.sin(np.pi * m * y)
        + b * np.sin(np.pi * m * x) * np.sin(np.pi * n * y)
    )


def min_max_scaling(array: np.ndarray) -> np.ndarray:
    """Min-Max scaling

    Args:
        array (np.ndarray): Array

    Returns:
        np.ndarray: Min-Max Scaled array
    """
    min_val = np.min(array)
    max_val = np.max(array)
    return (array - min_val) / (max_val - min_val)


def chlandni(
    width: int = 512,
    height: int = 512,
    m: float = 1,
    n: float = 1,
    a: float = 1,
    b: float = 1,
) -> np.ndarray:
    """Chlandni

    Args:
        width (int, optional): Img width. Defaults to 512.
        height (int, optional): Img height. Defaults to 512.
        m (float, optional): m parameter. Defaults to 1.
        n (float, optional): n parameter. Defaults to 1.
        a (float, optional): a parameter. Defaults to 1.
        b (float, optional): b parameter. Defaults to 1.

    Returns:
        np.ndarray: Output array
    """
    shape = (height, width)
    x, y = np.meshgrid(
        np.linspace(0.0, 1.0, shape[1]),
        np.linspace(0.0, 1.0, shape[0]),
    )
    results = chlandni_func(x, y, m=m, n=n, a=a, b=b)
    results = abs(min_max_scaling(results) - 1)  # Inversion
    results = results**10  # Contrast

    # Simple sand effect
    random_array = np.random.random(shape)
    results = np.where(random_array > 0.65, random_array, 0) * results

    return (min_max_scaling(results) * 255).astype(np.uint8)


if __name__ == "__main__":
    matplotlib.use("TkAgg")

    output = chlandni(m=3, n=2, a=-1.29, b=2.26)
    plt.imshow(output, cmap="gray")
    plt.show()
