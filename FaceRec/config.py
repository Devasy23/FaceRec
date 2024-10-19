from __future__ import annotations

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# This class named Config is likely used for storing configuration settings or parameters in a Python program.
class Config:
    try:
        SECRET_KEY = os.environ.get("SECRET_KEY")
    except Exception as e:
        print(f"Error retrieving SECRET_KEY from environment: {e}")
        SECRET_KEY = None  # Default to None or handle it as needed

    DEBUG = True  # Assuming DEBUG should be a boolean, not a tuple
    try:
        upload_image_path = os.path.join(basedir, "static/Images/uploads")
    except Exception as e:
        print(f"Error setting upload_image_path: {e}")
        upload_image_path = None  # Default to None or handle it as needed

    ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "jfif"]  # Use a list, not a tuple with a list inside
    try:
        image_data_file = os.path.join(basedir, "static/Images/image_data.json")
    except Exception as e:
        print(f"Error setting image_data_file path: {e}")
        image_data_file = None  # Default to None or handle it as needed
