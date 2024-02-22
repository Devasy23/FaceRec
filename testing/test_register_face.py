import pytest
import requests
from fastapi.testclient import TestClient
from API.route import app
import os


client = TestClient(app)
def test_register_face():
    # Open a test image file in binary mode
    IMAGEDIR = "test-faces/"
    with open("./test-faces/07c64ef1-b32e-4396-97ea-0894249d58ee.jpg", "rb") as image_file:
        # Create a tuple with the file's name and its content
        file_tuple = ("test_image.jpg", image_file.read())
        # Create a dictionary with the file's data
        data = {"file": file_tuple}
        # Send a POST request to the register_face endpoint with the test image
        response = client.post("/upload/", files=data)
        # Assert that the response status code is 200 (success)
        assert response.status_code == 200
        # Assert that the response json contains the filename
        assert "filename" in response.json()
        # Assert that the file was saved correctly
        assert os.path.exists(f"{IMAGEDIR}{response.json()['filename']}")
        # Clean up the created file
        os.remove(f"{IMAGEDIR}{response.json()['filename']}")