from pathlib import Path
from typing import cast

import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageFilter

from daily_portrait import settings
from daily_portrait.utils import get_image_date, get_values
from daily_portrait.utils.alignment import get_eyes_points, move_face, rotation_face


def load_image_as_np(ctx: dict, fn: Path):
    image = face_recognition.load_image_file(fn)
    ctx["image-path"] = fn
    ctx["np-image"] = image
    ctx["height"], ctx["width"] = image.shape[:2]


def resize_and_pad(ctx: dict):
    image, height, width = get_values(ctx, ["np-image", "height", "width"])
    pad_color = (0, 0, 0)
    if "standard_height" not in ctx:
        ctx["standard_height"] = height
        ctx["standard_width"] = width
    standard_height, standard_width = get_values(
        ctx, ["standard_height", "standard_width"]
    )
    if standard_width == width and standard_height == height:
        return

    ctx["height"] = standard_height
    ctx["width"] = standard_width

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
    ctx["np-image"] = scaled_img


def align_face(ctx: dict):
    image, height, width = get_values(ctx, ["np-image", "height", "width"])
    left_eye, right_eye = get_eyes_points(image=image)
    image = rotation_face(left_eye, right_eye, width, height, image)
    image = move_face(left_eye, right_eye, width, height, image)
    ctx["np-image"] = image


def crop_face(ctx: dict):
    crop_rate = settings.crop_rate
    if not crop_rate or crop_rate == 1:
        return
    image, height, width = get_values(ctx, ["np-image", "height", "width"])
    y_cut = int(height * (1 - crop_rate) / 2)
    top = y_cut
    bottom = height - y_cut
    x_cut = int(width * (1 - crop_rate) / 2)
    left = x_cut
    right = width - x_cut
    ctx["np-image"] = image[top:bottom, left:right]
    ctx["height"] = bottom - top
    ctx["width"] = right - left


def add_date(ctx: dict):
    image, height, width, fn = get_values(
        ctx, ["np-image", "height", "width", "image-path"]
    )
    date = get_image_date(fn)
    if not date:
        return
    date = date[:10]
    font_scale = (width + height) / 560.0
    font_size = 0.4 * font_scale
    thickness = round(font_scale) or 1
    cv2.putText(
        image,
        date,
        (width // 15, height * 14 // 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_size,
        (255, 0, 0),
        thickness,
    )


def as_pil_image(ctx: dict):
    image = ctx["np-image"]
    ctx["pil-image"] = Image.fromarray(image.astype("uint8"), "RGB")


def pil_min_filter(ctx: dict):
    if not settings.pil_min_filter_size:
        return
    im = ctx["pil-image"]
    ctx["pil-image"] = im.filter(ImageFilter.MinFilter(settings.pil_min_filter_size))


def save_image(ctx: dict):
    output_dir = cast(Path, ctx["output-dir"])
    image_path = cast(Path, ctx.get("image-path"))
    output_fn = str(output_dir / image_path.name)
    if pil_image := ctx.get("pil-image"):
        pil_image.save(output_fn)
        return
    cv2.imwrite(output_fn, cv2.cvtColor(ctx["np-image"], cv2.COLOR_RGB2BGR))


default_filters = [
    resize_and_pad,
    align_face,
    crop_face,
    add_date,
    as_pil_image,
    pil_min_filter,
]
