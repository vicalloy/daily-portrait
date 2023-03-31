import math
from typing import Iterable, TypeAlias

import cv2
import face_recognition
import numpy as np

Point: TypeAlias = tuple[int, int]
standard_center_point: Point | None = None
standard_eyes_dist: float | None = None


def points_center(points: Iterable[Point]) -> Point:
    xs = (e[0] for e in points)
    ys = (e[1] for e in points)
    return sum(xs) // 6, sum(ys) // 6


def angle_between_2_points(p1: Point, p2: Point):
    x1, y1 = p1
    x2, y2 = p2
    tan = (y2 - y1) / (x2 - x1)
    return np.degrees(np.arctan(tan))


def get_rotation_matrix(p1: Point, p2: Point, scale):
    angle = angle_between_2_points(p1, p2)
    center_point = points_center([p1, p2])
    xc, yc = center_point
    print("center:", center_point)
    # TODO calculate scale
    return cv2.getRotationMatrix2D((xc, yc), angle, scale)


def get_eyes_points(image: np.ndarray):
    face_landmarks: np.ndarray = face_recognition.face_landmarks(image)
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


def rotation_face(
    left_eye: Point, right_eye: Point, width: int, height: int, image: np.ndarray
):
    scale = get_scale(left_eye, right_eye)
    matrix = get_rotation_matrix(left_eye, right_eye, scale)
    print("matrix:", matrix)
    return cv2.warpAffine(image, matrix, (width, height), flags=cv2.INTER_CUBIC)


def get_move_vector(left_eye: Point, right_eye: Point):
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


def move_face(
    left_eye: Point, right_eye: Point, width: int, height: int, image: np.ndarray
) -> np.ndarray:
    move_x, move_y = get_move_vector(left_eye, right_eye)
    matrix = np.float32([[1, 0, move_x], [0, 1, move_y]])
    return cv2.warpAffine(image, matrix, (width, height), flags=cv2.INTER_CUBIC)
