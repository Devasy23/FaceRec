import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True,
    upload_image_path= os.path.join(basedir, 'static/Images/uploads'),
    ALLOWED_EXTENSIONS = ["jpg","jpeg","png","jfif"],
    image_data_file = os.path.join(basedir, 'static/Images/image_data.json')