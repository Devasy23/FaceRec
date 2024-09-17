from __future__ import annotations

import base64
import io
import json
import os

import cv2
import requests
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import Response as flask_response
from PIL import Image

from FaceRec.config import Config

Face_Rec_blueprint = Blueprint(
    'Face_Rec_blueprint',
    __name__,
    template_folder='../../templates/',
    static_folder='../../static/',
)
cap = cv2.VideoCapture(0)


def display_live_video():
    """
    Generates a live video stream from the default camera.

    This function yields a sequence of JPEG images from the default camera.
    The images are encoded in a multipart response, with each image separated
    by a boundary string.

    The function is designed to be used with the Flask Response object, which
    handles the details of the HTTP response. The caller should use the
    Response object to set the content type to "multipart/x-mixed-replace" and
    then yield from this function.

    The function breaks out of the loop when the camera is closed or there is
    an error reading from the camera.

    :return: A generator that yields a sequence of JPEG images from the
             default camera.
    """
    while True:
        success, frame = cap.read(True)  # Read a frame from the camera
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


@Face_Rec_blueprint.route('/recognize_employee')
def recognize_employee():
    """
    Route for the employee recognition page.

    This route is used to serve the HTML page for recognizing employees.

    The page contains a live video feed from the default camera and a button
    to capture a frame from the video feed and send it to the server for
    recognition.

    The page uses JavaScript to display the video feed and send the request
    to the server.

    The server responds with a JSON object containing the name of the
    recognized employee, if any.

    :return: The rendered HTML page for employee recognition.
    """
    return render_template('recognition.html')


@Face_Rec_blueprint.route('/video_feed')
def video_feed():
    """
    Route for displaying live video from the camera.

    This route is used to display a live video feed from the default camera.

    The video feed is a multipart response with a sequence of JPEG images,
    each separated by a boundary string.

    The content type of the response is "multipart/x-mixed-replace;boundary=frame".

    :return: The rendered HTML page for displaying live video from the camera.
    """
    return flask_response(
        display_live_video(), mimetype='multipart/x-mixed-replace;boundary=frame',
    )


@Face_Rec_blueprint.route('/Recognize', methods=['GET', 'POST'])
def recognize():
    """
    Route for recognizing employees from the captured image.

    This route is used to recognize employees from the captured image.

    The route is a POST request with the following form data:
        - image: The captured image of the employee.

    The server responds with a JSON object containing the name of the
    recognized employee, if any.

    :return: The rendered HTML page for employee recognition with the
             response from the server.
    """
    files = {'image': (open(f"captured_image.jpg", 'rb'), 'image/jpeg')}
    fastapi_url = (
        'http://127.0.0.1:8000/recognize_face'  # Replace with your FastAPI URL
    )
    response = requests.post(fastapi_url, files=files)
    return render_template('recognition.html', response_text=response.text)
