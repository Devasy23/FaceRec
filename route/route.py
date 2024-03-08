import os
import uuid
from datetime import datetime
from random import randint

from deepface import DeepFace
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from matplotlib import pyplot as plt
from pymongo import MongoClient

IMAGEDIR = "test-faces/"

mongodb_uri = "mongodb://localhost:27017/"
port = 8000
client = MongoClient(mongodb_uri, port)

db = client["ImageDB"]
faceEntries = db["faceEntries"]

app = FastAPI()


# deprecated
@app.post("/upload/")
async def register_face(file: UploadFile = File(...)):

    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    # save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    # db.images.insert_one({"filename": file.filename, "contents": contents})
    return {"filename": file.filename}


@app.post("/create_new_faceEntry")
async def create_new_faceEntry(
    id: int, age: int, gender: str, image: UploadFile = File(...)
):
    # Generate a unique ID
    # id = uuid.uuid4()

    # Get the current time
    time = datetime.now()

    # Read the image file
    image_data = await image.read()
    print(image.filename)
    # Save the original image in a specified directory
    with open(f"../Images/dbImages/{image.filename}", "wb") as f:
        f.write(image_data)

    # Extract the face from the image
    face_image_data = DeepFace.extract_faces(
        f"../Images/dbImages/{image.filename}", detector_backend="mtcnn"
    )

    # Save the face image in a specified directory
    plt.imsave(f"../Images/Faces/{image.filename}", face_image_data[0]["face"])

    # Calculate the embeddings of the face image
    embeddings = DeepFace.represent(
        f"../Images/dbImages/{image.filename}",
        model_name="Facenet",
        detector_backend="mtcnn",
    )

    # Store the data in the database
    db.faceEntries.insert_one(
        {
            "id": id,
            "age": age,
            "gender": gender,
            "time": time,
            "embeddings": embeddings,
            # "face-img": face_image_data,
        }
    )

    return {"message": "Face entry created successfully"}


@app.get("/show/")
async def read_random_file():

    # get random file from the image directory
    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)

    path = f"{IMAGEDIR}{files[random_index]}"

    return FileResponse(path)


@app.delete("/delete/{filename}")
async def delete_file(filename: str):
    os.remove(f"{IMAGEDIR}/{filename}")
    return {"message": "Face deleted successfully"}
