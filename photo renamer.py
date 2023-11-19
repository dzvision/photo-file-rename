from PIL import Image
import os
import exifread
from datetime import datetime

def get_exif_date_and_camera(file_path):
    with open(file_path, 'rb') as image_file:
        tags = exifread.process_file(image_file, stop_tag='EXIF DateTimeOriginal')
        if 'EXIF DateTimeOriginal' in tags:
            date_taken = tags['EXIF DateTimeOriginal']
            date_taken = datetime.strptime(str(date_taken), '%Y:%m:%d %H:%M:%S')
        else:
            # Use file creation time if EXIF date is not available
            date_taken = datetime.fromtimestamp(os.path.getctime(file_path))

        # Extract camera make and model information
        camera_make = str(tags.get('Image Make', 'Unknown'))
        camera_model = str(tags.get('Image Model', 'Unknown'))

    return date_taken, camera_make, camera_model

def rename_photos(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(directory, filename)

            date_taken, camera_make, camera_model = get_exif_date_and_camera(file_path)

            # Format the new filename
            new_filename = f"{date_taken.strftime('%Y%m%d_%H%M%S')}_{camera_make}_{camera_model}.jpg"
            new_filepath = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(file_path, new_filepath)
            print(f"Renamed: {filename} to {new_filename}")

if __name__ == "__main__":
    # Replace 'your_directory_path' with the path to your photos directory
    photos_directory = 'X:\\AAA\\photo'
    rename_photos(photos_directory)