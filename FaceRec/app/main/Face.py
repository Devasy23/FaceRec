import base64
import io
import json
import os
import cv2
from flask import Blueprint
from flask import Response as flask_response
from flask import redirect, render_template, request
from PIL import Image
import requests
 
from FaceRec.config import Config
 
Face_Rec_blueprint = Blueprint(
    "Face_Rec_blueprint",
    __name__,
    template_folder="../../templates/",
    static_folder="../../static/",
)
cap = cv2.VideoCapture(0)
 
def display_live_video():
    while True:
        success, frame = cap.read(True)  # Read a frame from the camera
        if not success:
            break
        frame = cv2.flip(frame, 1)
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes
        if not ret:
            break
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + bytearray(buffer) + b"\r\n\r\n"
        )
 
@Face_Rec_blueprint.route("/recognize_employee")
def recognize_employee():
    return render_template("recognition.html")
 
@Face_Rec_blueprint.route("/video_feed")
def video_feed():
    return flask_response(
        display_live_video(), mimetype="multipart/x-mixed-replace;boundary=frame"
    )
 
 
   
@Face_Rec_blueprint.route("/Recognize", methods=["GET","POST"])
def recognize():
    files = {'image': (open(f"captured_image.jpg", 'rb'), 'image/jpeg')}
    fastapi_url = 'http://127.0.0.1:8000/recognize_face'  # Replace with your FastAPI URL
    response = requests.post(fastapi_url, files=files)
    return render_template("recognition.html", response_text = response.text)
