# flake8: noqa
from pathlib import Path
from typing import Iterable, Callable

from daily_portrait import settings
from daily_portrait.filter import load_image_as_np, default_filters, save_image
from daily_portrait.utils import list_images


def process_images(
    input_dir: Path, output_dir: Path, filters: Iterable[Callable] = default_filters
):
    ctx = {"output-dir": output_dir}
    for img in list_images(input_dir):
        load_image_as_np(ctx, img)
        for func in filters:
            func(ctx)
        save_image(ctx)
