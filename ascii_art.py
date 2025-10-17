"""
20251017

Image to ASCII art converter.

"""

import string
from itertools import product

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def min_max_scaling(array: np.ndarray) -> np.ndarray:
    """Min-Max scaling.

    Args:
        array: Array

    Returns:
        Min-Max Scaled array
    """
    min_val = np.min(array)
    max_val = np.max(array)
    return (array - min_val) / (max_val - min_val)


def get_char_size(
    font: ImageFont.ImageFont | ImageFont.FreeTypeFont,
    kerning_offset: int = 0,
    leading_offset: int = 0,
) -> tuple[int, int]:
    """Font character size.

    Args:
        font: Font
        kerning_offset: Font kerning offset
        leading_offset: Font leading offset

    Returns:
        Font character size (width, height)
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    _, _, right, bottom = np.array([font.getbbox(c) for c in chars]).T
    return (np.max(right) + kerning_offset, np.max(bottom) + leading_offset)


def measure_chars(
    chars: str,
    font: ImageFont.ImageFont | ImageFont.FreeTypeFont,
    char_size: tuple[int, int],
    inversion: bool = False,
) -> np.ndarray:
    """Measures characters.

    Args:
        chars: Characters
        font: Font
        char_size: Font character size
        inversion: Measurement inversion.

    Returns:
        Measurement
    """

    def _measure_char(
        char: str,
        font: ImageFont.ImageFont | ImageFont.FreeTypeFont,
        char_size: tuple[int, int],
    ) -> tuple[np.floating, np.floating]:
        image = Image.new("L", char_size)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text=char, fill=255, font=font)
        image_array = np.array(image)
        brightness, contrast = np.mean(image_array), np.std(image_array)
        return brightness, contrast

    measurement = np.array([_measure_char(c, font, char_size) for c in chars]).T
    measurement = measurement if inversion else -measurement
    measurement = np.apply_along_axis(min_max_scaling, 1, measurement)
    return measurement


def ascii_art(
    image: Image.Image,
    font: ImageFont.ImageFont | ImageFont.FreeTypeFont,
    ascii_width: int = 80,
    chars: str = " '.0:HIJLM",
    inversion: bool = False,
    kerning_offset: int = 0,
    leading_offset: int = 0,
    as_image: bool = False,
) -> str | Image.Image:
    """Image to ASCII art converter.

    Args:
        image: Image
        font: Font
        ascii_width: ASCII art width (chars)
        chars: Characters
        inversion: Image inversion.
        kerning_offset: Font kerning offset
        leading_offset: Font leading offset
        as_image: Return image

    Returns:
        ASCII art string / image
    """
    char_size = get_char_size(font, kerning_offset, leading_offset)

    chars_brightness, chars_contrast = measure_chars(
        chars, font, char_size, inversion
    )

    # Brightness as a measure.
    # Can be used contrast, their combinations, or something else.
    chars_vals = chars_brightness

    # Image processing
    image_width, image_height = image.size
    aspect_ratio = char_size[0] / char_size[1]
    ascii_height = np.round(
        image_height * ascii_width / image_width * aspect_ratio
    ).astype(int)
    image_array = np.array(image.resize((ascii_width, ascii_height)))
    scaled = min_max_scaling(image_array)

    # Image representation as a matrix of symbol indices.
    indices = np.abs(
        scaled.reshape(*scaled.shape, 1) - chars_vals.reshape(1, 1, -1)
    ).argmin(axis=2)

    # String output
    if not as_image:
        ascii_art = "\n".join("".join(chars[i] for i in row) for row in indices)
        return ascii_art

    # Image.Image output
    output_image = Image.new(
        "L", (char_size[0] * ascii_width, char_size[1] * ascii_height), 255
    )
    draw = ImageDraw.Draw(output_image)
    for i, j in product(range(ascii_width), range(ascii_height)):
        x, y = char_size[0] * i, char_size[1] * j + leading_offset
        draw.text((x, y), chars[indices[j][i]], 0, font)
    return output_image


if __name__ == "__main__":
    font = ImageFont.truetype(font="Inconsolata-Regular.ttf", size=16)
    image = Image.open("4.1.04.tiff").convert("L")
    chars = string.ascii_letters + string.digits + string.punctuation + " "
    ascii_str = ascii_art(image=image, font=font, chars=chars)
    print(ascii_str)
