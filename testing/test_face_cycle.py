import base64

from fastapi.testclient import TestClient

from API.route import router

client = TestClient(router)


def test_face_lifecycle():
    # Register two new faces
    with open("./test-faces/devansh.jpg", "rb") as image_file:
        encoded_string1 = base64.b64encode(image_file.read()).decode("utf-8")
    response1 = client.post(
        "/create_new_faceEntry",
        json={
            "EmployeeCode": "1",
            "Name": "Devansh",
            "gender": "Male",
            "Department": "IT",
            "Image": encoded_string1,
        },
    )
    assert response1.status_code == 200
    assert response1.json() == {"message": "Face entry created successfully"}

    with open("./test-faces/devansh.jpg", "rb") as image_file:
        encoded_string2 = base64.b64encode(image_file.read()).decode("utf-8")
    response2 = client.post(
        "/create_new_faceEntry",
        json={
            "EmployeeCode": "2",
            "Name": "test",
            "gender": "Female",
            "Department": "IT",
            "Image": encoded_string2,
        },
    )
    assert response2.status_code == 200
    assert response2.json() == {"message": "Face entry created successfully"}

    # Get all data
    response = client.get("/Data/")
    assert response.status_code == 200
    # assert len(response.json()) == 2

    # Update a face
    response = client.put(
        "/update/1",
        json={
            "Name": "Test",
            "gender": "Male",
            "Department": "IT_Test",
            "Image": "estring",
        },
    )
    assert response.status_code == 200
    assert response.json() == "Updated Successfully"

    # Get all data again
    response = client.get("/Data/")
    assert response.status_code == 200
    # assert len(response.json()) == 2

    # Delete a face
    response = client.delete("/delete/1")
    assert response.status_code == 200
    assert response.json() == {"Message": "Successfully Deleted"}

    # Check that only one face remains
    response = client.get("/Data/")
    assert response.status_code == 200
    # assert len(response.json()) == 1

    # Delete the remaining face
    response = client.delete("/delete/2")
    assert response.status_code == 200
    assert response.json() == {"Message": "Successfully Deleted"}
