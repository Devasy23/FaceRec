from __future__ import annotations

import base64
import io
import json
import os

import cv2
import requests
from flask import Blueprint
from flask import Response as flask_response
from flask import redirect, render_template, request
from PIL import Image

from FaceRec.config import Config

Edit_blueprint = Blueprint(
    "Edit_blueprint",
    __name__,
    template_folder="../../templates/",
    static_folder="../../static/",
)

cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video capture.")
    # You can raise an exception or handle it as needed


# Function for displaying live video
def display_live_video():
    """
    Generator for displaying live video from the camera.

    Yields frames as JPEG images.
    """
    while True:
        success, frame = cap.read()  # Read a frame from the camera
        if not success:
            print("Error: Failed to capture image.")
            break
        frame = cv2.flip(frame, 1)
        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            print("Error: Failed to encode image.")
            break
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            bytearray(buffer) + b"\r\n\r\n"
        )


# Route for displaying video
@Edit_blueprint.route("/video_feed")
def video_feed():
    """Route for displaying live video from the camera.

    Returns a multipart response with a JPEG image for each frame from the camera.
    """
    return flask_response(
        display_live_video(),
        mimetype="multipart/x-mixed-replace;boundary=frame",
    )


# Route for capturing image from video
@Edit_blueprint.route("/capture", methods=["GET", "POST"])
def capture():
    """Route for capturing an image from the video feed.

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

    EmployeeCode = request.form.get("EmployeeCode", "")
    Name = request.form.get("Name", "")
    gender = request.form.get("gender", "")
    Dept = request.form.get("Department", "")

    try:
        ret, frame = cap.read(True)
        if not ret:
            print("Error: Could not read frame from camera.")
            return redirect("Image")  # or handle error appropriately

        frame = cv2.flip(frame, 1)
        _, buffer = cv2.imencode(".jpg", frame)
        encoded_image = base64.b64encode(buffer).decode("utf-8")

        with open(Config.image_data_file, "w") as file:
            json.dump({"base64_image": encoded_image}, file)
    except Exception as e:
        print(f"Error while capturing image: {e}")

    return redirect("Image")


# Route to display captured image
@Edit_blueprint.route("/Image", methods=["GET"])
def display_image():
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
    try:
        if os.path.exists(Config.image_data_file):
            with open(Config.image_data_file) as file:
                image_data = json.load(file)

            encoded_image = image_data.get("base64_image", "")
            decoded_image_data = base64.b64decode(encoded_image)
            image = Image.open(io.BytesIO(decoded_image_data))
            filename = "final.png"
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
                image_path = os.path.join(
                    Config.upload_image_path[0], recent_image)
            else:
                recent_image = None
                image_path = ""
        else:
            print(f"Error: {Config.image_data_file} does not exist.")
            recent_image = None
            image_path = ""

        return render_template("index.html", image_path=image_path)
    except Exception as e:
        print(f"Error while displaying image: {e}")
        return render_template(
            "index.html", image_path=""
        )  # Show a default image or handle error


@Edit_blueprint.route("/edit/<int:EmployeeCode>", methods=["POST", "GET"])
def edit(EmployeeCode):
    """Edit an existing employee.

    This route allows users to edit an existing employee record. The
    employee is identified by the EmployeeCode, which is a required
    parameter.

    The route accepts both GET and POST requests. A GET request will
    retrieve the employee data from the database and display it in
    the template. A POST request will update the employee data in the
    database with the values provided in the form.

    The form data is expected to contain the following fields:

    - Name
    - gender
    - Department

    The image is expected to be stored in the `Config.image_data_file`
    file.

    The most recent image is displayed.

    The image is displayed in the template with the name "image_path".

    Returns:
        A rendered template with the image path if the request is a
        GET, or a redirect to the home page if the request is a POST.
    """
    if request.method == "POST":
        Name = request.form["Name"]
        gender = request.form["Gender"]
        Department = request.form["Department"]
        try:
            with open(Config.image_data_file) as file:
                image_data = json.load(file)

            encoded_image = image_data.get("base64_image", "")
            payload = {
                "Name": Name,
                "gender": gender,
                "Department": Department,
                "Image": encoded_image,
            }
            try:
                url = requests.put(
                    f"http://127.0.0.1:8000/update/{EmployeeCode}",
                    json=payload,
                )
                if url.status_code == 200:
                    return redirect("/")
                else:
                    print(
                        f"Error: Failed to update employee data with status code {url.status_code}"
                    )
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")

        except Exception as e:
            print(f"Error while processing employee data: {e}")

    try:
        response = requests.get(f"http://127.0.0.1:8000/read/{EmployeeCode}")
        if response.status_code == 200:
            employee_data = response.json()
            return render_template("edit.html", employee_data=employee_data)
        else:
            print(
                f"Error: Failed to retrieve employee data with status code {response.status_code}"
            )
            return f"Error {response.status_code}: Failed to retrieve employee data."
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return "Error: Could not retrieve employee data."
