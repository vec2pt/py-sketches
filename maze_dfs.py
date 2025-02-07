"""
20250201

Maze (Depth-first search)

Links:
    https://www.youtube.com/watch?v=zbXKcDVV4G0
"""

from dataclasses import dataclass
from enum import IntEnum
from itertools import product
from random import randint

from PIL import Image, ImageDraw


class Direction(IntEnum):
    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __repr__(self) -> str:
        return str(self.value)


@dataclass
class Cell:
    coords: tuple[int, int]
    direction: Direction = Direction.NONE
    visited: bool = False


class Maze:
    def __init__(self, width: int, height: int) -> None:
        """Maze (Depth-first search)

        Args:
            width (int): Maze width.
            height (int): Maze height.
        """
        self._width = width
        self._height = height
        self._cells = {
            coords: Cell(coords)
            for coords in product(range(self._width), range(self._height))
        }
        self._current_cell = self._cells[(0, 0)]
        self._current_cell.visited = True
        self._stack = [self._current_cell]

    def _get_neighbor(self, cell: Cell) -> Cell | None:
        neighbors = []
        directions = []

        x, y = cell.coords
        for coords, direction in zip(
            [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)],
            [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST],
        ):
            neighbor = self._cells.get(coords, None)
            if neighbor and not neighbor.visited:
                neighbors.append(neighbor)
                directions.append(direction)
        if neighbors:
            neighbor_index = randint(0, len(neighbors) - 1)
            neighbor = neighbors[neighbor_index]
            cell.direction += directions[neighbor_index]
            return neighbor

    def generate(self) -> None:
        """Generates a maze."""
        while len(self._stack) != 0:
            self._current_cell = self._stack[-1]
            self._stack.pop(-1)
            neighbor = self._get_neighbor(self._current_cell)
            if neighbor:
                self._stack.append(self._current_cell)
                neighbor.visited = True
                self._stack.append(neighbor)

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
            if not cell.visited:
                continue
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
            if cell.direction & Direction.NORTH:
                draw.rectangle(
                    (
                        (im_x, im_y - wall_thickness),
                        (im_x + path_width - 1, im_y - 1),
                    ),
                    fill=1,
                )
            if cell.direction & Direction.EAST:
                draw.rectangle(
                    (
                        (im_x + path_width, im_y),
                        (
                            im_x + path_width + wall_thickness - 1,
                            im_y + path_width - 1,
                        ),
                    ),
                    fill=1,
                )
            if cell.direction & Direction.SOUTH:
                draw.rectangle(
                    (
                        (im_x, im_y + path_width),
                        (
                            im_x + path_width - 1,
                            im_y + path_width + wall_thickness - 1,
                        ),
                    ),
                    fill=1,
                )
            if cell.direction & Direction.WEST:
                draw.rectangle(
                    (
                        (im_x - wall_thickness, im_y),
                        (im_x - 1, im_y + path_width - 1),
                    ),
                    fill=1,
                )
        return im


if __name__ == "__main__":
    maze = Maze(width=9, height=9)
    maze.generate()
    maze.plot().save("maze_dfs.png")
