import math
from pathlib import Path

import cv2
import face_recognition
import numpy as np

standard_center_point: tuple[int, int] | None = None
standard_eyes_dist: float | None = None


def points_center(points):
    xs = (e[0] for e in points)
    ys = (e[1] for e in points)
    return sum(xs) // 6, sum(ys) // 6


def angle_between_2_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    tan = (y2 - y1) / (x2 - x1)
    return np.degrees(np.arctan(tan))


def get_rotation_matrix(p1, p2, scale):
    angle = angle_between_2_points(p1, p2)
    center_point = points_center([p1, p2])
    xc, yc = center_point
    print("center:", center_point)
    # TODO calculate scale
    return cv2.getRotationMatrix2D((xc, yc), angle, scale)


def get_eyes_points(image):
    face_landmarks = face_recognition.face_landmarks(image)
    print("find face count:", len(face_landmarks))
    assert len(face_landmarks) == 1
    face_landmarks = face_landmarks[0]

    # print(face_landmarks)
    left_eye = points_center(face_landmarks["left_eye"])
    right_eye = points_center(face_landmarks["right_eye"])
    print("eyes:", left_eye, right_eye)
    return left_eye, right_eye


def get_scale(left_eye, right_eye):
    dist = math.dist(left_eye, right_eye)
    print("dist:", dist)
    scale = 1
    global standard_eyes_dist
    if standard_eyes_dist:
        scale = standard_eyes_dist / dist
    else:
        standard_eyes_dist = dist
    return scale


def rotation_face(left_eye, right_eye, width, height, image):
    scale = get_scale(left_eye, right_eye)
    matrix = get_rotation_matrix(left_eye, right_eye, scale)
    print("matrix:", matrix)
    return cv2.warpAffine(image, matrix, (width, height), flags=cv2.INTER_CUBIC)


def get_move_vector(left_eye, right_eye):
    global standard_center_point
    center_point = points_center([left_eye, right_eye])
    print("center:", center_point)
    move_x, move_y = 0, 0
    if standard_center_point:
        move_x = standard_center_point[0] - center_point[0]
        move_y = standard_center_point[1] - center_point[1]
    else:
        standard_center_point = center_point
    return move_x, move_y


def move_face(left_eye, right_eye, width, height, image):
    move_x, move_y = get_move_vector(left_eye, right_eye)
    matrix = np.float32([[1, 0, move_x], [0, 1, move_y]])
    return cv2.warpAffine(image, matrix, (width, height), flags=cv2.INTER_CUBIC)


def crop_image(image, crop_rate):
    height, width = image.shape[:2]
    y_cut = int(height * (1 - crop_rate) / 2)
    top = y_cut
    bottom = height - y_cut
    x_cut = int(width * (1 - crop_rate) / 2)
    left = x_cut
    right = width - x_cut
    return image[top:bottom, left:right]


def align_face(image_path: Path, output_dir: Path, crop_rate=0.8):
    image = face_recognition.load_image_file(image_path)
    height, width = image.shape[:2]

    left_eye, right_eye = get_eyes_points(image=image)
    image = rotation_face(left_eye, right_eye, width, height, image)

    left_eye, right_eye = get_eyes_points(image=image)
    image = move_face(left_eye, right_eye, width, height, image)
    image = crop_image(image=image, crop_rate=crop_rate)
    cv2.imwrite(
        str(output_dir / image_path.name), cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    )


def align_faces(input_dir: Path, output_dir: Path):
    for img in input_dir.glob("*.jpeg"):
        align_face(img, output_dir)
