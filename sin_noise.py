"""
20231107

Sin Noise

"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("TkAgg")


def sin_noise(width, height):
    y, x = np.indices((height, width))
    offset = np.random.random((height, width)) * 2 * np.pi
    noise = np.sin(y * 2 * np.pi + np.sin(x * 2 * np.pi + offset))
    return noise


if __name__ == "__main__":
    plt.imshow(sin_noise(15, 5), cmap="Greys", interpolation="gaussian")
    plt.show()
