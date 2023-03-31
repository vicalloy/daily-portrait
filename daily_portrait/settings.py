import contextlib

standard_center_point: tuple[int, int] | None = None
standard_eyes_dist: float | None = None
crop_rate = 0.8
image_pattern = "*.jpeg"

with contextlib.suppress(ImportError):
    from .local_settings import *  # noqa
