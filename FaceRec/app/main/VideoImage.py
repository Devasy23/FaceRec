import base64
import io
import json
import os

import cv2
from flask import Blueprint
from flask import Response as flask_response
from flask import redirect, render_template, request
from PIL import Image

from FaceRec.config import Config

employee_blueprint = Blueprint(
    "employee_blueprint",
    __name__,
    template_folder="../../templates/",
    static_folder="../../static/",
)

cap = cv2.VideoCapture(0)


# function for displaying live video
def display_live_video():
    while True:
        success, frame = cap.read()  # Read a frame from the camera
        if not success:
            break
        frame = cv2.flip(frame, 1)
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes
        if not ret:
            break
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + bytearray(buffer) + b"\r\n\r\n"
        )


# Route for displaying video
@employee_blueprint.route("/video_feed")
def video_feed():
    return flask_response(
        display_live_video(), mimetype="multipart/x-mixed-replace;boundary=frame"
    )


# Route for capturing image from video
@employee_blueprint.route("/capture", methods=["GET", "POST"])
def capture():
    global EmployeeCode
    global Name
    global gender
    global Dept
    global encoded_image
    EmployeeCode = request.form.get("EmployeeCode", "")
    Name = request.form.get("Name", "")
    gender = request.form.get("gender", "")
    Dept = request.form.get("Department", "")
    ret, frame = cap.read(True)
    frame = cv2.flip(frame, 1)
    _, buffer = cv2.imencode(".jpg", frame)
    encoded_image = base64.b64encode(buffer).decode("utf-8")
    with open(Config.image_data_file, "w") as file:
        json.dump({"base64_image": encoded_image}, file)
    return redirect("Image")


# Route to display captured image
@employee_blueprint.route("/Image", methods=["GET"])
def display_image():
    if os.path.exists(Config.image_data_file):
        with open(Config.image_data_file, "r") as file:
            image_data = json.load(file)
        encoded_image = image_data.get("base64_image", "")
        decoded_image_data = base64.b64decode(encoded_image)
        image = Image.open(io.BytesIO(decoded_image_data))
        filename = "final.png"
        image.save(os.path.join(Config.upload_image_path[0], filename), quality=100)
        image = sorted(
            os.listdir(Config.upload_image_path[0]),
            key=lambda x: os.path.getatime(
                os.path.join(Config.upload_image_path[0], x)
            ),
            reverse=True,
        )
    if image:
        recent_image = image[0]
        image_path = os.path.join(Config.upload_image_path[0], recent_image)
    else:
        recent_image = None
    image_path = os.path.join(Config.upload_image_path[0], recent_image)
    print("done")
    return render_template("index.html", image_path=image_path)
