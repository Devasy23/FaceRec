from __future__ import annotations

import base64
import io
import json
import os
import logging

import cv2
import requests
from flask import Blueprint
from flask import Response as flask_response
from flask import jsonify, redirect, render_template, request
from PIL import Image

from FaceRec.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

employee_blueprint = Blueprint(
    "employee_blueprint",
    __name__,
    template_folder="../../templates/",
    static_folder="../../static/",
)

cap = cv2.VideoCapture(0)

# Function for displaying live video
def display_live_video():
    """
    Generator for displaying live video from the camera.

    Yields frames as JPEG images.
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

# Route for displaying video
@employee_blueprint.route("/video_feed")
def video_feed():
    """
    Route for displaying live video from the camera.

    Returns a multipart response with a JPEG image for each frame from the camera.
    """
    return flask_response(
        display_live_video(),
        mimetype="multipart/x-mixed-replace;boundary=frame",
    )

# Route for capturing image from video
@employee_blueprint.route("/capture", methods=["GET", "POST"])
def capture():
    """
    Route for capturing an image from the video feed.

    The captured image is saved to a file specified by the `Config.image_data_file`.
    """
    EmployeeCode = request.form.get("EmployeeCode", "")
    Name = request.form.get("Name", "")
    gender = request.form.get("gender", "")
    Dept = request.form.get("Department", "")
    
    try:
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to capture frame for employee image.")
            return jsonify({"error": "Failed to capture image"}), 500
        
        frame = cv2.flip(frame, 1)
        _, buffer = cv2.imencode(".jpg", frame)
        encoded_image = base64.b64encode(buffer).decode("utf-8")

        with open(Config.image_data_file, "w") as file:
            json.dump({"base64_image": encoded_image}, file)

        logger.info("Image captured and saved successfully.")
        return redirect("Image")

    except Exception as e:
        logger.error(f"Error capturing image: {e}")
        return jsonify({"error": "Error capturing image"}), 500

# Route to display captured image
@employee_blueprint.route("/Image", methods=["GET"])
def display_image():
    """
    Route to display the captured image.

    The image is read from a file specified by the `Config.image_data_file`.
    """
    image_path = None
    if os.path.exists(Config.image_data_file):
        try:
            with open(Config.image_data_file) as file:
                image_data = json.load(file)
            encoded_image = image_data.get("base64_image", "")
            decoded_image_data = base64.b64decode(encoded_image)
            image = Image.open(io.BytesIO(decoded_image_data))
            filename = "final.png"
            image.save(os.path.join(Config.upload_image_path[0], filename), quality=100)

            recent_images = sorted(
                os.listdir(Config.upload_image_path[0]),
                key=lambda x: os.path.getatime(os.path.join(Config.upload_image_path[0], x)),
                reverse=True,
            )
            image_path = os.path.join(Config.upload_image_path[0], recent_images[0]) if recent_images else None
            logger.info("Image displayed successfully.")
        except Exception as e:
            logger.error(f"Error displaying image: {e}")
            return jsonify({"error": "Error displaying image"}), 500
    
    return render_template("index.html", image_path=image_path)

# Route for recognition capturing
@employee_blueprint.route("/capturing", methods=["GET", "POST"])
def capturing():
    """
    This route captures an image from the video feed and saves it.
    """
    try:
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to capture frame during recognition.")
            return jsonify({"error": "Failed to capture image"}), 500

        frame = cv2.flip(frame, 1)
        _, buffer = cv2.imencode(".jpg", frame)
        encoded_image = base64.b64encode(buffer).decode("utf-8")

        with open(Config.image_data_file, "w") as file:
            json.dump({"base64_image": encoded_image}, file)

        logger.info("Recognition image captured successfully.")
        return redirect("Pic")

    except Exception as e:
        logger.error(f"Error capturing recognition image: {e}")
        return jsonify({"error": "Error capturing recognition image"}), 500

# Route to display captured image for recognition
@employee_blueprint.route("/Pic", methods=["GET", "POST"])
def display_pic():
    """Route to display the captured image for recognition."""
    if os.path.exists(Config.image_data_file):
        try:
            with open(Config.image_data_file) as file:
                image_data = json.load(file)
            encoded_image = image_data.get("base64_image", "")
            decoded_image_data = base64.b64decode(encoded_image)
            image = Image.open(io.BytesIO(decoded_image_data))
            filename = "final.png"
            image.save(os.path.join(Config.upload_image_path[0], filename), quality=100)

            recent_images = sorted(
                os.listdir(Config.upload_image_path[0]),
                key=lambda x: os.path.getatime(os.path.join(Config.upload_image_path[0], x)),
                reverse=True,
            )
            image_path = os.path.join(Config.upload_image_path[0], recent_images[0]) if recent_images else None
            
            logger.info("Displaying recognition image.")
            files = {
                "Face": open(os.path.join(Config.upload_image_path[0], "final.png"), "rb"),
            }
            fastapi_url = "http://127.0.0.1:8000/recognize_face"
            req = requests.post(fastapi_url, files=files)
            data = req.content
            return data

        except Exception as e:
            logger.error(f"Error displaying recognition image: {e}")
            return jsonify({"error": "Error displaying recognition image"}), 500

    return jsonify({"error": "No image found"}), 404
