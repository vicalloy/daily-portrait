import logging
import math
from typing import TypeAlias

import cv2
import face_recognition
import numpy as np

from daily_portrait import settings

Point: TypeAlias = tuple[int, int]
logger = logging.getLogger(__name__)


def points_center(points: list[Point]) -> Point:
    xs = (e[0] for e in points)
    ys = (e[1] for e in points)
    return sum(xs) // len(points), sum(ys) // len(points)


def angle_between_2_points(p1: Point, p2: Point):
    x1, y1 = p1
    x2, y2 = p2
    tan = (y2 - y1) / (x2 - x1)
    return np.degrees(np.arctan(tan))


def get_rotation_matrix(p1: Point, p2: Point, scale):
    angle = angle_between_2_points(p1, p2)
    center_point = points_center([p1, p2])
    xc, yc = center_point
    logger.debug(f"center: {center_point}")
    return cv2.getRotationMatrix2D((xc, yc), angle, scale)


def get_eyes_points(image: np.ndarray):
    face_landmarks: np.ndarray = face_recognition.face_landmarks(image)
    logger.debug(f"find face count: {len(face_landmarks)}")
    assert len(face_landmarks) == 1
    face_landmarks = face_landmarks[0]

    # print(face_landmarks)
    left_eye = points_center(face_landmarks["left_eye"])
    right_eye = points_center(face_landmarks["right_eye"])
    logger.debug(f"eyes: {left_eye} {right_eye}")
    return left_eye, right_eye


def get_scale(left_eye, right_eye):
    dist = math.dist(left_eye, right_eye)
    logger.debug(f"dist: {dist}")
    scale = 1
    if settings.standard_eyes_dist:
        scale = settings.standard_eyes_dist / dist
    else:
        settings.standard_eyes_dist = dist
    return scale


def rotation_face(
    left_eye: Point, right_eye: Point, width: int, height: int, image: np.ndarray
):
    scale = get_scale(left_eye, right_eye)
    matrix = get_rotation_matrix(left_eye, right_eye, scale)
    logger.debug(f"matrix: {matrix}")
    return cv2.warpAffine(image, matrix, (width, height), flags=cv2.INTER_CUBIC)


def get_move_vector(left_eye: Point, right_eye: Point):
    center_point = points_center([left_eye, right_eye])
    logger.debug(f"center: {center_point}")
    move_x, move_y = 0, 0

    if standard_center_point := settings.standard_center_point:
        move_x = standard_center_point[0] - center_point[0]
        move_y = standard_center_point[1] - center_point[1]
    else:
        settings.standard_center_point = center_point
    return move_x, move_y


def move_face(
    left_eye: Point, right_eye: Point, width: int, height: int, image: np.ndarray
) -> np.ndarray:
    move_x, move_y = get_move_vector(left_eye, right_eye)
    matrix = np.float32([[1, 0, move_x], [0, 1, move_y]])
    return cv2.warpAffine(image, matrix, (width, height), flags=cv2.INTER_CUBIC)
