# Face Recognition Project

This project uses Flask, FastAPI,DeepFace and MongoDB to create a Face recognition system. It allows users to register face with associated metadata, update their information and also can delete their data.

### Get started

These instructions will get you a copy of the project up and running on your local machine for development. 

### Prerequisites

This project requires Python 3.7 or later.

### Installing

1. Clone this repository to your local system using link

    ```bash
    git clone "https://dev.azure.com/tmspl/FaceRec/_git/FaceRec-Employee-Enrollment.python"
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
python main.py
```

## Project Structure

- `requirements.txt`: Contains the Python dependencies for the project.
- `API/`: Contains code of FastAPI application.
- `FaceRec/`: Contain all files of HTML,CSS and flask application.
- `main.py`: Contains code of to start FastAPI and flask together.

## Database Schema

1. Create new connection in MongoDB and Connect using given url
   `URL: mongodb://localhost:27017/8000`

2.  Create database using 
    Database name: `DatabaseName`
    Collection name: `CollectionName`

3.  Add data by importing json file:
    From 'database.mongo' folder -> `{DatabaseName}.{CollectionName}.json`

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

# Face Recognition Project

This project uses FastAPI and DeepFace to create a face recognition system. It allows users to register faces with associated metadata, and then recognizes faces in new images.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This project requires Python 3.7 or later.

### Installing

1. Clone the repository:

    ```bash
    git clone https://gitlab.com/Devasy23/FaceRec.git
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

To start the FastAPI server, run the following command:

```bash
uvicorn main:app --reload
```

## Project Structure

- `main/`: Contains the main FastAPI application.
- `Images/`: Contains the original images and extracted faces.
- `testing/`: Contains the test cases for the application.
- `requirements.txt`: Contains the Python dependencies for the project.

## Database Schema

The database contains a `faceEntries` collection with the following schema:

- `id`: A unique identifier for the face entry.
- `age`: The age of the person.
- `gender`: The gender of the person.
- `time`: The time the face entry was created.
- `embeddings`: The embeddings of the face image.

## Function Flow

1. `create_new_faceEntry()`: This function receives a POST request with an image and metadata (age and gender). It extracts the face from the image, calculates the embeddings, and stores the data in the database.

2. `register_face()`: This function is used to store face images in the database, it is currently deprecated.
## Testing

To run the tests, use the following command:

```bash
pytest
```

## License

This project is licensed under the APACHE License - see the [LICENSE](LICENSE) file for details.
