from fastapi import APIRouter,Form, HTTPException, Response
import base64
import json
import os
from PIL import Image
from pydantic import BaseModel
from io import BytesIO
from datetime import datetime
from pymongo import MongoClient
from deepface import DeepFace
from bson import ObjectId
import logging
from matplotlib import pyplot as plt



# Create a logger object
logger = logging.getLogger(__name__)
# Create a file handler
handler = logging.FileHandler('log.log')
handler.setLevel(logging.INFO)
# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

router = APIRouter()

# To create connection with Mongodb
mongodb_uri ='mongodb://localhost:27017/'
port = 8000
client = MongoClient(mongodb_uri,port)

db = client["ImageDB"]
faceEntries = db["faceEntries"]

# Models  for the data to be sent and received by the server
class Employee(BaseModel):
    EmployeeCode: int
    Name: str
    gender:str
    Department:str
    Image:str

class UpdateEmployee(BaseModel):
    Name: str
    gender:str
    Department:str
    Image:str

# To create new entries of employee
@router.post("/create_new_faceEntry")
async def create_new_faceEntry(EmployeeCode:int= Form(...),Name: str=Form(...), gender: str=Form(...),Department: str= Form(...),encoded_image: str=Form(...)):
    time = datetime.now()
    img_recovered = base64.b64decode(encoded_image)  # decode base64string
    # print(img_recovered)
    pil_image = Image.open(BytesIO(img_recovered))
    image_filename= f"{Name}.png"
    pil_image.save(image_filename)
    # print path of the current working directory
    # pil_image.save(f"Images\dbImages\{Name}.jpg")
    # Extract the face from the image
    face_image_data = DeepFace.extract_faces(image_filename, detector_backend="mtcnn",enforce_detection=False)
    # Calculate the embeddings of the face image
    # plt.imsave(f"Images/Faces/{Name}.jpg", face_image_data[0]['face'])
    embeddings = DeepFace.represent(image_filename, model_name="Facenet", detector_backend="mtcnn")
    os.remove(image_filename)
    # Store the data in the database
    db.faceEntries.insert_one({
        "EmployeeCode":EmployeeCode,
        "Name": Name,
        "gender": gender,
        "Department": Department,
        "time": time,
        "embeddings": embeddings,
        "Image": encoded_image
    })
    return {"message": "Face entry created successfully"}

# To display all records
@router.get("/Data/",response_model=list[Employee])
async def get_employees():
    employees_mongo =  faceEntries.find()
    employees = [
        Employee(
            EmployeeCode=int(employee.get('EmployeeCode', 0)),
            Name=employee.get('Name', 'N/A'),
            gender=employee.get('gender', 'N/A'),
            Department=employee.get('Department', 'N/A'),
            Image=employee.get('Image', 'N/A')
        )
        for employee in employees_mongo
    ]
    return employees

#To display specific record info
@router.get('/read/{EmployeeCode}', response_class=Response)
async def read_employee(EmployeeCode: int):
    try:
        # logger.info(f"Start {EmployeeCode}")
        items = faceEntries.find_one(filter={'EmployeeCode': EmployeeCode}, projection={"Name":True,"gender":True,"Department":True,"Image":True,"_id": False})
        if items:
            json_items = json.dumps(items)
            return Response(content=bytes(json_items, 'utf-8'), media_type="application/json")
        else:
            return Response(content=json.dumps({"message": "Employee not found"}), media_type="application/json", status_code=404)
    except Exception as e:
        print(e)

# For updating existing record
@router.put('/update/{EmployeeCode}', response_model=str)
async def update_employees(EmployeeCode: int, Employee: UpdateEmployee):
    try:
        # logger.warning("Updating Start")
        user_id = faceEntries.find_one({"EmployeeCode": EmployeeCode}, projection={"_id": True})
        print(user_id)
        if not user_id:
            raise HTTPException(status_code=404, detail="Employee not found")
        Employee_data = Employee.model_dump(by_alias=True,exclude_unset=True)
        # logger.info(f"Employee data to update: {Employee_data}")
        try:
            update_result = faceEntries.update_one(
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
@router.delete('/delete/{EmployeeCode}')
async def delete_employees(EmployeeCode:int):
    print(EmployeeCode)
    db.faceEntries.find_one_and_delete({
        'EmployeeCode':EmployeeCode
        })

    return {"Message": "Successfully Deleted"}