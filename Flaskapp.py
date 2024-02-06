from fastapi import FastAPI
from flask import Flask, jsonify,redirect,render_template,request
from flask import Response as flask_response
import requests
import cv2
import base64
import json
import os
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
from pydantic import BaseModel
import uvicorn
from io import BytesIO
from fastapi import FastAPI, Form, HTTPException, Response
import os
from datetime import datetime
from pymongo import MongoClient
from deepface import DeepFace
import logging
from bson import ObjectId
import uvicorn

app = Flask(__name__,template_folder="template")

app.config["UPLOAD_FOLDER"]= "static/uploads/"
app.config["IMAGE_DATA"]="static/image_data.json"
upload_image_path = app.config["UPLOAD_FOLDER"]
image_data_file =app.config["IMAGE_DATA"]

cap = cv2.VideoCapture(0)

def display_live_video():
    while True:
        success, frame = cap.read()  # Read a frame from the camera
        if not success:
            break
        frame = cv2.flip(frame,1)
        ret, buffer = cv2.imencode('.jpg',frame)
        frame = buffer.tobytes
        if not ret:
            break
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + bytearray(buffer) + b'\r\n\r\n')
    
@app.route('/')
def Main_page():
    if not os.path.exists(upload_image_path):
        os.makedirs(upload_image_path)
    return redirect("DisplayingEmployees")

@app.route('/Add_employee')
def add_employee():
    return render_template("index.html")

@app.route('/submit_form',methods=['POST'])
def submit_form():
    Employee_Code = request.form['EmployeeCode']
    Name = request.form['Name']
    gender = request.form['Gender']
    Department = request.form['Department']
    with open(image_data_file,'r') as file:
            image_data = json.load(file)
    encoded_image= image_data.get("base64_image","")
    jsonify({
        "EmployeeCode": Employee_Code,
        "Name": Name,
        "gender": gender,
        "Department":Department,
        "encoded_image" : encoded_image
    })
    
    payload={"EmployeeCode": Employee_Code,"Name": Name,"gender": gender,"Department":Department,"encoded_image":encoded_image}
    url = 'http://127.0.0.1:8000/create_new_faceEntry'
    try:
        resp = requests.post(url=url, data=payload)
        #logger.info(resp.status_code)
        #logger.info(resp.json())
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    jsonify({"message": "Successfully executed"})
    print("Executed.")
    return redirect('DisplayingEmployees')


@app.route('/video_feed')
def video_feed():
    return flask_response(display_live_video(),mimetype='multipart/x-mixed-replace;boundary=frame')


        
@app.route('/capture', methods=['GET','POST'])
def capture():

    global EmployeeCode
    global Name
    global gender
    global Dept
    global encoded_image

    EmployeeCode =request.form.get('EmployeeCode','')
    Name = request.form.get('Name', '')
    gender = request.form.get('gender', '')
    Dept = request.form.get('Department', '')

    
    ret, frame = cap.read(True)
    frame = cv2.flip(frame,1)
    _, buffer = cv2.imencode(".jpg", frame)
    encoded_image = base64.b64encode(buffer).decode("utf-8")
    with open(image_data_file, 'w') as file:
        json.dump({"base64_image":encoded_image},file)
    return redirect("Image")


@app.route('/Image',methods=['GET'])
def display_image():
    if os.path.exists(image_data_file):
        with open(image_data_file,'r') as file:
            image_data = json.load(file)
        encoded_image= image_data.get("base64_image","")
        decoded_image_data = base64.b64decode(encoded_image)
        image = Image.open(io.BytesIO(decoded_image_data))
        filename ='final.png'
        image.save(os.path.join(upload_image_path, filename), quality=100)


        image = sorted(os.listdir(upload_image_path),key = lambda x: os.path.getatime(os.path.join(upload_image_path,x)),reverse=True)
    if image:
        recent_image = image[0]
        image_path=os.path.join(upload_image_path,recent_image)
    else:
        recent_image= None
    image_path=os.path.join(upload_image_path,recent_image)
    print("done")
    return render_template("index.html",image_path=image_path)


@app.route('/DisplayingEmployees')
def display_information():
    global employees
    url = "http://127.0.0.1:8000/Data/"
    
    try:
        resp = requests.get(url=url)
        #logger.info(resp.status_code)
        #logger.info(resp.json())
        employees =resp.json()

    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    return render_template("table.html",employees=employees)
   

@app.route('/edit/<int:EmployeeCode>',methods=['POST','GET'])
def edit(EmployeeCode):
        if request.method =="POST":
            Name =request.form['Name']
            gender = request.form['Gender']
            Department = request.form['Department']
            with open(image_data_file,'r') as file:
                image_data = json.load(file)
            encoded_image= image_data.get("base64_image","")
            payload={"Name":Name,"gender":gender,"Department":Department,"Image":encoded_image}
            #logger.info(payload)
            try:
                url =requests.put(f'http://127.0.0.1:8000/update/{EmployeeCode}',json=payload)
                #logger.info(url.status_code)
                #logger.info(url.json())
                
                return redirect("/")
                
                
            except requests.exceptions.RequestException as e:
                print(f'Request failed: {e}')
        response = requests.get(f"http://127.0.0.1:8000/read/{EmployeeCode}")
        #logger.info(response.status_code)
        #logger.info(response.json())
        if response.status_code == 200:
            employee_data = response.json()
            return render_template("edit.html", employee_data=employee_data)
        else:
            return f"Error {response.status_code}: Failed to retrieve employee data."
    

@app.route('/Delete/<int:EmployeeCode>',methods=['DELETE','GET'])
def Delete(EmployeeCode):
    

    #logger.info(employees)
    response = requests.delete(f"http://127.0.0.1:8000/delete/{EmployeeCode}")
    jsonify(response.json())
 
    return redirect("/DisplayingEmployees")

Fastapp = FastAPI()

@Fastapp.get("/")
def read_root():
    return {"Hello": "FASTAPI"}


mongodb_uri ='mongodb://localhost:27017/'
port = 8000
client = MongoClient(mongodb_uri,port)

db = client["ImageDB"]
faceEntries = db["faceEntries"]

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

@Fastapp.post("/create_new_faceEntry")
async def create_new_faceEntry(EmployeeCode:int= Form(...),Name: str=Form(...), gender: str=Form(...),Department: str= Form(...),encoded_image: str=Form(...)):
    time = datetime.now()
    img_recovered = base64.b64decode(encoded_image)  # decode base64string
    print(img_recovered)
    pil_image = Image.open(BytesIO(img_recovered))

    image_filename= f"{Name}.jpg"
    pil_image.save(image_filename)
    
    # Extract the face from the image
    face_image_data = DeepFace.extract_faces(image_filename, detector_backend="mtcnn",enforce_detection=False)

    # Calculate the embeddings of the face image
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


@Fastapp.get("/Data/",response_model=list[Employee])
async def get_employees():
    employees_mongo =  faceEntries.find()
    print(employees_mongo)
    employees_mongo_data = [Employee(EmployeeCode=employee['EmployeeCode'],Name=employee['Name'],gender=employee['gender'],
                                    Department=employee['Department'],Image=employee['Image'])
                            for employee in employees_mongo]
   
    return employees_mongo_data

@Fastapp.get('/read/{EmployeeCode}', response_class=Response)
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


@Fastapp.put('/update/{EmployeeCode}', response_model=str)
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


@Fastapp.delete('/delete/{EmployeeCode}')
async def delete_employees(EmployeeCode:int):
    print(EmployeeCode)
    db.faceEntries.find_one_and_delete({
        'EmployeeCode':EmployeeCode
        })

    return {"Message": "Successfully Deleted"}

def run_flask():
    app.run(host="127.0.0.1", port=5000)

def run_fastapi_app():
    uvicorn.run(Fastapp, host="127.0.0.1", port=8000)


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_flask)
        executor.submit(run_fastapi_app)
    