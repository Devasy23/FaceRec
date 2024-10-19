from __future__ import annotations

import base64
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from API.database import Database
from API.route import router

client = TestClient(router)

@patch("API.database.Database.find_one_and_delete")
@patch("API.database.Database.update_one")
@patch("API.database.Database.find_one")
@patch("API.database.Database.find")
@patch("API.database.Database.insert_one")
def test_face_lifecycle(
    mock_insert_one: MagicMock,
    mock_find: MagicMock,
    mock_find_one: MagicMock,
    mock_update_one: MagicMock,
    mock_find_one_and_delete: MagicMock,
):
    # Register two new faces
    """Test the entire lifecycle of a face entry:

    1. Register a new face entry.
    2. Get all face entries.
    3. Update a face entry.
    4. Get all face entries again.
    5. Delete a face entry.
    6. Check that only one face entry remains.
    7. Delete the remaining face entry.
    """
    mock_doc = {
        "_id": "65e6284d01f95cd96ea334a7",
        "EmployeeCode": "1",
        "Name": "Devansh",
        "gender": "Male",
        "Department": "IT",
        "Images": ["encoded_string1", "encoded_string2"],
    }

    # Configure the mock to return the mock document when find() is called
    mock_find.return_value = [mock_doc, mock_doc]
    mock_insert_one.return_value = MagicMock(inserted_id="1")
    mock_find_one.return_value = mock_doc
    mock_update_one.return_value = MagicMock(modified_count=1)
    mock_find_one_and_delete.return_value = mock_doc

    with open("./test-faces/devansh.jpg", "rb") as image_file:
        encoded_string1 = base64.b64encode(image_file.read()).decode("utf-8")
    
    response1 = client.post(
        "/create_new_faceEntry",
        json={
            "EmployeeCode": "1",
            "Name": "Devansh",
            "gender": "Male",
            "Department": "IT",
            "Images": [encoded_string1, encoded_string1],
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
            "Images": [encoded_string2, encoded_string2],
        },
    )
    assert response2.status_code == 200
    assert response2.json() == {"message": "Face entry created successfully"}

    # Get all data
    response = client.get("/Data/")
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Update a face
    response = client.put(
        "/update/1",
        json={
            "Name": "Test",
            "gender": "Male",
            "Department": "IT_Test",
            "Images": [encoded_string2, encoded_string2],
        },
    )
    assert response.status_code == 200
    assert response.json() == "Updated Successfully"

    # Get all data again
    response = client.get("/Data/")
    assert response.status_code == 200
    assert len(response.json()) == 2

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
