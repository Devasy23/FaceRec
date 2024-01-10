# import pytest
# from starlette.testclient import TestClient
# from ..main import app
# import os

# IMAGEDIR = "/test-faces"

# def test_register_face():
#     client = TestClient(app)
#     with open('test_image.jpg', 'rb') as test_file:
#         response = client.post(
#             "/upload/",
#             files={"file": ("test_image.jpg", test_file, "image/jpeg")},
#         )

#     assert response.status_code == 200
#     assert 'filename' in response.json()

#     # Cleanup: remove the uploaded file after test
#     os.remove(f"{IMAGEDIR}{response.json()['filename']}")

import requests
import base64

# Open the image file in binary mode, read it, and encode it to base64
# with open('test-faces/07c64ef1-b32e-4396-97ea-0894249d58ee.jpg', 'rb') as image_file:
#     encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

# # Define the URL where you want to send the POST request
# url = "http://localhost:8000/upload/"

# # Define the headers for the POST request
# headers = {'Content-Type': 'application/json'}

# # Define the body of the POST request
# data = {"file": encoded_string}

# # Send the POST request
# response = requests.post(url, headers=headers, json=data)

# # Print the response
# print(response.json())

import requests

# Open the image file in binary mode
with open('test-faces/07c64ef1-b32e-4396-97ea-0894249d58ee.jpg', 'rb') as image_file:
    # Define the URL where you want to send the POST request
    url = "http://localhost:8000/upload/"

    # Send the POST request with the file
    response = requests.post(url, files={'file': image_file})

    # Print the response
    print(response.json())