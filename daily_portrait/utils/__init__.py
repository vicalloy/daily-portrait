from pathlib import Path
from typing import Iterable

from PIL import Image

from daily_portrait import settings


def get_values(ctx: dict, keys: Iterable):
    return (ctx[e] for e in keys)


def get_image_date(fn: Path) -> str | None:
    with Image.open(fn) as img:
        img_exif = img.getexif()
        if img_exif is None:
            return None
        if dt := img_exif.get(306, None):
            return dt
    return None


def rename_photos(images_dir: Path):
    todo_names: list[tuple[Path, Path]] = []
    for img_filename in images_dir.glob(settings.image_pattern):
        if dt := get_image_date(img_filename):
            new_filename = images_dir / f"{dt}{img_filename.suffix}"
            todo_names.append((img_filename, new_filename))
    for names in todo_names:
        names[0].rename(names[1])
