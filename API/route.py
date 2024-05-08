import base64
import json
import logging
import os
from datetime import datetime
from io import BytesIO
from typing import List

from bson import ObjectId
from deepface import DeepFace
from fastapi import APIRouter, HTTPException, Response, UploadFile, File
from matplotlib import pyplot as plt
from PIL import Image
from pydantic import BaseModel

from API.database import Database
from API.utils import init_logging_config
from dotenv import load_dotenv

load_dotenv()
init_logging_config()

MONGO_URI = os.getenv("MONGO_URL1")
router = APIRouter()


client = Database()
client2 = Database(MONGO_URI, "FaceRec")

collection = "faceEntries"
collection2 = "ImageDB"


# Models  for the data to be sent and received by the server
class Employee(BaseModel):
    EmployeeCode: int
    Name: str
    gender: str
    Department: str
    Images: List[str]


class UpdateEmployee(BaseModel):
    Name: str
    gender: str
    Department: str
    Images: List[str]


# To create new entries of employee
@router.post("/create_new_faceEntry")
async def create_new_faceEntry(Employee: Employee):
    """
    Create a new face entry for an employee.

    Args:
        Employee (Employee): The employee object containing the employee details.

    Returns:
        dict: A dictionary with a success message.

    Raises:
        None
    """
    logging.info("Creating new face entry")
    Name = Employee.Name
    EmployeeCode = Employee.EmployeeCode
    gender = Employee.gender
    Department = Employee.Department
    encoded_images = Employee.Images
    time = datetime.now()

    embeddings = []
    for encoded_image in encoded_images:
        img_recovered = base64.b64decode(encoded_image)  # decode base64string
        pil_image = Image.open(BytesIO(img_recovered))
        logging.info(f"Image opened {Name}")
        image_filename = f"{Name}.png"
        pil_image.save(image_filename)
        pil_image.save(f"Images\dbImages\{Name}.jpg")
        face_image_data = DeepFace.extract_faces(
            image_filename, detector_backend="mtcnn", enforce_detection=False
        )
        plt.imsave(f"Images/Faces/{Name}.jpg", face_image_data[0]["face"])
        logging.info(f"Face saved {Name}")
        embedding = DeepFace.represent(
            image_filename, model_name="Facenet512", detector_backend="mtcnn"
        )
        embeddings.append(embedding)
        logging.info(f"Embedding created Embeddings for {Name}")
        os.remove(image_filename)

    logging.debug(f"About to insert Embeddings: {embeddings}")
    # Store the data in the database
    client2.insert_one(
        collection2,
        {
            "EmployeeCode": EmployeeCode,
            "Name": Name,
            "gender": gender,
            "Department": Department,
            "time": time,
            "embeddings": embeddings,
            "Images": encoded_images,
        },
    )

    return {"message": "Face entry created successfully"}


# To display all records
@router.get("/Data/", response_model=list[Employee])
async def get_employees():
    """
    Retrieve a list of employees from the database.

    Returns:
        list[Employee]: A list of Employee objects containing employee information.
    """
    logging.info("Displaying all employees")
    employees_mongo = client.find(collection)
    logging.info(f"Employees found {employees_mongo}")
    employees = [
        Employee(
            EmployeeCode=int(employee.get("EmployeeCode", 0)),
            Name=employee.get("Name", "N/A"),
            gender=employee.get("gender", "N/A"),
            Department=employee.get("Department", "N/A"),
            Images=employee.get("Images", []),
        )
        for employee in employees_mongo
    ]
    return employees


# To display specific record info
@router.get("/read/{EmployeeCode}", response_class=Response)
async def read_employee(EmployeeCode: int):
    """
    Retrieve employee information based on the provided EmployeeCode.

    Args:
        EmployeeCode (int): The unique code of the employee.

    Returns:
        Response: A response object containing the employee information in JSON format.

    Raises:
        HTTPException: If the employee is not found.

    """
    logging.info(f"Display information for {EmployeeCode}")
    try:
        logging.info(f"Start {EmployeeCode}")
        items = client.find_one(
            collection,
            filter={"EmployeeCode": EmployeeCode},
            projection={
                "Name": True,
                "gender": True,
                "Department": True,
                "Images": True,
                "_id": False,
            },
        )
        if items:
            json_items = json.dumps(items)
            return Response(
                content=bytes(json_items, "utf-8"), media_type="application/json"
            )
        else:
            return Response(
                content=json.dumps({"message": "Employee not found"}),
                media_type="application/json",
                status_code=404,
            )
    except Exception as e:
        print(e)


@router.put("/update/{EmployeeCode}", response_model=str)
async def update_employees(EmployeeCode: int, Employee: UpdateEmployee):
    """
    Update employee information based on the provided EmployeeCode.

    Whenever user clicks on update employee button, in the frontend part, all the images will be visible - they can be deleted or new images can be added.
    Accordingly, the embeddings will be recalculated and updated in the database.

    Args:
        EmployeeCode (int): The unique code of the employee to be updated.
        Employee (UpdateEmployee): The updated employee data.

    Returns:
        str: A message indicating the success of the update operation.

    Raises:
        HTTPException: If the employee with the given EmployeeCode is not found.
        HTTPException: If no data was updated during the update operation.
        HTTPException: If an internal server error occurs.
    """
    logging.info(f"Updating for EmployeeCode: {EmployeeCode}")
    try:
        user_id = client.find_one(
            collection, {"EmployeeCode": EmployeeCode}, projection={"_id": True}
        )
        print(user_id)
        if not user_id:
            raise HTTPException(status_code=404, detail="Employee not found")
        Employee_data = Employee.model_dump(by_alias=True, exclude_unset=True)
        logging.info(f"Employee data {Employee_data}")
        # Calculate and store embeddings for the updated image array
        encoded_images = Employee.Images
        embeddings = []
        for encoded_image in encoded_images:
            img_recovered = base64.b64decode(encoded_image)  # decode base64string
            pil_image = Image.open(BytesIO(img_recovered))
            image_filename = f"{Employee.Name}.png"
            pil_image.save(image_filename)
            logging.info(f"Image saved {Employee.Name}")
            face_image_data = DeepFace.extract_faces(
                image_filename, detector_backend="mtcnn", enforce_detection=False
            )
            embedding = DeepFace.represent(
                image_filename, model_name="Facenet", detector_backend="mtcnn"
            )
            logging.info(f"Embedding created {Employee.Name}")
            embeddings.append(embedding)
            os.remove(image_filename)
        Employee_data["embeddings"] = embeddings

        try:
            update_result = client.update_one(
                collection,
                {"_id": ObjectId(user_id["_id"])},
                update={"$set": Employee_data},
            )
            logging.info(f"Update result {update_result}")
            if update_result.modified_count == 0:
                raise HTTPException(status_code=400, detail="No data was updated")
            return "Updated Successfully"
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# To delete employee record
@router.delete("/delete/{EmployeeCode}")
async def delete_employees(EmployeeCode: int):
    """
    Delete an employee from the collection based on the provided EmployeeCode.

    Args:
        EmployeeCode (int): The unique code of the employee to be deleted.

    Returns:
        dict: A dictionary containing a success message.

    """
    """
    Delete an employee from the collection based on the provided EmployeeCode.

    Args:
        EmployeeCode (int): The unique code of the employee to be deleted.

    Returns:
        dict: A dictionary containing a success message.

    """
    logging.info("Deleting Employee")
    logging.info(f"Deleting for EmployeeCode: {EmployeeCode}")
    client.find_one_and_delete(collection, {"EmployeeCode": EmployeeCode})

    return {"Message": "Successfully Deleted"}


@router.post("/recognize_face", response_class=Response)
async def recognize_face(Face: UploadFile = File(...)):
    """
    Recognize a face from the provided image.

    Args:
        Face (UploadFile): The image file to be recognized.

    Returns:
        Response: A response object containing the recognized employee information in JSON format.

    Raises:
        HTTPException: If an internal server error occurs.
    """
    logging.info("Recognizing Face")
    try:
        img_data = await Face.read()
        with open("temp.png", "wb") as f:
            f.write(img_data)

        embedding = DeepFace.represent(img_path="temp.png", model_name="Facenet512", detector_backend="mtcnn")
        result = client2.vector_search(collection2, embedding[0]['embedding'])
        logging.info(f"Result: {result[0]['Name']}, {result[0]['score']}")
        os.remove("temp.png")
        if result[0]['score'] < 0.5:
            return Response(status_code=404, content=json.dumps({"message": "No match found"}))
    except Exception as e:
        logging.error(f"Error: {e}")
        os.remove("temp.png")
        raise HTTPException(status_code=500, detail="Internal server error")
    return Response(
        content=bytes(json.dumps(result[0], default=str), "utf-8"),
        media_type="application/json",
    )