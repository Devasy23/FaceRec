from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from pymongo import MongoClient
from random import randint
import uuid

IMAGEDIR = "test-faces/"

mongodb_uri ='mongodb://localhost:27017/'
port = 8000
client = MongoClient(mongodb_uri,port)

db = client["ImageDB"]

app = FastAPI()

@app.post("/upload/")
async def register_face(file: UploadFile = File(...)):

    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    #save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    db.images.insert_one({"filename": file.filename, "contents": contents})
    return {"filename": file.filename}



@app.get("/show/")
async def read_random_file():

    # get random file from the image directory
    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)

    path = f"{IMAGEDIR}{files[random_index]}"
    
    return FileResponse(path)