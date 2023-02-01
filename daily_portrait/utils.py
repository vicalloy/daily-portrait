from pathlib import Path

import cv2


def images_to_video(input_dir: Path, output: Path, frame_size: tuple[int, int]):
    out = cv2.VideoWriter(str(output), cv2.VideoWriter_fourcc(*"DIVX"), 1, frame_size)
    for img_filename in input_dir.glob("*.jpg"):
        img = cv2.imread(str(img_filename))
        img = cv2.resize(img, frame_size)
        out.write(img)
    out.release()
