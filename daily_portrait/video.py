from pathlib import Path

import cv2
from PIL import Image

from . import settings


def images_to_video(input_dir: Path, output: Path):
    files = sorted(input_dir.glob(settings.image_pattern))
    out = None
    for img_filename in files:
        img = cv2.imread(str(img_filename))
        if out is None:
            frame_size = list(reversed(img.shape[:2]))
            out = cv2.VideoWriter(
                str(output), cv2.VideoWriter_fourcc(*"MJPG"), settings.fps, frame_size
            )
        out.write(img)
    assert out is not None
    out.release()


def images_to_gif(input_dir: Path, output: Path):
    files = sorted(input_dir.glob(settings.image_pattern))
    images = [Image.open(img_filename) for img_filename in files]
    images[0].save(
        output,
        save_all=True,
        append_images=images[1:],
        optimize=True,
        duration=1000 // settings.fps,
        loop=0,
    )
