# daily-portrait

Automatically align portraits and create a time-lapse video.

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


## How it works

1. Rename each photo by its date in EXIF data. 
   1. If a photo does not have EXIF data, keep its original name.
2. Resize all photos to match the size of the first photo.
3. Align face
   1. Locate the two eyes in the photo.
   2. Find the center point between the two eyes.
   3. Rotate the photo to make the eyes horizontal.
   4. Move the photo to align the center point.
   5. Scale the face based on the distance between the eyes.
4. Crop the face according to the ratio in the settings.
5. Adjust each photo to fit the frame size.
6. Add the date to each photo using the EXIF data. 
   If a photo does not have EXIF data, skip this step.
7. Save each photo to the output directory.
8. Create a video from the photos in the output directory.
