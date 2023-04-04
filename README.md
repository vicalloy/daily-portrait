# daily-portrait

Auto align portrait and create time lapse video.

## Install

1. `pip install poetry`
2. `poetry install`
3. `poetry shell`

## Usage

1. Put all photos to `./input`
2. Run `cp daily_portrait/local_settings.sample.py daily_portrait/local_settings.py`
3. Modify `daily_portrait/local_settings.py`, if you want change the default settings.
    ```python
    crop_rate = 0.8
    image_pattern = "*.jpeg"
    pil_min_filter_size = 0  # odd number must >=3, set 0 to no effect
    fps = 4
    # (width, height), if width=0, height will auto calculate by width
    frame_size: tuple[int, int] | None = None
    ```
4. Run `python app.py`
   1. processed photos are in `./output`
   2. The output video is `out.gif` and `out.avi`
