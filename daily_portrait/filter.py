from pathlib import Path
from typing import Iterable, cast

import cv2
import face_recognition
from PIL import Image

from daily_portrait.alignment import get_eyes_points, move_face, rotation_face


def load_image_as_np(ctx: dict, fn: Path):
    image = face_recognition.load_image_file(fn)
    ctx["image-path"] = fn
    ctx["np-image"] = image
    ctx["height"], ctx["width"] = image.shape[:2]


def get_values(ctx: dict, keys: Iterable):
    return (ctx[e] for e in keys)


def align_face(ctx: dict):
    image, height, width = get_values(ctx, ["np-image", "height", "width"])
    left_eye, right_eye = get_eyes_points(image=image)
    image = rotation_face(left_eye, right_eye, width, height, image)
    left_eye, right_eye = get_eyes_points(image=image)
    image = move_face(left_eye, right_eye, width, height, image)
    ctx["np-image"] = image


def crop_face(ctx: dict):
    crop_rate = 0.8
    image, height, width = get_values(ctx, ["np-image", "height", "width"])
    y_cut = int(height * (1 - crop_rate) / 2)
    top = y_cut
    bottom = height - y_cut
    x_cut = int(width * (1 - crop_rate) / 2)
    left = x_cut
    right = width - x_cut
    ctx["np-image"] = image[top:bottom, left:right]


def as_pil_image(ctx: dict):
    image = ctx["np-image"]
    ctx["pil-image"] = Image.fromarray(image.astype("uint8"), "RGB")


def save_image(ctx: dict):
    output_dir = cast(Path, ctx["output-dir"])
    image_path = cast(Path, ctx.get("image-path"))
    output_fn = str(output_dir / image_path.name)
    if pil_image := ctx.get("pil-image"):
        pil_image.save(output_fn)
        return
    cv2.imwrite(output_fn, cv2.cvtColor(ctx["np-image"], cv2.COLOR_RGB2BGR))


default_filters = [align_face, crop_face, as_pil_image]
