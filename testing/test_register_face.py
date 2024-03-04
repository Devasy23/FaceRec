import pytest
import requests
from fastapi.testclient import TestClient
from API.route import router
import os
import base64


client = TestClient(router)
def test_register_face():
    # Open a test image file in binary mode
    IMAGEDIR = "test-faces/"
    with open("./test-faces/07c64ef1-b32e-4396-97ea-0894249d58ee.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    response = client.post(
        "/create_new_faceEntry",
        data={
            "EmployeeCode": 1,
            "Name": "test",
            "gender": "Male",
            "Department": "test",
            "encoded_image": encoded_string,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Face entry created successfully"}
