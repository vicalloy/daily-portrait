from pathlib import Path

from daily_portrait import align_faces
from daily_portrait.utils import images_to_gif, rename_photos

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    rename_photos(BASE_DIR / "input")
    align_faces(BASE_DIR / "input", BASE_DIR / "output")
    images_to_gif(BASE_DIR / "output", BASE_DIR / "p.gif")
