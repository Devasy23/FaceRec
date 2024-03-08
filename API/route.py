import base64
import json
import logging
import os
from datetime import datetime
from io import BytesIO

from API.utils import init_logging_config
from typing import List
from bson import ObjectId
from deepface import DeepFace
from fastapi import APIRouter, Form, HTTPException, Response
from matplotlib import pyplot as plt
from PIL import Image
from pydantic import BaseModel
from pymongo import MongoClient

from API.database import Database

init_logging_config()

router = APIRouter()


client = Database()

collection = "faceEntries"


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
    Name = Employee.Name
    EmployeeCode = Employee.EmployeeCode
    gender = Employee.gender
    Department = Employee.Department
    encoded_images = Employee.Images
    time = datetime.now()
    
    embeddings = []
    for encoded_image in encoded_images:
        img_recovered = base64.b64decode(encoded_image)  # decode base64string
        # print(img_recovered)
        pil_image = Image.open(BytesIO(img_recovered))
        image_filename = f"{Name}.png"
        pil_image.save(image_filename)
        # print path of the current working directory
        pil_image.save(f"Images\dbImages\{Name}.jpg")
        # Extract the face from the image
        face_image_data = DeepFace.extract_faces(
            image_filename, detector_backend="mtcnn", enforce_detection=False
        )
        # Calculate the embeddings of the face image
        plt.imsave(f"Images/Faces/{Name}.jpg", face_image_data[0]["face"])
        embedding = DeepFace.represent(
            image_filename, model_name="Facenet", detector_backend="mtcnn"
        )
        embeddings.append(embedding)
        os.remove(image_filename)
    # Store the data in the database
    client.insert_one(
        collection,
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
    employees_mongo = client.find(collection)
    employees = [
        Employee(
            EmployeeCode=int(employee.get("EmployeeCode", 0)),
            Name=employee.get("Name", "N/A"),
            gender=employee.get("gender", "N/A"),
            Department=employee.get("Department", "N/A"),
            Images=employee.get("Images", "N/A"),
        )
        for employee in employees_mongo
    ]
    return employees


# To display specific record info
@router.get("/read/{EmployeeCode}", response_class=Response)
async def read_employee(EmployeeCode: int):
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


# For updating existing record
@router.put("/update/{EmployeeCode}", response_model=str)
async def update_employees(EmployeeCode: int, Employee: UpdateEmployee):
    try:
        # logger.warning("Updating Start")
        user_id = client.find_one(
            collection, {"EmployeeCode": EmployeeCode}, projection={"_id": True}
        )
        print(user_id)
        if not user_id:
            raise HTTPException(status_code=404, detail="Employee not found")
        Employee_data = Employee.model_dump(by_alias=True, exclude_unset=True)
        # logger.info(f"Employee data to update: {Employee_data}")
        try:
            update_result = client.update_one(
                collection,
                filter={"_id": ObjectId(user_id["_id"])},
                update={"$set": Employee_data},
            )
            if update_result.modified_count == 0:
                raise HTTPException(status_code=400, detail="No data was updated")
            return "Updated Successfully"
        except Exception as e:
            # logger.error(f"Error while updating: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        # logger.error(f"Error while fetching user_id: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# To delete employee record
@router.delete("/delete/{EmployeeCode}")
async def delete_employees(EmployeeCode: int):
    print(EmployeeCode)
    client.find_one_and_delete(collection, {"EmployeeCode": EmployeeCode})

    return {"Message": "Successfully Deleted"}
