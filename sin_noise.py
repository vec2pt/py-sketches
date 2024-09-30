"""
20231107

Sin Noise

"""

import numpy as np
from PIL import Image, ImageFilter


def sin_noise(width: int, height: int) -> np.ndarray:
    y, x = np.indices((height, width))
    offset = np.random.random((height, width)) * 2 * np.pi
    noise = np.sin(y * 2 * np.pi + np.sin(x * 2 * np.pi + offset))
    min_val = np.min(noise)
    max_val = np.max(noise)
    scaled_noise = (noise - min_val) / (max_val - min_val)
    return scaled_noise


if __name__ == "__main__":
    noise = sin_noise(15, 5)
    img = Image.fromarray((noise * 255).astype(np.uint8), "L")
    img = img.filter(ImageFilter.GaussianBlur(1))
    img.save("sin_noise.png")
