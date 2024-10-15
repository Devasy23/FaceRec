from fastapi import FastAPI, File, UploadFile, Form
from deepface import DeepFace
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()
client = MongoClient('mongodb://localhost:27017/')
db = client['face_recognition']
users_collection = db['users']

@app.post("/register/")
async def register_face(image: UploadFile = File(...), name: str = Form(...)):
    # Perform face recognition and get face embedding
    try:
        face_embedding = DeepFace.represent(img_path=image.file, model_name='Facenet')
        
        # Store face embedding and metadata in MongoDB
        user_data = {
            "name": name,
            "face_embedding": face_embedding
        }
        users_collection.insert_one(user_data)
        
        return {"message": "Face registered successfully"}
    except Exception as e:
        return {"error": str(e)}, 500
