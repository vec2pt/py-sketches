"""
20250201

Maze (Origin Shift)

Links:
    https://www.youtube.com/watch?v=zbXKcDVV4G0
"""

from enum import IntEnum
from random import choice

from PIL import Image, ImageDraw


class Direction(IntEnum):
    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __repr__(self) -> str:
        return str(self.value)


class Maze:
    def __init__(self, width: int, height: int) -> None:
        """Maze (Origin Shift)

        Args:
            width (int): Maze width.
            height (int): Maze height.
        """
        self._width = width
        self._height = height
        self._origin_node = (self._height - 1, self._width - 1)

        self._maze = [
            [Direction.EAST for _ in range(self._width - 1)] + [Direction.SOUTH]
            for _ in range(self._height)
        ]

        self._maze[self._origin_node[0]][self._origin_node[1]] = Direction.NONE

    def generate(self, iterations: int | None = None) -> None:
        """Generates a maze.

        Args:
            iterations (int | None, optional): Iterations. Defaults to None.
        """
        if iterations is None:
            iterations = self._width * self._height * 10

        for _ in range(iterations):
            options = [d for d in Direction if d != 0]
            if self._origin_node[0] == 0:
                options.remove(Direction.NORTH)
            elif self._origin_node[0] == self._height - 1:
                options.remove(Direction.SOUTH)
            if self._origin_node[1] == 0:
                options.remove(Direction.WEST)
            elif self._origin_node[1] == self._width - 1:
                options.remove(Direction.EAST)

            node_val = choice(options)
            self._maze[self._origin_node[0]][self._origin_node[1]] = node_val

            if node_val == Direction.NORTH:
                self._origin_node = (
                    self._origin_node[0] - 1,
                    self._origin_node[1],
                )
            elif node_val == Direction.EAST:
                self._origin_node = (
                    self._origin_node[0],
                    self._origin_node[1] + 1,
                )
            elif node_val == Direction.SOUTH:
                self._origin_node = (
                    self._origin_node[0] + 1,
                    self._origin_node[1],
                )
            elif node_val == Direction.WEST:
                self._origin_node = (
                    self._origin_node[0],
                    self._origin_node[1] - 1,
                )
            self._maze[self._origin_node[0]][self._origin_node[1]] = (
                Direction.NONE
            )

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

        for x, y in [
            (i, j) for i in range(self._width) for j in range(self._height)
        ]:
            im_x = x * (path_width + wall_thickness) + wall_thickness
            im_y = y * (path_width + wall_thickness) + wall_thickness
            cell_vec = self._maze[y][x]
            if cell_vec == Direction.NONE:
                draw.rectangle(
                    (
                        (im_x, im_y),
                        (im_x + path_width - 1, im_y + path_width - 1),
                    ),
                    fill=1,
                )
            elif cell_vec == Direction.NORTH:
                draw.rectangle(
                    (
                        (im_x, im_y - wall_thickness),
                        (im_x + path_width - 1, im_y + path_width - 1),
                    ),
                    fill=1,
                )
            elif cell_vec == Direction.EAST:
                draw.rectangle(
                    (
                        (im_x, im_y),
                        (
                            im_x + path_width + wall_thickness - 1,
                            im_y + path_width - 1,
                        ),
                    ),
                    fill=1,
                )
            elif cell_vec == Direction.SOUTH:
                draw.rectangle(
                    (
                        (im_x, im_y),
                        (
                            im_x + path_width - 1,
                            im_y + path_width + wall_thickness - 1,
                        ),
                    ),
                    fill=1,
                )
            elif cell_vec == Direction.WEST:
                draw.rectangle(
                    (
                        (im_x - wall_thickness, im_y),
                        (im_x + path_width - 1, im_y + path_width - 1),
                    ),
                    fill=1,
                )
        return im


if __name__ == "__main__":
    maze = Maze(9, 9)
    maze.generate()
    maze.plot().save("maze_origin_shift.png")
