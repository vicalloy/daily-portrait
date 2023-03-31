from pathlib import Path

from PIL import Image

from daily_portrait import settings


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
