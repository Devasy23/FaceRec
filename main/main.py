from io import BytesIO
import json
from fastapi import Body, Depends, FastAPI, Form, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
import os
from datetime import datetime
from pymongo import MongoClient, ReturnDocument
from random import randint
# from fastapi_mongodb import MongoDBMiddleware
from deepface import DeepFace
from pydantic import BaseModel
import base64
import logging
from PIL import Image
from bson import ObjectId


logger = logging.getLogger(__name__)
logging.basicConfig(filename='logging.txt',
                    filemode='a',
                    format='%(asctime)s - %(name)-10s - %(levelname)-8s - %(lineno)4d - %(funcName)-15s - %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


IMAGEDIR = "D:/FaceRec-main/test-faces/"

mongodb_uri ='mongodb://localhost:27017/'
port = 8000
client = MongoClient(mongodb_uri,port)

db = client["ImageDB"]
faceEntries = db["faceEntries"]

def testing(client):
    try:
        if client.is_primary:
            print("Connected to mongodb")
        else:
            print("Not connect.")
    except Exception as err:

# catch pymongo.errors.ServerSelectionTimeoutError
        print ("pymongo ERROR:", err)

print(testing(client))

app = FastAPI()


class item(BaseModel):
    id: float |  None = None

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




# deprecated
# @app.post("/upload/")
# async def register_face(filename: str = Form(...), filedata: str = Form(...)):

#     image_as_bytes = str.encode(filedata)  # convert string to bytes
#     img_recovered = base64.b64decode(image_as_bytes)  # decode base64string
#     try:
#         with open(f"../Images/upload/uploaded_{filename}", "wb") as f:
#             f.write(img_recovered)
#     except Exception:
#         return {"message": "There was an error uploading the file"}
    
#     logger.info("Successfully run" + filename)
#     # db.images.insert_one({"filename": file.filename, "contents": contents})
#     return {"filename": filename} 

@app.post("/create_new_faceEntry")
async def create_new_faceEntry(EmployeeCode:int= Form(...),Name: str=Form(...), gender: str=Form(...),Department: str= Form(...),encoded_image: str=Form(...)):
    # Generate a unique ID
    # id = uuid.uuid4()

    # Get the current time
    time = datetime.now()
    
    #image_as_bytes = str.encode(encoded_image)
    #print("Image:", image_as_bytes)  # convert string to bytes
    img_recovered = base64.b64decode(encoded_image)  # decode base64string
    print(img_recovered)
    pil_image = Image.open(BytesIO(img_recovered))

    image_filename= f"{Name}.jpg"
    pil_image.save(image_filename)
    
    # Extract the face from the image
    face_image_data = DeepFace.extract_faces(image_filename, detector_backend="mtcnn",enforce_detection=False)

    # Calculate the embeddings of the face image
    embeddings = DeepFace.represent(image_filename, model_name="Facenet", detector_backend="mtcnn")
    # with  open(image_filename,'rb') as image_file:
    #     image_binary = (image_file.read())
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
         #"face-img": face_image_data,
    })

    return {"message": "Face entry created successfully"}

# @app.get("/show/")
# async def read_random_file():
#     folder ="D:/FaceRec-main/Images/upload"
#     # get random file from the image directory
#     files = os.listdir(folder)
#     random_index = randint(0, len(files) - 1)

#     path = f"{folder}{files[random_index]}"
#     logger.info("Successfully shown.")
#     return FileResponse(path)


@app.get("/Data/",response_model=list[Employee])
async def get_employees():
    employees_mongo =  faceEntries.find()
    print(employees_mongo)
    employees_mongo_data = [Employee(EmployeeCode=employee['EmployeeCode'],Name=employee['Name'],gender=employee['gender'],
                                    Department=employee['Department'],Image=employee['Image'])
                            for employee in employees_mongo]
   
    return employees_mongo_data



@app.get('/read/{EmployeeCode}', response_class=Response)
async def read_employee(EmployeeCode: int):
    try:
        logger.info(f"Start {EmployeeCode}")
        items = faceEntries.find_one(filter={'EmployeeCode': EmployeeCode}, projection={"Name":True,"gender":True,"Department":True,"Image":True,"_id": False})
        if items:
            json_items = json.dumps(items)
            return Response(content=bytes(json_items, 'utf-8'), media_type="application/json")
        else:
            return Response(content=json.dumps({"message": "Employee not found"}), media_type="application/json", status_code=404)
    except Exception as e:
        print(e)


@app.put('/update/{EmployeeCode}', response_model=str)
async def update_employees(EmployeeCode: int, Employee: UpdateEmployee):
    try:
        logger.warning("Updating Start")
        user_id = faceEntries.find_one({"EmployeeCode": EmployeeCode}, projection={"_id": True})
        print(user_id)
        if not user_id:
            raise HTTPException(status_code=404, detail="Employee not found")

        Employee_data = Employee.model_dump(by_alias=True,exclude_unset=True)
        logger.info(f"Employee data to update: {Employee_data}")

        try:
            update_result = faceEntries.update_one(
                filter={"_id": ObjectId(user_id["_id"])},
                update={"$set": Employee_data},
            )

            if update_result.modified_count == 0:
                raise HTTPException(status_code=400, detail="No data was updated")

            return "Updated Successfully"

        except Exception as e:
            logger.error(f"Error while updating: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    except Exception as e:
        logger.error(f"Error while fetching user_id: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@app.delete('/delete/{EmployeeCode}')
async def delete_employees(EmployeeCode:int):
    print(EmployeeCode)
    db.faceEntries.find_one_and_delete({
        'EmployeeCode':EmployeeCode
        })

    return {"Message": "Successfully Deleted"}