import os
import base64
from typing import Optional
from PIL import Image
from io import BytesIO
from shared.constants import MAX_UPLOAD_SIZE, UPLOAD_DIR


class FileHandler:
    @staticmethod
    def save_photo(photo_base64: str, filename: str) -> Optional[str]:
        """
        Saves a base64 encoded photo to the upload directory.

        Args:
            photo_base64: Base64 encoded photo string
            filename: Name to save the file as

        Returns:
            str: Path to the saved file or None if failed
        """
        try:
            # Remove data URI scheme if present
            if "base64," in photo_base64:
                photo_base64 = photo_base64.split("base64,")[1]

            # Decode base64 string
            photo_data = base64.b64decode(photo_base64)

            # Check file size
            if len(photo_data) > MAX_UPLOAD_SIZE:
                raise ValueError("File size exceeds maximum limit")

            # Ensure upload directory exists
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            # Process and optimize image
            img = Image.open(BytesIO(photo_data))
            img.thumbnail((800, 800))  # Resize if too large

            # Save optimized image
            file_path = os.path.join(UPLOAD_DIR, filename)
            img.save(file_path, optimize=True, quality=85)

            return file_path

        except Exception as e:
            print(f"Error saving photo: {str(e)}")
            return None

    @staticmethod
    def load_photo(file_path: str) -> Optional[str]:
        """
        Loads a photo and returns it as base64 encoded string.

        Args:
            file_path: Path to the photo file

        Returns:
            str: Base64 encoded photo or None if failed
        """
        try:
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                return f"data:image/png;base64,{encoded_string}"
        except Exception as e:
            print(f"Error loading photo: {str(e)}")
            return None

    @staticmethod
    def delete_photo(file_path: str) -> bool:
        """
        Deletes a photo file.

        Args:
            file_path: Path to the photo file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting photo: {str(e)}")
            return False
