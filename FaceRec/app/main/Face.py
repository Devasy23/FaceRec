from __future__ import annotations

import base64
import json
import logging
import os

import cv2
import requests
from flask import Blueprint
from flask import Response as flask_response
from flask import redirect, render_template, request

from FaceRec.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Face_Rec_blueprint = Blueprint(
    "Face_Rec_blueprint",
    __name__,
    template_folder="../../templates/",
    static_folder="../../static/",
)

cap = cv2.VideoCapture(0)


def display_live_video():
    """
    Generates a live video stream from the default camera.

    This function yields a sequence of JPEG images from the default camera.
    The images are encoded in a multipart response, with each image separated
    by a boundary string.

    The function breaks out of the loop when the camera is closed or there is
    an error reading from the camera.

    :return: A generator that yields a sequence of JPEG images from the
             default camera.
    """
    while True:
        success, frame = cap.read()  # Read a frame from the camera
        if not success:
            logger.error("Failed to read frame from camera.")
            break
        frame = cv2.flip(frame, 1)
        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            logger.error("Failed to encode frame to JPEG.")
            break
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            bytearray(buffer) + b"\r\n\r\n"
        )


@Face_Rec_blueprint.route("/recognize_employee")
def recognize_employee():
    """
    Route for the employee recognition page.

    This route is used to serve the HTML page for recognizing employees.
    :return: The rendered HTML page for employee recognition.
    """
    return render_template("recognition.html")


@Face_Rec_blueprint.route("/video_feed")
def video_feed():
    """
    Route for displaying live video from the camera.

    The content type of the response is "multipart/x-mixed-replace;boundary=frame".
    :return: The rendered HTML page for displaying live video from the camera.
    """
    return flask_response(
        display_live_video(),
        mimetype="multipart/x-mixed-replace;boundary=frame",
    )


@Face_Rec_blueprint.route("/Recognize", methods=["GET", "POST"])
def recognize():
    """
    Route for recognizing employees from the captured image.

    The server responds with a JSON object containing the name of the
    recognized employee, if any.

    :return: The rendered HTML page for employee recognition with the
             response from the server.
    """
    try:
        # Capture the image file for recognition
        with open("captured_image.jpg", "rb") as img_file:
            files = {"image": (img_file, "image/jpeg")}
            fastapi_url = (
                "http://127.0.0.1:8000/recognize_face"  # Replace with your FastAPI URL
            )
            response = requests.post(fastapi_url, files=files)
            response.raise_for_status()  # Raise an error for bad responses
            logger.info("Recognition request successful.")
            return render_template("recognition.html", response_text=response.text)

    except requests.exceptions.RequestException as e:
        logger.error(f"Recognition request failed: {e}")
        return render_template(
            "recognition.html", response_text="Recognition failed. Please try again."
        )

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return render_template(
            "recognition.html", response_text="An unexpected error occurred."
        )
