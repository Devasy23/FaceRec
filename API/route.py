from __future__ import annotations

import base64
import json
import logging
import os
import re
from datetime import datetime
from io import BytesIO
from typing import List
from tensorflow.keras.models import load_model
from bson import ObjectId
from deepface import DeepFace
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import Response
from fastapi import UploadFile
from matplotlib import pyplot as plt
from PIL import Image
from pydantic import BaseModel
import numpy as np
from keras.preprocessing import image

from API.database import Database
from API.utils import init_logging_config

load_dotenv()
init_logging_config()

MONGO_URI = os.getenv('MONGO_URL1')
router = APIRouter()


client = Database()
client2 = Database(MONGO_URI, 'FaceRec')

collection = 'faceEntries'
collection2 = 'ImageDB'
collection3 = 'VectorDB'

# Models  for the data to be sent and received by the server
class Employee(BaseModel):
    EmployeeCode: int
    Name: str
    gender: str
    Department: str
    Images: list[str]


class UpdateEmployee(BaseModel):
    Name: str
    gender: str
    Department: str
    Images: list[str]

def load_and_preprocess_image(img_path, target_size=(160, 160)):
    
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

def calculate_embeddings(image_filename):
    
    """
    Calculate embeddings for the provided image.
    
    Args:
        image_filename (str): The path to the image file.
        
    Returns:
        list: A list of embeddings for the image.
    """
    
    face_image_data = DeepFace.extract_faces(
        image_filename, detector_backend='mtcnn', enforce_detection=False,
    )
    new_image_path = f'Images/Faces/tmp.jpg'
    
    if face_image_data[0]['face'] is not None:
        plt.imsave(new_image_path, face_image_data[0]['face'])
        
        img_array = load_and_preprocess_image(new_image_path)
        model=load_model('Model/embedding_trial3.h5')
        embedding = model.predict(img_array)[0]
        embedding_list = embedding.tolist()
        logging.info(f'Embedding created')
        
        return embedding_list

@router.post('/recalculate_embeddings')
async def recalculate_embeddings():
    """
    Recalculate embeddings for all the images in the database.

    Returns:
        dict: A dictionary with a success message.

    Raises:
        None
    """
    logging.info('Recalculating embeddings')
    employees_mongo = client2.find(collection2)
    for employee in employees_mongo:
        print(employee, type(employee))
        embeddings = []
        
        # In the initial version, the images were stored in the 'Image' field
        if 'Images' in employee:
            images = employee['Images']
        else:
            images = [employee['Image']]
        
        for encoded_image in images:
            
            pil_image = Image.open(BytesIO(base64.b64decode(encoded_image)))
            image_filename = f'{employee["Name"]}.png'
            pil_image.save(image_filename)
            logging.debug(f'Image saved {employee["Name"]}')
            embeddings.append(calculate_embeddings(image_filename))
            # os.remove(image_filename)

        logging.debug(f'About to update Embeddings: {embeddings}')
        # Store the data in the database
        client2.update_one(
            collection2,
            {'EmployeeCode': employee['EmployeeCode']},
            {'$set': {'embeddings': embeddings, 'Images': images}},
        )

    return {'message': 'Embeddings Recalculated successfully'}


# To create new entries of employee
@router.post('/create_new_faceEntry')
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
    logging.info('Creating new face entry')
    Name = re.sub(' +', ' ', Employee.Name).replace(
        '\r\n',
        '',
    ).replace('\n', '')
    EmployeeCode = Employee.EmployeeCode
    gender = Employee.gender.replace('\r\n', '').replace('\n', '')
    Department = Employee.Department.replace('\r\n', '').replace('\n', '')
    encoded_images = Employee.Images
    time = datetime.now()

    embeddings = []
    for encoded_image in encoded_images:
        img_recovered = base64.b64decode(encoded_image)  # decode base64string
        pil_image = Image.open(BytesIO(img_recovered))
        logging.info(f'Image opened {Name}')
        image_filename = f'{Name}.png'
        pil_image.save(image_filename)
        pil_image.save(fr'Images\dbImages\{Name}.jpg')
        logging.info(f'Face saved {Name}')
        # embedding = DeepFace.represent(
        #     image_filename, model_name='Facenet512', detector_backend='mtcnn',
        # )
        
        embeddings.append(calculate_embeddings(image_filename))
        # os.remove(image_filename)

    logging.debug(f'About to insert Embeddings: {embeddings}')
    # Store the data in the database
    client2.insert_one(
        collection2,
        {
            'EmployeeCode': EmployeeCode,
            'Name': Name,
            'gender': gender,
            'Department': Department,
            'time': time,
            'embeddings': embeddings,
            'Images': encoded_images,
        },
    )

    return {'message': 'Face entry created successfully'}


# To display all records
@router.get('/Data/', response_model=list[Employee])
async def get_employees():
    """
    Retrieve a list of employees from the database.

    Returns:
        list[Employee]: A list of Employee objects containing employee information.
    """
    logging.info('Displaying all employees')
    employees_mongo = client2.find(collection2)
    logging.info(f'Employees found {employees_mongo}')
    employees = [
        Employee(
            EmployeeCode=int(employee.get('EmployeeCode', 0)),
            Name=employee.get('Name', 'N/A'),
            gender=employee.get('gender', 'N/A'),
            Department=employee.get('Department', 'N/A'),
            Images=employee.get('Images', []),
        )
        for employee in employees_mongo
    ]
    return employees


# To display specific record info
@router.get('/read/{EmployeeCode}', response_class=Response)
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
    logging.debug(f'Display information for {EmployeeCode}')
    try:
        logging.debug(f'Start {EmployeeCode}')
        items = client2.find_one(
            collection2,
            filter={'EmployeeCode': EmployeeCode},
            projection={
                'Name': True,
                'gender': True,
                'Department': True,
                'Images': True,
                '_id': False,
            },
        )
        if items:
            json_items = json.dumps(items)
            return Response(
                content=bytes(json_items, 'utf-8'), media_type='application/json',
            )
        else:
            return Response(
                content=json.dumps({'message': 'Employee not found'}),
                media_type='application/json',
                status_code=404,
            )
    except Exception as e:
        print(e)


@router.put('/update/{EmployeeCode}', response_model=str)
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
    logging.debug(f'Updating for EmployeeCode: {EmployeeCode}')
    try:
        user_id = client2.find_one(
            collection2, {'EmployeeCode': EmployeeCode}, projection={'_id': True},
        )
        print(user_id)
        if not user_id:
            raise HTTPException(status_code=404, detail='Employee not found')
        Employee_data = Employee.model_dump(by_alias=True, exclude_unset=True)
        logging.info(f'Employee data {Employee_data}')
        # Calculate and store embeddings for the updated image array
        encoded_images = Employee.Images
        embeddings = []
        for encoded_image in encoded_images:
            img_recovered = base64.b64decode(
                encoded_image,
            )  # decode base64string
            pil_image = Image.open(BytesIO(img_recovered))
            image_filename = f'{Employee.Name}.png'
            pil_image.save(image_filename)
            logging.debug(f'Image saved {Employee.Name}')
            
            # embedding = DeepFace.represent(
            #     image_filename, model_name='Facenet', detector_backend='mtcnn',
            # )
            
            embeddings.append(calculate_embeddings(image_filename))
            # os.remove(image_filename)

        Employee_data['embeddings'] = embeddings

        try:
            update_result = client2.update_one(
                collection2,
                {'_id': ObjectId(user_id['_id'])},
                update={'$set': Employee_data},
            )
            logging.info(f'Update result {update_result}')
            if update_result.modified_count == 0:
                raise HTTPException(
                    status_code=400, detail='No data was updated',
                )
            return 'Updated Successfully'
        except Exception as e:
            raise HTTPException(
                status_code=500, detail='Internal server error',
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


# To delete employee record
@router.delete('/delete/{EmployeeCode}')
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
    logging.info('Deleting Employee')
    logging.debug(f'Deleting for EmployeeCode: {EmployeeCode}')
    client2.find_one_and_delete(collection2, {'EmployeeCode': EmployeeCode})

    return {'Message': 'Successfully Deleted'}


@router.post('/recognize_face', response_class=Response)
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
    logging.info('Recognizing Face')
    try:
        # Code to calculate embeddings via Original Facenet model
        
        img_data = await Face.read()
        image_filename = 'temp.png'
        with open(image_filename, 'wb') as f:
            f.write(img_data)
        # embedding = DeepFace.represent(
        #     img_path='temp.png', model_name='Facenet512', detector_backend='mtcnn',
        # )
        
        # Code to calculate embeddings via Finetuned Facenet model
        face_image_data = DeepFace.extract_faces(
            image_filename, detector_backend='mtcnn', enforce_detection=False,
        )
        
        if face_image_data and face_image_data[0]['face'] is not None:
            
            plt.imsave(f'Images/Faces/tmp.jpg', face_image_data[0]['face'])
            face_image_path = f'Images/Faces/tmp.jpg'
            img_array = load_and_preprocess_image(face_image_path)
            
            model = load_model('Model/embedding_trial3.h5')
            embedding_list = model.predict(img_array)[0]  # Get the first prediction
            print(embedding_list, type(embedding_list))
            embedding = embedding_list.tolist()
            result = client2.vector_search(collection3, embedding)
            logging.info(f"Result: {result[0]['Name']}, {result[0]['score']}")
            os.remove('temp.png')
            if result[0]['score'] < 0.5:
                return Response(
                    status_code=404, content=json.dumps({'message': 'No match found'}),
                )
    except Exception as e:
        logging.error(f'Error: {e}')
        os.remove('temp.png')
        raise HTTPException(status_code=500, detail='Internal server error')
    return Response(
        content=bytes(json.dumps(result[0], default=str), 'utf-8'),
        media_type='application/json',
    )
