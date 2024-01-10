import pytest
import requests


def test_register_face():
    with open('test-faces/07c64ef1-b32e-4396-97ea-0894249d58ee.jpg', 'rb') as image_file:
        url = "http://localhost:8000/upload/"
        response = requests.post(url, files={'file': image_file})

        assert response.status_code == 200
    filename = response.json()['filename']
    url = f"http://localhost:8000/delete/{filename}"
    response = requests.delete(url)
    assert response.status_code == 200
    assert response.json() == {'message': 'Face deleted successfully'}
    
        
        

        # assert response.json() == {'message': 'Face registered successfully'}
# Open the image file in binary mode
# with open('test-faces/07c64ef1-b32e-4396-97ea-0894249d58ee.jpg', 'rb') as image_file:
#     # Define the URL where you want to send the POST request
#     url = "http://localhost:8000/upload/"

#     # Send the POST request with the file
#     response = requests.post(url, files={'file': image_file})

#     # Print the response
#     assert response.status_code == 200
#     # print(response.json())