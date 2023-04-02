from pathlib import Path

import cv2
from PIL import Image

from . import settings


def get_frame_size(
    org_frame_size: tuple[int, int] | None, img_height: int, img_width: int
):
    if org_frame_size is None:
        return img_width, img_height
    if org_frame_size[1] > 0:
        return org_frame_size
    return org_frame_size[0], int(img_height * (org_frame_size[0] / img_width))


def images_to_video(
    input_dir: Path, output: Path, frame_size: tuple[int, int] | None = None
):
    out = cv2.VideoWriter(
        output.absolute(), cv2.VideoWriter_fourcc(*"DIVX"), settings.fps, frame_size
    )
    for img_filename in input_dir.glob(settings.image_pattern):
        img = cv2.imread(img_filename.absolute())
        height, width = img.shape[:2]
        frame_size = get_frame_size(frame_size, height, width)
        img = cv2.resize(img, frame_size)
        out.write(img)
    out.release()


def images_to_gif(
    input_dir: Path, output: Path, frame_size: tuple[int, int] | None = None
):
    images = []
    files = list(input_dir.glob(settings.image_pattern))
    files.sort()
    for img_filename in files:
        with Image.open(img_filename) as img:
            frame_size = get_frame_size(frame_size, img.height, img.width)
            img = img.resize(frame_size)
            images.append(img)
    images[0].save(
        output,
        save_all=True,
        append_images=images[1:],
        optimize=True,
        duration=1000 // settings.fps,
        loop=0,
    )
