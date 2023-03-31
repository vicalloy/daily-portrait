import contextlib

standard_center_point: tuple[int, int] | None = None
standard_eyes_dist: float | None = None
crop_rate = 0.8
image_pattern = "*.jpeg"
pil_min_filter_size = 0  # odd number, set 0 to no effect

with contextlib.suppress(ImportError):
    from .local_settings import *  # noqa
