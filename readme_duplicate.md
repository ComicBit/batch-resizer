# Image Similarity Detector and Cleaner

This Python script identifies and optionally deletes similar images in a specified directory, helping to manage and clean up image files.

## Features

- Scans a directory for image files (jpeg, jpg, png, gif).
- Compares images using Structural Similarity Index (SSIM).
- Identifies similar images based on a customizable SSIM threshold.
- Option to automatically delete duplicates, keeping one image from each similar pair.

## Requirements

- Python 3.x
- Libraries: scikit-image, numpy

Install the required libraries using the command: `pip install -r requirements.txt`

## Usage

1. Update the `directory` variable in the script with the path to your image directory.
2. Run the script to find similar images. Review the list of similar images.
3. If you want to delete duplicates, uncomment the line calling `delete_images(similar_images)` and run the script again.

## Caution

- Use the delete function with caution. It's recommended to backup your images before running the deletion process.
- Review the list of similar images before deleting.

## License

This script is released under the MIT License.
