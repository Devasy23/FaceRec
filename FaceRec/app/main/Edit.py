from __future__ import annotations

import base64
import io
import json
import os

import cv2
import requests
from flask import Blueprint, Response as flask_response, redirect, render_template, request, g, flash
from PIL import Image
from FaceRec.config import Config

Edit_blueprint = Blueprint(
    "Edit_blueprint",
    __name__,
    template_folder="../../templates/",
    static_folder="../../static/",
)

# Global variable for video capture
cap = cv2.VideoCapture(0)

def initialize_camera():
    """Initialize the camera resource if it's not already opened."""
    global cap
    if not cap.isOpened():
        cap.open(0)


def release_camera():
    """Release the camera resource when no longer needed."""
    global cap
    if cap.isOpened():
        cap.release()


def validate_input(data: dict) -> bool:
    """Validates the input form data."""
    if not data.get("EmployeeCode").isdigit():
        flash("Invalid EmployeeCode. It should be numeric.")
        return False
    if not data.get("Name"):
        flash("Name cannot be empty.")
        return False
    if not data.get("gender"):
        flash("Gender cannot be empty.")
        return False
    if not data.get("Department"):
        flash("Department cannot be empty.")
        return False
    return True


def display_live_video():
    """Generator for displaying live video from the camera."""
    initialize_camera()  # Ensure camera is initialized
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            break
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n\r\n"
        )


@Edit_blueprint.route("/video_feed")
def video_feed():
    """Route for displaying live video from the camera."""
    return flask_response(
        display_live_video(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@Edit_blueprint.route("/capture", methods=["POST"])
def capture():
    """Route for capturing an image from the video feed."""
    form_data = {
        "EmployeeCode": request.form.get("EmployeeCode", ""),
        "Name": request.form.get("Name", ""),
        "gender": request.form.get("gender", ""),
        "Department": request.form.get("Department", "")
    }

    if not validate_input(form_data):
        return redirect("capture")

    try:
        initialize_camera()  # Ensure camera is initialized
        ret, frame = cap.read()
        if not ret:
            flash("Failed to capture the image.")
            return redirect("capture")

        frame = cv2.flip(frame, 1)
        _, buffer = cv2.imencode(".jpg", frame)
        encoded_image = base64.b64encode(buffer).decode("utf-8")
        
        g.employee_data = form_data
        g.encoded_image = encoded_image

        with open(Config.image_data_file, "w") as file:
            json.dump({"base64_image": encoded_image}, file)
    except Exception as e:
        flash(f"Error capturing image: {e}")
        return redirect("capture")

    return redirect("Image")


@Edit_blueprint.route("/Image", methods=["GET"])
def display_image():
    """Route to display the captured image."""
    try:
        if os.path.exists(Config.image_data_file):
            with open(Config.image_data_file) as file:
                image_data = json.load(file)
            
            encoded_image = image_data.get("base64_image", "")
            decoded_image_data = base64.b64decode(encoded_image)
            image = Image.open(io.BytesIO(decoded_image_data))

            filename = "final.png"
            image.save(os.path.join(Config.upload_image_path[0], filename), quality=100)

            image_files = sorted(
                os.listdir(Config.upload_image_path[0]),
                key=lambda x: os.path.getatime(os.path.join(Config.upload_image_path[0], x)),
                reverse=True
            )
            recent_image = image_files[0] if image_files else None
        else:
            recent_image = None
    except Exception as e:
        flash(f"Error loading image: {e}")
        return render_template("index.html", image_path=None)

    image_path = os.path.join(Config.upload_image_path[0], recent_image) if recent_image else None
    return render_template("index.html", image_path=image_path)


@Edit_blueprint.route("/edit/<int:EmployeeCode>", methods=["POST", "GET"])
def edit(EmployeeCode):
    """Edit an existing employee."""
    if request.method == "POST":
        form_data = {
            "Name": request.form["Name"],
            "gender": request.form["Gender"],
            "Department": request.form["Department"]
        }

        if not validate_input(form_data):
            return redirect(f"/edit/{EmployeeCode}")

        try:
            with open(Config.image_data_file) as file:
                image_data = json.load(file)

            encoded_image = image_data.get("base64_image", "")
            payload = {**form_data, "Image": encoded_image}

            response = requests.put(f"http://127.0.0.1:8000/update/{EmployeeCode}", json=payload)
            if response.status_code != 200:
                flash(f"Failed to update employee: {response.status_code}")
            return redirect("/")
        except requests.exceptions.RequestException as e:
            flash(f"Request failed: {e}")
            return redirect(f"/edit/{EmployeeCode}")

    try:
        response = requests.get(f"http://127.0.0.1:8000/read/{EmployeeCode}")
        if response.status_code == 200:
            employee_data = response.json()
            return render_template("edit.html", employee_data=employee_data)
        else:
            flash(f"Error {response.status_code}: Failed to retrieve employee data.")
            return render_template("edit.html", employee_data=None)
    except requests.exceptions.RequestException as e:
        flash(f"Error fetching employee data: {e}")
        return render_template("edit.html", employee_data=None)

