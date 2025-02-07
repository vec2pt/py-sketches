"""
20250206

Meze (Kruskal's algorithm)

Links:
    https://en.wikipedia.org/wiki/Maze_generation_algorithm#Iterative_randomized_Kruskal's_algorithm_(with_sets)
"""

from dataclasses import dataclass
from itertools import product
from random import shuffle

from PIL import Image, ImageDraw


@dataclass
class Cell:
    coords: tuple[int, int]
    group: int


@dataclass
class Wall:
    from_cell: tuple[int, int]
    to_cell: tuple[int, int]
    opening: bool = False


class Maze:
    def __init__(self, width: int, height: int) -> None:
        """Maze (Kruskal's algorithm)

        Args:
            width (int): Maze width.
            height (int): Maze height.
        """
        self._width = width
        self._height = height
        self._cells = {
            coords: Cell(coords, i)
            for i, coords in enumerate(
                product(range(self._width), range(self._height))
            )
        }
        self._walls = [
            Wall((i, k), (j, k))
            for i, j in zip(range(self._width - 1), range(1, self._width))
            for k in range(self._height)
        ] + [
            Wall((k, i), (k, j))
            for i, j in zip(range(self._height - 1), range(1, self._height))
            for k in range(self._width)
        ]
        shuffle(self._walls)

    def generate(self) -> None:
        """Generates a maze."""
        for wall in self._walls:
            from_cell = self._cells[wall.from_cell]
            to_cell = self._cells[wall.to_cell]
            if from_cell.group != to_cell.group:
                wall.opening = True
                group_min = min(to_cell.group, from_cell.group)
                group_max = max(to_cell.group, from_cell.group)
                for cell in self._cells.values():
                    if cell.group == group_max:
                        cell.group = group_min

    def plot(
        self, path_width: int = 32, wall_thickness: int = 8
    ) -> Image.Image:
        """Creates an image of a maze.

        Args:
            path_width (int, optional): Path width. Defaults to 32.
            wall_thickness (int, optional): Wall thickness. Defaults to 8.

        Returns:
            Image.Image: Maze image.
        """
        im = Image.new(
            "1",
            (
                self._width * (path_width + wall_thickness) + wall_thickness,
                self._height * (path_width + wall_thickness) + wall_thickness,
            ),
        )
        draw = ImageDraw.Draw(im)
        for cell in self._cells.values():
            im_x = (
                cell.coords[0] * (path_width + wall_thickness) + wall_thickness
            )
            im_y = (
                cell.coords[1] * (path_width + wall_thickness) + wall_thickness
            )
            draw.rectangle(
                (
                    (im_x, im_y),
                    (im_x + path_width - 1, im_y + path_width - 1),
                ),
                fill=1,
            )

        for wall in self._walls:
            if not wall.opening:
                continue

            if wall.from_cell[0] == wall.to_cell[0]:
                im_x = (
                    wall.from_cell[0] * (path_width + wall_thickness)
                    + wall_thickness
                )
                im_y = (wall.from_cell[1] + 1) * (path_width + wall_thickness)
                draw.rectangle(
                    (
                        (im_x, im_y),
                        (im_x + path_width - 1, im_y + wall_thickness - 1),
                    ),
                    fill=1,
                )
            elif wall.from_cell[1] == wall.to_cell[1]:
                im_x = (wall.from_cell[0] + 1) * (path_width + wall_thickness)
                im_y = (
                    wall.from_cell[1] * (path_width + wall_thickness)
                    + wall_thickness
                )
                draw.rectangle(
                    (
                        (im_x, im_y),
                        (im_x + wall_thickness - 1, im_y + path_width - 1),
                    ),
                    fill=1,
                )
        return im


if __name__ == "__main__":
    maze = Maze(width=9, height=9)
    maze.generate()
    maze.plot().save("maze_kruskals.png")
