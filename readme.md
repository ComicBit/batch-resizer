# Face Detection and Alignment Script

## Overview
This Python script automates the processing of a batch of images by detecting faces and ensuring they are correctly aligned (facing the camera). It is designed for applications that require consistent facial orientation in images, such as identity verification systems or profile picture processing. Given a batch of pictures, the script ensures all output images have the subject centered. Photos without a face, not looking at the camera, or with multiple subjects, will be discarded and placed in the `output/trash` folder.

## Features
- **Face Detection**: Uses the `face_recognition` library to identify faces in images.
- **Facial Landmarks Identification**: Detects key facial landmarks to determine face orientation.
- **Orientation Check**: Determines whether the subject is looking directly at the camera.
- **Confidence Scoring**: Provides a confidence score for the face orientation assessment.
- **Image Cropping and Resizing**: Adjusts images based on the position of the detected face, maintaining a specific aspect ratio and size.
- **Batch Processing**: Capable of processing multiple images in various formats (PNG, JPG, JPEG, TIFF, BMP, GIF).
- **Organized Output**: Saves processed images in an `output` folder and moves non-conforming images to `output/trash`.

## Disclaimer
This script is a work in progress and far from perfect. Users should anticipate some inconsistencies and limitations in its current form.

## Known Bugs
1. **Mini Image Saving Issue**: Images with `xxx_mini.jpg` extensions are sporadically saved, although they are meant only for processing and should not be saved.
2. **Skipping/Duplicating Images**: There are instances where pictures are sometimes skipped and sometimes duplicated in the output.
3. **Algorithm Reliability**: The algorithm is not fully reliable, and results should be manually verified for accuracy.

## Requirements
- Python 3.x
- Libraries: `face_recognition`, `PIL` (Pillow), `numpy`, `shutil`, `os`
- You can install them with `pip install -r requirements.txt`

## Usage
1. Place the images you want to process in the `input_folder`.
2. Run the script.
3. Processed images will appear in the `output_folder`. Images not meeting the criteria will be in the `output/trash` folder.

## To-do's
- Merging the script with the duplicates detection.
- Bug-fixing

## License
[MIT License](https://opensource.org/licenses/MIT)

## Author
[Leandro Piccione]
