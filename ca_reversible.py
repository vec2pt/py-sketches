"""
20251103

Reversible cellular automaton.

"""

import numpy as np
from PIL import Image, ImageOps


def rca(initial: np.ndarray, steps: int = 128, rule: int = 105) -> np.ndarray:
    """Reversible cellular automaton.

    Args:
        initial: Initial state.
        steps: Steps.
        rule: Rule.

    Returns:
        Reversible cellular automaton grid.

    """
    width = len(initial)
    grid = np.zeros((steps + 1, width), dtype=np.uint8)
    grid[1] = initial

    for t in range(2, steps + 1):
        prev = grid[t - 1]
        pattern = (np.roll(prev, 1) << 2) | (prev << 1) | np.roll(prev, -1)
        grid[t] = np.bitwise_xor(((rule >> (7 - pattern)) & 1), grid[t - 2])
    return np.delete(grid, 0, 0)


if __name__ == "__main__":
    size = 128
    rule = 105
    initial_array = np.random.randint(0, 2, size=size, dtype=np.uint8)
    grid = rca(initial=initial_array, steps=size, rule=rule)
    img = Image.fromarray(grid * 255)
    ImageOps.scale(img, 4, Image.Resampling.NEAREST).save("rca.png")
