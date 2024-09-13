from __future__ import annotations

import base64
import io
import json
import os

import cv2
import requests
from flask import Blueprint, jsonify, redirect, render_template, request
from PIL import Image

from FaceRec.config import Config

video_capture = cv2.VideoCapture(0)
flk_blueprint = Blueprint(
    "flk_blueprint ",
    __name__,
    template_folder="../../templates/",
    static_folder="../../static/",
    # capture_image="../../Capture image/"
)


@flk_blueprint.route("/")
def Main_page():
    """
    This route is used to create a directory for storing images of employees
    if it does not already exist. It then redirects to the route displaying all
    records of employees. This route is used when the user first visits the
    website.
    """
    path = str(Config.upload_image_path[0])
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    else:
        pass
    return redirect("DisplayingEmployees")


# Displaying all records
@flk_blueprint.route("/DisplayingEmployees")
def display_information():
    """This route is used to retrieve all records of employees from the FastAPI
    endpoint http://127.0.0.1:8000/Data/ and store them in the employees global
    variable. The records are then passed to the template table.html to be
    displayed in a table. If the request to the FastAPI endpoint fails, an
    appropriate error message is printed to the console."""
    global employees
    url = "http://127.0.0.1:8000/Data/"
    try:
        resp = requests.get(url=url)
        # logger.info(resp.status_code)
        # logger.info(resp.json())
        employees = resp.json()

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return render_template("table.html", employees=employees)


# To add employee record
@flk_blueprint.route("/Add_employee")
def add_employee():
    """This route is used to display the form for adding a new employee record.
    The form is rendered from the template index.html."""

    return render_template("index.html")


# To submit the form data to server and save it in database
@flk_blueprint.route("/submit_form", methods=["POST"])
def submit_form():
    """
    This route is used to handle the form submission of the new employee
    record. The form data is received from the request object and then
    validated. The image is base64 encoded and saved in the file defined
    in the Config class. The image is then sent to the FastAPI endpoint
    http://127.0.0.1:8000/create_new_faceEntry to be stored in the MongoDB
    database. If the request to the FastAPI endpoint fails, an appropriate
    error message is returned. If the request is successful, the user is
    redirected to the route /DisplayingEmployees to view the newly added
    record.
    """
    Employee_Code = request.form["EmployeeCode"]
    Name = request.form["Name"]
    gender = request.form["Gender"]
    Department = request.form["Department"]

    if request.files["File"]:
        if "File" not in request.files:
            return jsonify({"message": "No file part"}), 400
        file = request.files["File"]
        allowed_extensions = {"png", "jpg", "jpeg"}
        if (
            "." not in file.filename
            or file.filename.split(".")[-1].lower() not in allowed_extensions
        ):
            return jsonify({"message": "File extension is not valid"}), 400
        if file:
            image_data = file.read()
            encoded_image = base64.b64encode(image_data).decode("utf-8")
            with open(Config.image_data_file, "w") as file:
                json.dump({"base64_image": encoded_image}, file)

    with open(Config.image_data_file, "r") as file:
        image_data = json.load(file)
    encoded_image = image_data.get("base64_image", "")
    jsonify(
        {
            "EmployeeCode": Employee_Code,
            "Name": Name,
            "gender": gender,
            "Department": Department,
            "encoded_image": encoded_image,
        },
    )

    payload = {
        "EmployeeCode": Employee_Code,
        "Name": Name,
        "gender": gender,
        "Department": Department,
        "Image": encoded_image,
    }
    url = "http://127.0.0.1:8000/create_new_faceEntry"
    payload.status_code
    # try:
    #     resp = requests.post(
    #         url=url,
    #         json={
    #             "EmployeeCode": 134,
    #             "Name": "Name",
    #             "gender": "gender",
    #             "Department": "Department",
    #             "Image": "your_image",
    #         },
    #     )
    #     resp.status_code
    # except requests.exceptions.RequestException as e:
    #     print(f"Request failed: {e}")
    jsonify({"message": "Successfully executed"})
    print("Executed.")
    if payload.status_code == 200:
        return redirect("DisplayingEmployees")
    else:
        return jsonify({"message": "Failed to execute"})


# To edit an employee details


# To delete employee details
@flk_blueprint.route("/Delete/<int:EmployeeCode>", methods=["DELETE", "GET"])
def Delete(EmployeeCode):
    """Delete an employee with the given EmployeeCode.

    Args:
        EmployeeCode: The employee code of the employee to be deleted.

    Returns:
        A JSON response with a message indicating the success or failure of the deletion.

    Raises:
        400 error if the EmployeeCode is not an integer.
    """
    if not isinstance(EmployeeCode, int):
        return jsonify({"message": "Employee code should be an integer"}, 400)
    response = requests.delete(f"http://127.0.0.1:8000/delete/{EmployeeCode}")
    jsonify(response.json())

    return redirect("/DisplayingEmployees")
