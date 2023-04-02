import logging
from pathlib import Path

from daily_portrait import process_images
from daily_portrait.utils import rename_photos
from daily_portrait.video import images_to_gif, images_to_video


def config_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s",
        handlers=[logging.StreamHandler()],
    )


if __name__ == "__main__":
    config_logging()
    BASE_DIR = Path(__file__).resolve().parent
    rename_photos(BASE_DIR / "input")
    print("rename photos finished")
    process_images(BASE_DIR / "input", BASE_DIR / "output")
    print("process photos finished")
    images_to_gif(BASE_DIR / "output", BASE_DIR / "out.gif")
    print("gif created")
    images_to_video(BASE_DIR / "output", BASE_DIR / "out.avi")
    print("video created")
