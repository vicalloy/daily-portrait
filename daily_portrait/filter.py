from pathlib import Path
from typing import cast

import cv2
import face_recognition
from PIL import Image, ImageFilter

from daily_portrait import settings
from daily_portrait.utils import get_image_date, get_values
from daily_portrait.utils.alignment import get_eyes_points, move_face, rotation_face


def load_image_as_np(ctx: dict, fn: Path):
    image = face_recognition.load_image_file(fn)
    ctx["image-path"] = fn
    ctx["np-image"] = image
    ctx["height"], ctx["width"] = image.shape[:2]


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


default_filters = [align_face, crop_face, add_date, as_pil_image, pil_min_filter]
