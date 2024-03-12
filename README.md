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

1. Configure your database connection in `API/config.py`:
    - For local MongoDB, set `"local": "mongodb://localhost:27017/"` in the `DB_CONFIG` dictionary.
    - For MongoDB Atlas, replace `<Your MongoDB Atlas connection string here>` with your actual MongoDB Atlas connection string in the `DB_CONFIG` dictionary.
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
- `Images`: Base64 encoded image file.

## Function Flow 

1. `create_new_faceEntry()`: This function receives a POST request with an image and metadata. It extracts the face from the image, calculates the embeddings, and stores the data in the database.

2. `Data()`: This function sent a GET request  to `/data` endpoint of FastAPI app to get the list of Face Entries from MongoDB.

3. `update()` :This function is used to update the details of the face entry in the database.

4. `read()` : This function sent a GET request with specific Employeecode to read the information related to that particular Employeecode.

5. `delete()` : This function is used to delete the specific Employee Data.

## Testing

To run the tests, use the following command:

```bash
pytest
```

## License

This project is licensed under the APACHE License - see the [LICENSE](LICENSE) file for details.
## Dual Database Setup

This project supports using both a local MongoDB instance and MongoDB Atlas for database operations. This flexibility allows for easy switching between a local database for development and a cloud-based database for production or testing purposes.

To switch between the local MongoDB and MongoDB Atlas, instantiate the `Database` class with the `use_atlas` parameter set accordingly:
- For local MongoDB, use `Database(use_atlas=False)`.
- For MongoDB Atlas, use `Database(use_atlas=True)`.

Note: The `recognise_face()` API endpoint is configured to exclusively use MongoDB Atlas due to its reliance on cloud-specific features.
