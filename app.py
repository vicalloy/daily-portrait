import logging
from pathlib import Path

from daily_portrait import process_images
from daily_portrait.utils import images_to_gif, rename_photos


def config_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s",
        handlers=[logging.StreamHandler()],
    )


if __name__ == "__main__":
    config_logging()
    BASE_DIR = Path(__file__).resolve().parent
    rename_photos(BASE_DIR / "input")
    process_images(BASE_DIR / "input", BASE_DIR / "output")
    images_to_gif(BASE_DIR / "output", BASE_DIR / "p.gif")
