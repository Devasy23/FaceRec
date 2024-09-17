from __future__ import annotations

import base64
import io
import json
import os

import cv2
import requests
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import Response as flask_response
from PIL import Image

from FaceRec.config import Config

employee_blueprint = Blueprint(
    'employee_blueprint',
    __name__,
    template_folder='../../templates/',
    static_folder='../../static/',
)

cap = cv2.VideoCapture(0)


# function for displaying live video
def display_live_video():
    """
    Generator for displaying live video from the camera.

    Yields frames as JPEG images.
    """
    while True:
        success, frame = cap.read()  # Read a frame from the camera
        if not success:
            break
        frame = cv2.flip(frame, 1)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes
        if not ret:
            break
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(buffer) + b'\r\n\r\n'
        )


# Route for displaying video
@employee_blueprint.route('/video_feed')
def video_feed():
    """
    Route for displaying live video from the camera.

    Returns a multipart response with a JPEG image for each frame from the camera.

    The `mimetype` parameter is set to `'multipart/x-mixed-replace;boundary=frame'` to
    indicate that the response body contains multiple images, separated by a boundary
    string (`'--frame\r\n'`). The browser will display each image in sequence, creating
    the illusion of a live video feed.
    """

    return flask_response(
        display_live_video(),
        mimetype='multipart/x-mixed-replace;boundary=frame',
    )


# Route for capturing image from video
@employee_blueprint.route('/capture', methods=['GET', 'POST'])
def capture():
    """
    Route for capturing an image from the video feed.

    This route is used to capture a single frame from the video feed and save it to a file.
    The frame is flipped horizontally before saving.

    The image is stored in a file specified by the `Config.image_data_file` variable.

    The response is a redirect to the "Image" route, which displays the captured image.

    The request is expected to be a POST request with the following form data:
        - EmployeeCode: The employee code for the person in the image.
        - Name: The name of the person in the image.
        - gender: The gender of the person in the image.
        - Department: The department of the person in the image.
    """
    global EmployeeCode
    global Name
    global gender
    global Dept
    global encoded_image
    EmployeeCode = request.form.get('EmployeeCode', '')
    Name = request.form.get('Name', '')
    gender = request.form.get('gender', '')
    Dept = request.form.get('Department', '')
    ret, frame = cap.read(True)
    frame = cv2.flip(frame, 1)
    _, buffer = cv2.imencode('.jpg', frame)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    with open(Config.image_data_file, 'w') as file:
        json.dump({'base64_image': encoded_image}, file)
    return redirect('Image')


# Route to display captured image
@employee_blueprint.route('/Image', methods=['GET'])
def display_image():
    """
    Route to display the captured image.

    This route is used to display the most recently captured image in the template.

    The image is read from a file specified by the `Config.image_data_file` variable.

    The most recent image is displayed.

    The image path is passed to the template as a variable named `image_path`.

    Returns:
        A rendered template with the image path.
    """
    if os.path.exists(Config.image_data_file):
        with open(Config.image_data_file) as file:
            image_data = json.load(file)
        encoded_image = image_data.get('base64_image', '')
        decoded_image_data = base64.b64decode(encoded_image)
        image = Image.open(io.BytesIO(decoded_image_data))
        filename = 'final.png'
        image.save(
            os.path.join(
                Config.upload_image_path[0],
                filename,
            ),
            quality=100,
        )
        image = sorted(
            os.listdir(Config.upload_image_path[0]),
            key=lambda x: os.path.getatime(
                os.path.join(Config.upload_image_path[0], x),
            ),
            reverse=True,
        )
    if image:
        recent_image = image[0]
        image_path = os.path.join(Config.upload_image_path[0], recent_image)
    else:
        recent_image = None
    image_path = os.path.join(Config.upload_image_path[0], recent_image)
    print('done')
    return render_template('index.html', image_path=image_path)


# Below route are of Recognition


@employee_blueprint.route('/capturing', methods=['GET', 'POST'])
def capturing():
    """
    This route is used to capture an image from the video feed.

    When the route is accessed, a single frame is read from the video feed
    and saved to a file specified by the `Config.image_data_file` variable.

    The frame is flipped horizontally before saving.

    The response is a redirect to the "Pic" route, which displays the captured
    image.

    The request is expected to be a GET or POST request with no form data.
    """
    ret, frame = cap.read(True)
    frame = cv2.flip(frame, 1)
    _, buffer = cv2.imencode('.jpg', frame)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    with open(Config.image_data_file, 'w') as file:
        json.dump({'base64_image': encoded_image}, file)
    return redirect('Pic')


# Route to display captured image
@employee_blueprint.route('/Pic', methods=['GET', 'POST'])
def display_pic():
    """Route to display the captured image.

    This route reads the image data from a file specified by the
    `Config.image_data_file` variable and displays it in the template.

    The image is saved to a file in the directory specified by the
    `Config.upload_image_path` variable.

    The most recent image is displayed.

    The image is displayed in the template with the name "image_path".

    Returns:
        A rendered template with the image path.

    """
    if os.path.exists(Config.image_data_file):
        with open(Config.image_data_file) as file:
            image_data = json.load(file)
        encoded_image = image_data.get('base64_image', '')
        decoded_image_data = base64.b64decode(encoded_image)
        image = Image.open(io.BytesIO(decoded_image_data))
        filename = 'final.png'
        image.save(
            os.path.join(
                Config.upload_image_path[0],
                filename,
            ),
            quality=100,
        )
        image = sorted(
            os.listdir(Config.upload_image_path[0]),
            key=lambda x: os.path.getatime(
                os.path.join(Config.upload_image_path[0], x),
            ),
            reverse=True,
        )
    if image:
        recent_image = image[0]
        image_path = os.path.join(Config.upload_image_path[0], recent_image)
    else:
        recent_image = None
    image_path = os.path.join(Config.upload_image_path[0], recent_image)
    print('done')
    files = {'Face': open(os.path.join(
        Config.upload_image_path[0], 'final.jpg'), 'rb')}
    try:
        fastapi_url = 'http://127.0.0.1:8000/recognize_face'
        req = requests.post(fastapi_url, files=files)
        data = req.content
        return data
    except Exception as e:
        print('Error:', e)
