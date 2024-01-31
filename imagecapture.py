import http
from flask import Flask, Response, jsonify,redirect,render_template ,current_app,request, url_for
import requests
import cv2
import base64
import json
import os
from PIL import Image
import io
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(filename='logging.txt',
                    filemode='a',
                    format='%(asctime)s - %(name)-10s - %(levelname)-8s - %(lineno)4d - %(funcName)-15s - %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


app = Flask(__name__,template_folder="template")
app.config.from_file("config.json", load=json.load) 

with app.app_context():
    upload_image_path = current_app.config.get('UPLOAD_FOLDER')
    image_data_file = current_app.config.get('IMAGE_DATA')

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
        logger.info(resp.status_code)
        #logger.info(resp.json())
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    jsonify({"message": "Successfully executed"})
    print("Executed.")
    return redirect('DisplayingEmployees')


@app.route('/video_feed')
def video_feed():
    return Response(display_live_video(),mimetype='multipart/x-mixed-replace;boundary=frame')


        
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
        logger.info(resp.status_code)
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
            logger.info(payload)
            try:
                url =requests.put(f'http://127.0.0.1:8000/update/{EmployeeCode}',json=payload)
                logger.info(url.status_code)
                logger.info(url.json())
                
                return redirect("/")
                
                
            except requests.exceptions.RequestException as e:
                print(f'Request failed: {e}')
        response = requests.get(f"http://127.0.0.1:8000/read/{EmployeeCode}")
        logger.info(response.status_code)
        logger.info(response.json())
        if response.status_code == 200:
            employee_data = response.json()
            return render_template("edit.html", employee_data=employee_data)
        else:
            return f"Error {response.status_code}: Failed to retrieve employee data."
    


# @app.route('/editted_form',methods=['POST'])
# def editted_form():
#     Name = request.form['Name']
#     gender = request.form['Gender']
#     Department = request.form['Department']
#     with open(image_data_file,'r') as file:
#             image_data = json.load(file)
#     encoded_image= image_data.get("base64_image","")
#     jsonify({
#         "EmployeeCode": EmployeeCode,
#         "Name": Name,
#         "gender": gender,
#         "Department":Department,
#         "encoded_image" : encoded_image
#     })
#     payload={"Name": Name,"gender": gender,"Department":Department,"encoded_image":encoded_image}
#     url = 'http://127.0.0.1:8000/update/{EmployeeCode}'
#     try:
#         resp = requests.put(url=url, data=payload)
#         logger.info(resp.status_code)
#         # logger.info(resp.json())
#     except requests.exceptions.RequestException as e:
#         print(f'Request failed: {e}')
#     jsonify({"message": "Successfully executed"})
#     print("Executed.")
#     return redirect('DisplayingEmployees')

@app.route('/Delete/<int:EmployeeCode>',methods=['DELETE','GET'])
def Delete(EmployeeCode):
    

    #logger.info(employees)
    response = requests.delete(f"http://127.0.0.1:8000/delete/{EmployeeCode}")
    jsonify(response.json())
 
    return redirect("/DisplayingEmployees")


if __name__ == '__main__':
    app.run(debug=True)
    