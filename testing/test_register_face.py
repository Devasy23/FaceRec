import base64
import os

import pytest
import requests
from fastapi.testclient import TestClient

from API.route import router

client = TestClient(router)


def test_register_face():
    # Open a test image file in binary mode
    IMAGEDIR = "test-faces/"
    with open("./test-faces/devansh.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    response = client.post(
        "/create_new_faceEntry",
        json={
            "EmployeeCode": "1",
            "Name": "Test",
            "gender": "Male",
            "Department": "Test",
            "Image": encoded_string,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Face entry created successfully"}
