import face_recognition
from PIL import Image
import os
import numpy as np
import shutil

def find_faces_and_landmarks(image, scale_factor=3):
    # Resize image for analysis
    small_image = image.resize((int(image.width / scale_factor), int(image.height / scale_factor)))

    # Convert image to RGB if it's not
    if small_image.mode != 'RGB':
        small_image = small_image.convert('RGB')

    small_frame = np.array(small_image)

    # Face detection using 'hog' model
    face_locations = face_recognition.face_locations(small_frame, model="hog")
    if not face_locations:
        return None, None

    # Scale face locations back to original image size
    scaled_face_locations = [(int(top * scale_factor), int(right * scale_factor), int(bottom * scale_factor), int(left * scale_factor)) for top, right, bottom, left in face_locations]

    # Face landmarks detection on original image
    face_landmarks = face_recognition.face_landmarks(np.array(image.convert('RGB')), scaled_face_locations)
    return scaled_face_locations, face_landmarks

def is_looking_at_camera(face_landmarks):
    nose_tip = face_landmarks['nose_tip']
    left_eye = face_landmarks['left_eye']
    right_eye = face_landmarks['right_eye']

    left_eye_center = np.mean(left_eye, axis=0)
    right_eye_center = np.mean(right_eye, axis=0)
    eyes_center = (left_eye_center + right_eye_center) / 2

    is_aligned = left_eye_center[0] < nose_tip[0][0] < right_eye_center[0]
    confidence = abs(eyes_center[0] - nose_tip[0][0]) / (right_eye_center[0] - left_eye_center[0])
    confidence = max(0, 100 - confidence * 100)  # Convert to percentage

    return is_aligned, confidence

def process_image(image_path, output_path, target_size=(768, 1344), scale_factor=3, trash_folder='trash'):
    with Image.open(image_path) as img:
        face_locations, face_landmarks_list = find_faces_and_landmarks(img, scale_factor)

        if not face_locations or not face_landmarks_list:
            shutil.copy2(image_path, os.path.join(trash_folder, os.path.basename(image_path)))
            return

        # Select the main face based on size
        main_face = max(face_locations, key=lambda rect: (rect[2] - rect[0]) * (rect[3] - rect[1]))
        main_face_index = face_locations.index(main_face)
        main_face_landmarks = face_landmarks_list[main_face_index]

        looking_at_camera, confidence = is_looking_at_camera(main_face_landmarks)
        if not looking_at_camera:
            trash_name = f"{int(confidence)}%-{os.path.basename(image_path)}"
            shutil.copy2(image_path, os.path.join(trash_folder, trash_name))
            return

        top, right, bottom, left = main_face

        # Cropping logic
        face_center_x = (left + right) // 2
        face_center_y = (top + bottom) // 2

        target_aspect = target_size[0] / target_size[1]
        img_aspect = img.width / img.height

        if img_aspect > target_aspect:
            # Wider than target: scale height to target, adjust width
            scale = target_size[1] / img.height
            new_width = int(img.width * scale)
            new_height = target_size[1]
        else:
            # Taller than target: scale width to target, adjust height
            scale = target_size[0] / img.width
            new_height = int(img.height * scale)
            new_width = target_size[0]

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Adjust face center based on the scaling
        scaled_face_center_x = int(face_center_x * scale)
        scaled_face_center_y = int(face_center_y * scale)

        # Determine crop coordinates
        left_crop = max(scaled_face_center_x - target_size[0] // 2, 0)
        top_crop = max(scaled_face_center_y - target_size[1] // 2, 0)
        right_crop = min(left_crop + target_size[0], new_width)
        bottom_crop = min(top_crop + target_size[1], new_height)

        img = img.crop((left_crop, top_crop, right_crop, bottom_crop))

        # Convert image to RGB if it's in RGBA
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        img.save(output_path)

input_folder = 'target'
output_folder = 'output'
trash_folder = os.path.join(output_folder, 'trash')

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(trash_folder):
    os.makedirs(trash_folder)

# Process images
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, os.path.basename(filename))
        process_image(input_path, output_path, trash_folder=trash_folder)

print("Image processing complete.")
