# daily-portrait

Auto align portrait and create time lapse video.

## Install

1. `pip install poetry`
2. `poetry install`
3. `poetry shell`

## Usage

1. Put all photo to `./input`
2. Run `cp daily_portrait/local_settings.sample.py daily_portrait/local_settings.py`
3. Modify `daily_portrait/local_settings.py`, if you want change the default settings.
4. Run `python app.py`
   1. processed photos in `./output`
   2. The output video is `out.gif` and `out.avi`
