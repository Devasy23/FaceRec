from __future__ import annotations

import base64
import logging
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from API.route import router
from API.utils import init_logging_config

init_logging_config()

client = TestClient(router)


@pytest.mark.run(order=1)
def test_register_face1():
    """
    Test the creation of a face entry.

    Verifies that a POST request to /create_new_faceEntry with a valid
    JSON body containing an EmployeeCode, Name, gender, Department, and
    a list of one or more images creates a new face entry in the database
    and returns a message indicating success.
    """
    mock_doc = {
        "_id": "65e6284d01f95cd96ea334a7",
        "EmployeeCode": "1",
        "Name": "Devansh",
        "gender": "Male",
        "Department": "IT",
        "Images": ["encoded_string1", "encoded_string2"],
    }

    mock_find = MagicMock(return_value=[mock_doc, mock_doc])
    mock_insert_one = MagicMock(return_value=MagicMock(inserted_id="1"))
    mock_find_one = MagicMock(return_value=mock_doc)
    mock_update_one = MagicMock(return_value=MagicMock(modified_count=1))
    mock_find_one_and_delete = MagicMock(return_value=mock_doc)

    with patch("API.database.Database.find", mock_find), patch(
        "API.database.Database.insert_one",
        mock_insert_one,
    ), patch("API.database.Database.find_one", mock_find_one), patch(
        "API.database.Database.update_one",
        mock_update_one,
    ), patch(
        "API.database.Database.find_one_and_delete",
        mock_find_one_and_delete,
    ):

        with open("./test-faces/devansh.jpg", "rb") as image_file:
            encoded_string1 = base64.b64encode(
                image_file.read(),
            ).decode("utf-8")

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
        assert response1.json() == {
            "message": "Face entry created successfully",
        }


@pytest.mark.run(order=2)
def test_register_face2():
    """
    Test the creation of a second face entry.

    Verifies that a POST request to /create_new_faceEntry with a valid
    JSON body containing an EmployeeCode, Name, gender, Department, and
    a list of one or more images creates a new face entry in the database
    and returns a message indicating success.
    """
    mock_doc = {
        "_id": "65e6284d01f95cd96ea334a7",
        "EmployeeCode": "1",
        "Name": "Devansh",
        "gender": "Male",
        "Department": "IT",
        "Images": ["encoded_string1", "encoded_string2"],
    }

    mock_find = MagicMock(return_value=[mock_doc, mock_doc])
    mock_insert_one = MagicMock(return_value=MagicMock(inserted_id="1"))
    mock_find_one = MagicMock(return_value=mock_doc)
    mock_update_one = MagicMock(return_value=MagicMock(modified_count=1))
    mock_find_one_and_delete = MagicMock(return_value=mock_doc)

    with patch("API.database.Database.find", mock_find), patch(
        "API.database.Database.insert_one",
        mock_insert_one,
    ), patch("API.database.Database.find_one", mock_find_one), patch(
        "API.database.Database.update_one",
        mock_update_one,
    ), patch(
        "API.database.Database.find_one_and_delete",
        mock_find_one_and_delete,
    ):

        with open("./test-faces/devansh.jpg", "rb") as image_file:
            encoded_string2 = base64.b64encode(
                image_file.read(),
            ).decode("utf-8")

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
        assert response2.json() == {
            "message": "Face entry created successfully",
        }


@pytest.mark.run(order=3)
def test_get_all_faces_after_registration():
    """
    Test the retrieval of all face entries after registration.

    Verifies that a GET request to /Data returns a list of all face entries
    in the database, and that the list contains the two face entries created
    in the previous tests.
    """
    mock_doc = {
        "_id": "65e6284d01f95cd96ea334a7",
        "EmployeeCode": "1",
        "Name": "Devansh",
        "gender": "Male",
        "Department": "IT",
        "Images": ["encoded_string1", "encoded_string2"],
    }

    mock_find = MagicMock(return_value=[mock_doc, mock_doc])

    with patch("API.database.Database.find", mock_find):
        response = client.get("/Data/")
        assert response.status_code == 200
        logging.debug(response.json())
        assert len(response.json()) == 2


@pytest.mark.run(order=4)
def test_update_face():
    """
    Test the update of a face entry.

    Verifies that a PUT request to /update/{EmployeeCode} with a valid
    JSON body containing an EmployeeCode, Name, gender, Department, and
    a list of one or more images updates the face entry in the database
    and returns a message indicating success.
    """
    mock_doc = {
        "_id": "65e6284d01f95cd96ea334a7",
        "EmployeeCode": "1",
        "Name": "Devansh",
        "gender": "Male",
        "Department": "IT",
        "Images": ["encoded_string1", "encoded_string2"],
    }

    mock_find = MagicMock(return_value=[mock_doc, mock_doc])
    mock_insert_one = MagicMock(return_value=MagicMock(inserted_id="1"))
    mock_find_one = MagicMock(return_value=mock_doc)
    mock_update_one = MagicMock(return_value=MagicMock(modified_count=1))
    mock_find_one_and_delete = MagicMock(return_value=mock_doc)

    with patch("API.database.Database.find", mock_find), patch(
        "API.database.Database.insert_one",
        mock_insert_one,
    ), patch("API.database.Database.find_one", mock_find_one), patch(
        "API.database.Database.update_one",
        mock_update_one,
    ), patch(
        "API.database.Database.find_one_and_delete",
        mock_find_one_and_delete,
    ):
        with open("./test-faces/devansh.jpg", "rb") as image_file:
            encoded_string2 = base64.b64encode(
                image_file.read(),
            ).decode("utf-8")

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


@pytest.mark.run(order=5)
def test_delete_face():
    """
    Test the DELETE endpoint to delete a face entry.

    This test case asserts that the DELETE endpoint returns a 200 status code and a JSON response with the message 'Successfully Deleted'.
    """
    response = client.delete("/delete/1")
    assert response.status_code == 200
    assert response.json() == {"Message": "Successfully Deleted"}


@pytest.mark.run(order=6)
def test_recognize_face_fail():
    """
    Test the POST endpoint to recognize a face when no match is found.

    This test case asserts that the POST endpoint returns a 404 status code and a JSON response with the message 'No match found'.
    """
    mock_doc = {
        "Image": "encoded_string2",
        "Name": "Test2",
        "score": 0.0,
    }
    with patch("API.database.Database.vector_search", return_value=[mock_doc]):

        with open("./test-faces/devansh.jpg", "rb") as image_file:
            response = client.post(
                "/recognize_face",
                files={"Face": image_file},
            )
        assert response.status_code == 404
        assert response.json() == {"message": "No match found"}


@pytest.mark.run(order=7)
def test_recognize_face_success():
    """
    Test the POST endpoint to recognize a face when a match is found.

    This test case asserts that the POST endpoint returns a 200 status code and a JSON response with the name, image and score of the matching face entry.
    """
    mock_doc = {
        "Image": "encoded_string2",
        "Name": "Test2",
        "score": 1.0,
    }
    with patch("API.database.Database.vector_search", return_value=[mock_doc]):

        with open("./test-faces/devansh.jpg", "rb") as image_file:
            response = client.post(
                "/recognize_face",
                files={"Face": image_file},
            )
        assert response.status_code == 200
        assert response.json() == {
            "Name": "Test2",
            "Image": "encoded_string2",
            "score": 1.0,
        }
