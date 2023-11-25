"""
20231125

Gray-Scott Model

Links:
    https://itp.uni-frankfurt.de/~gros/StudentProjects/Projects_2020/projekt_schulz_kaefer/
    https://groups.csail.mit.edu/mac/projects/amorphous/GrayScott/
    https://www.mrob.com/pub/comp/xmorphia/index.html
"""


import matplotlib
import matplotlib.image
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage

matplotlib.use("TkAgg")


class GrayScottModel:
    """Gray-Scott Model"""

    def __init__(
        self,
        width: int = 50,
        height: int = 50,
        d_u: float = 0.01,
        d_v: float = 0.005,
        f: float = 0.029,
        k: float = 0.057,
        initiate_randomly: bool = False,
    ) -> None:
        """Gray-Scott Model

        Args:
            width (int, optional): Sample width. Defaults to 50.
            height (int, optional): Sample height. Defaults to 50.
            d_u (float, optional): U diffusion rate. Defaults to 0.01.
            d_v (float, optional): V diffusion rate. Defaults to 0.005.
            f (float, optional): Feed rate. Defaults to 0.029.
            k (float, optional): Kill rate. Defaults to 0.057.
            initiate_randomly (bool, optional): Initiate randomly. Defaults to False.
        """
        self._u = np.ones((height, width))
        self._v = np.zeros((height, width))
        if initiate_randomly:
            mask = np.random.random((height, width))
            mask = mask < 0.3
        else:
            mask = np.full((height, width), False)
            mask[
                height // 3 + 1 : -height // 3, width // 3 + 1 : -width // 3
            ] = True
        self._u[mask] = 0.50
        self._v[mask] = 0.25

        self._d_u = d_u
        self._d_v = d_v
        self._f = f
        self._k = k

    @property
    def u(self) -> np.ndarray:
        """Substanc U

        Returns:
            np.ndarray: Substanc U
        """
        return (self._u - self._u.min()) / (self._u.max() - self._u.min())

    @property
    def v(self) -> np.ndarray:
        """Substanc V

        Returns:
            np.ndarray: Substanc V
        """
        return (self._v - self._v.min()) / (self._v.max() - self._v.min())

    def compute(self):
        """Compute Gray-Scott Model"""
        self._u += (
            self._d_u * ndimage.laplace(self._u)
            - self._u * self._v * self._v
            + self._f * (1 - self._u)
        )
        self._v += (
            self._d_v * ndimage.laplace(self._v)
            + self._u * self._v * self._v
            - (self._f + self._k) * self._v
        )


if __name__ == "__main__":
    gsm = GrayScottModel(100, 100, 0.1, 0.05)

    for i in range(1000):
        gsm.compute()

    plt.imshow(gsm.v, cmap="Greys")
    plt.show()
