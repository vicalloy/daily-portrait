import contextlib

standard_center_point: tuple[int, int] | None = None
standard_eyes_dist: float | None = None
crop_rate = 0.8
image_pattern = "*.jpeg"
pil_min_filter_size = 0  # odd number, set 0 to no effect
fps = 4
frame_size: tuple[int, int] | None = None

with contextlib.suppress(ImportError):
    from .local_settings import *  # noqa
