from __future__ import annotations

import os

basedir = os.path.abspath(os.path.dirname(__file__))


# This class named Config is likely used for storing configuration settings or parameters in a Python
# program.
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = (True,)
    upload_image_path = (os.path.join(basedir, "static/Images/uploads"),)
    ALLOWED_EXTENSIONS = (["jpg", "jpeg", "png", "jfif"],)
    image_data_file = os.path.join(basedir, "static/Images/image_data.json")
