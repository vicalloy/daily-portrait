from pathlib import Path

from daily_portrait import align_faces

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    align_faces(BASE_DIR / "input", BASE_DIR / "output")
