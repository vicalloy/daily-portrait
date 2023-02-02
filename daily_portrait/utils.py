from pathlib import Path

import cv2
from PIL import Image


def images_to_video(input_dir: Path, output: Path, frame_size: tuple[int, int]):
    out = cv2.VideoWriter(str(output), cv2.VideoWriter_fourcc(*"DIVX"), 1, frame_size)
    for img_filename in input_dir.glob("*.jpg"):
        img = cv2.imread(str(img_filename))
        img = cv2.resize(img, frame_size)
        out.write(img)
    out.release()


def images_to_gif(input_dir: Path, output: Path, frame_size: tuple[int, int]):
    images = []
    for img_filename in input_dir.glob("*.jpg"):
        with Image.open(img_filename) as img:
            img = img.resize(frame_size)
            images.append(img)
    images[0].save(
        str(output),
        save_all=True,
        append_images=images[1:],
        optimize=True,
        duration=200,
        loop=0,
    )
