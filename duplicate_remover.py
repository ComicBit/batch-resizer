import os
from skimage import io, transform
from skimage.metrics import structural_similarity as ssim
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def find_similar_images(directory, ssim_threshold=0.95, target_size=(128, 128)):
    images = {}
    duplicates = []

    print("Starting image processing...")

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('jpeg', 'jpg', 'png', 'gif')):
                filepath = os.path.join(root, file)
                print(f"Processing {filepath}...")
                image = io.imread(filepath, as_gray=True)
                image = transform.resize(image, target_size, anti_aliasing=True)
                image = image.astype(np.float32) / 255.0

                for stored_path, stored_image in images.items():
                    s = ssim(image, stored_image, data_range=image.max() - image.min())
                    if s > ssim_threshold:
                        duplicates.append((filepath, stored_path))
                        break

                images[filepath] = image

    return duplicates

def delete_images(image_list):
    """Delete the specified images, keeping one from each pair."""
    to_delete = set()
    for img1, img2 in image_list:
        if img1 not in to_delete:
            print(f"Marking for deletion: {img2}")
            to_delete.add(img2)
    for img in to_delete:
        print(f"Deleting image: {img}")
        os.remove(img)

# Replace 'your_directory_path' with the path of the directory you want to check.
directory = '/Users/comicbit/Projects/Stable-Trainings/Resizer/output'
similar_images = find_similar_images(directory)

# Uncomment the line below to delete the similar images after reviewing them.
delete_images(similar_images)

if similar_images:
    print("Found the following similar images:")
    for pair in similar_images:
        print(pair)
else:
    print("No similar images found.")