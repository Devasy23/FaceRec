from __future__ import annotations

import base64
import json
import os

import cv2
import requests
from flask import Blueprint, jsonify, redirect, render_template, request
import logging

from FaceRec.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

video_capture = cv2.VideoCapture(0)
flk_blueprint = Blueprint(
    "flk_blueprint",
    __name__,
    template_folder="../../templates/",
    static_folder="../../static/",
)


@flk_blueprint.route("/")
def main_page():
    """
    This route creates a directory for storing employee images if it doesn't exist
    and redirects to the route displaying all employee records.
    """
    path = str(Config.upload_image_path[0])
    os.makedirs(path, exist_ok=True)
    return redirect("DisplayingEmployees")


@flk_blueprint.route("/DisplayingEmployees")
def display_information():
    """Retrieve and display all employee records."""
    global employees
    url = "http://127.0.0.1:8000/Data/"
    try:
        resp = requests.get(url=url)
        resp.raise_for_status()  # Raise an error for bad responses
        employees = resp.json()
        logger.info("Employee data retrieved successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        employees = []  # Handle the error gracefully by setting employees to an empty list
    return render_template("table.html", employees=employees)


@flk_blueprint.route("/Add_employee")
def add_employee():
    """Display the form for adding a new employee record."""
    return render_template("index.html")


@flk_blueprint.route("/submit_form", methods=["POST"])
def submit_form():
    """
    Handle the form submission for adding a new employee record.
    Validate input and save image data before sending it to the FastAPI endpoint.
    """
    try:
        Employee_Code = request.form["EmployeeCode"]
        Name = request.form["Name"]
        gender = request.form["Gender"]
        Department = request.form["Department"]

        # Validate and process image file
        if "File" not in request.files:
            return jsonify({"message": "No file part"}), 400
        file = request.files["File"]
        allowed_extensions = {"png", "jpg", "jpeg"}
        if file and file.filename.split('.')[-1].lower() not in allowed_extensions:
            return jsonify({"message": "File extension is not valid"}), 400

        image_data = file.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")

        # Save the encoded image
        with open(Config.image_data_file, "w") as img_file:
            json.dump({"base64_image": encoded_image}, img_file)

        # Prepare payload for API
        payload = {
            "EmployeeCode": Employee_Code,
            "Name": Name,
            "gender": gender,
            "Department": Department,
            "Image": encoded_image,
        }

        # Send request to FastAPI
        response = requests.post("http://127.0.0.1:8000/create_new_faceEntry", json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        logger.info("Employee record created successfully.")

        return redirect("DisplayingEmployees")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return jsonify({"message": "Failed to execute"}), 500

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"message": "An unexpected error occurred."}), 500


@flk_blueprint.route("/Delete/<int:EmployeeCode>", methods=["DELETE", "GET"])
def delete(EmployeeCode):
    """Delete an employee with the given EmployeeCode."""
    if not isinstance(EmployeeCode, int):
        return jsonify({"message": "Employee code should be an integer"}), 400

    try:
        response = requests.delete(f"http://127.0.0.1:8000/delete/{EmployeeCode}")
        response.raise_for_status()  # Raise an error for bad responses
        logger.info(f"Employee {EmployeeCode} deleted successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return jsonify({"message": "Failed to delete employee."}), 500

    return redirect("/DisplayingEmployees")


# Add additional routes for editing employee details if needed
@flk_blueprint.route("/Edit_employee/<int:EmployeeCode>")
def edit_employee(EmployeeCode):
    """Display the form for editing an existing employee record."""
    # Fetch employee details from the FastAPI endpoint
    url = f"http://127.0.0.1:8000/Data/{EmployeeCode}"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Raise an error for bad responses
        employee = response.json()
        return render_template("edit.html", employee=employee)
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return jsonify({"message": "Failed to retrieve employee data."}), 500


@flk_blueprint.route("/update_employee/<int:EmployeeCode>", methods=["POST"])
def update_employee(EmployeeCode):
    """Update an existing employee's details."""
    try:
        Name = request.form["Name"]
        gender = request.form["Gender"]
        Department = request.form["Department"]

        payload = {
            "EmployeeCode": EmployeeCode,
            "Name": Name,
            "gender": gender,
            "Department": Department,
        }

        response = requests.put(f"http://127.0.0.1:8000/update/{EmployeeCode}", json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        logger.info(f"Employee {EmployeeCode} updated successfully.")

        return redirect("DisplayingEmployees")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return jsonify({"message": "Failed to update employee."}), 500

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"message": "An unexpected error occurred."}), 500
