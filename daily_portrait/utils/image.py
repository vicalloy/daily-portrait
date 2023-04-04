import cv2
import numpy as np


def resize_and_pad(
    image: np.ndarray, height: int, width: int, standard_size: tuple[int, int]
):
    pad_color = (0, 0, 0)
    standard_width, standard_height = standard_size
    if standard_width == width and standard_height == height:
        return image

    # interpolation method
    interp = (
        cv2.INTER_AREA
        if height > standard_height or width > standard_width
        else cv2.INTER_CUBIC
    )

    # aspect ratio of image
    aspect = width / height
    standard_aspect = standard_width / standard_height

    if (standard_aspect > aspect) or (
        (standard_aspect == 1) and (aspect <= 1)
    ):  # new horizontal image
        new_h = standard_height
        new_w = np.round(new_h * aspect).astype(int)
        pad_horz = (standard_width - new_w) / 2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(
            int
        )
        pad_top, pad_bot = 0, 0
    elif (standard_aspect < aspect) or (
        (standard_aspect == 1) and (aspect >= 1)
    ):  # new vertical image
        new_w = standard_width
        new_h = np.round(float(new_w) / aspect).astype(int)
        pad_vert = float(standard_height - new_h) / 2
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0

    # set pad color
    # scale and pad
    scaled_img = cv2.resize(image, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(
        scaled_img,
        pad_top,
        pad_bot,
        pad_left,
        pad_right,
        borderType=cv2.BORDER_CONSTANT,
        value=pad_color,
    )
    return scaled_img
