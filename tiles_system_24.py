"""
20240505

Tiles system 24

Links:
    https://www.matsys.design/tile-house
"""

import random

import drawsvg as dw

TILES = [
    {"d_path": "", "weight": 1},
    {"d_path": "M 0 0 v 1", "weight": 4},
    {"d_path": "M 0 -1 v 2", "weight": 2},
    # {"d_path": "M 0 -1 v 2 m -1 -1 h 2", "weight": 1},
    {"d_path": "M 0 -1 a 1 1 0 0 0 1 1", "weight": 4},
    {"d_path": "M 0 -1 a 1 1 0 0 0 1 1 m -2 0 a 1 1 0 0 1 1 1", "weight": 2},
    {"d_path": "M 0 1 v -2 m 0 0 a 1 1 0 0 0 1 1", "weight": 8},
]


def tiles_system_24(
    w_tiles_count: int = 16,
    h_tiles_count: int = 16,
    tile_size: int = 32,
    fname: str = "tiles_map.svg",
):
    """TilesSystem24

    Args:
        w_tiles_count (int, optional): Width tiles count. Defaults to 16.
        h_tiles_count (int, optional): Height tiles count. Defaults to 16.
        tile_size (int, optional): Tile size in pixels. Defaults to 32.
        fname (str, optional): Output file name (svg). Defaults to "tiles_map.svg".
    """

    _padding = 30
    d = dw.Drawing(
        tile_size * w_tiles_count + _padding,
        tile_size * h_tiles_count + _padding,
        origin=(-_padding, -_padding),
        id_prefix="pic",
    )

    # Create SVG defs
    defs = []
    for i, tile in enumerate(TILES):
        tile_group = dw.Group(id=str(i))
        # Grid
        tile_group.append(
            dw.Path(
                "M 0 -1 -1 0 0 1 1 0 Z",
                fill="none",
                stroke="black",
                stroke_width=0.05,
                opacity=0.2,
            )
        )
        tile_group.append(
            dw.Path(
                tile["d_path"],
                fill="none",
                stroke="black",
                stroke_width=0.2,
                stroke_linecap="round",
            )
        )
        # Columns
        tile_group.append(dw.Circle(0, -1, 0.1, stroke="none", fill="black"))
        tile_group.append(dw.Circle(0, 1, 0.1, stroke="none", fill="black"))
        tile_group.append(dw.Circle(-1, 0, 0.1, stroke="none", fill="black"))
        tile_group.append(dw.Circle(1, 0, 0.1, stroke="none", fill="black"))
        defs.append(tile_group)

    indexes = [
        (a, b) for b in range(h_tiles_count) for a in range(w_tiles_count)
    ]

    for i, j in indexes:
        tile_index = random.choices(
            range(len(TILES)), [t["weight"] for t in TILES]
        )[0]
        rotation = random.randint(0, 3) * 90
        x_scale = tile_size / 2 * random.choice([-1, 1])
        y_scale = tile_size / 2 * random.choice([-1, 1])
        d.append(
            dw.Use(
                defs[tile_index],
                0,
                0,
                transform=f"translate({tile_size * i},{tile_size * j})scale({x_scale},{y_scale})rotate({rotation})",
            )
        )

    d.save_svg(fname)


if __name__ == "__main__":
    tiles_system_24()
