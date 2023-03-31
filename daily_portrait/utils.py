from pathlib import Path

import cv2
from PIL import Image

from daily_portrait import settings


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
        output.absolute(), cv2.VideoWriter_fourcc(*"DIVX"), 1, frame_size
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
    for img_filename in input_dir.glob(settings.image_pattern):
        with Image.open(img_filename) as img:
            frame_size = get_frame_size(frame_size, img.height, img.width)
            img = img.resize(frame_size)
            images.append(img)
    images[0].save(
        output,
        save_all=True,
        append_images=images[1:],
        optimize=True,
        duration=200,
        loop=0,
    )


def rename_photos(images_dir: Path):
    todo_names: list[tuple[Path, Path]] = []
    for img_filename in images_dir.glob(settings.image_pattern):
        with Image.open(img_filename) as img:
            img_exif = img.getexif()
            if img_exif is None:
                continue
            if dt := img_exif.get(306, None):
                new_filename = images_dir / f"{dt}{img_filename.suffix}"
                todo_names.append((img_filename, new_filename))
    for names in todo_names:
        names[0].rename(names[1])
