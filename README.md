# Face Recognition Project

This project uses Flask, FastAPI and DeepFace to create a Face recognition system. It allows users to register face with associated metadata, update their information and also can delete their data.

### Get started

These instructions will get you a copy of the project up and running on your local machine for development. 

### Prerequisites

This project requires Python 3.7 or later.

### Installing

1. Clone this repository to your local system using link

    ```bash
    git clone "link"
    ```

2. Navigate to the project directory:

    ```bash
    cd FaceRec
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```


### Running the Server
To start FLask and FastAPI, run the given command:
```bash
python Flaskapp.py
```

## Project Structure

- `requirements.txt`: Contains the Python dependencies for the project.
- `template/`:  Contains all the necessary HTML files to build your web pages.
- `static/`: Contains all files which is used by frontend to load data from backend.
- `Flaskapp.py`: Contains code of Flask and FastAPI application

## Database Schema

The database contains a `faceEntries` collection with the following schema:

- `id`: A unique identifier for the face entry.
- `Employeecode`: A unique  employee ID associated with the image.
- `Name`: The name of the person in the image.
- `gender`: The gender of the person.
- `Department`: The department of the person
- `time`: The time the face entry was created.
- `embeddings`: The embeddings of the face image.
- `Image`: Base64 encoded image file.

## Function Flow

1. `create_new_faceEntry()`: This function receives a POST request with an image and metadata. It extracts the face from the image, calculates the embeddings, and stores the data in the database.

2. `Data()`: This function sent a GET request  to `/data` endpoint of FastAPI app to get the list of Face Entries from MongoDB.

3. `update()` :This function is used to update the details of the face entry in the database.

4. `read()` : This function sent a GET request with specific Employeecode to read the information related to that particular Employeecode.

5. `delete()` : This function is used to delete the specific Employee Data.

