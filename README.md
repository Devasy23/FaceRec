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
- `Images`: Base64 encoded image file.

## Function Flow 

1. `create_new_faceEntry()`: This function receives a POST request with an image and metadata. It extracts the face from the image, calculates the embeddings, and stores the data in the database.

2. `Data()`: This function sent a GET request  to `/data` endpoint of FastAPI app to get the list of Face Entries from MongoDB.

3. `update()` :This function is used to update the details of the face entry in the database.

4. `read()` : This function sent a GET request with specific Employeecode to read the information related to that particular Employeecode.

5. `delete()` : This function is used to delete the specific Employee Data.
## Local MongoDB Atlas Setup Using Docker

To facilitate development and testing, you can run MongoDB Atlas locally using Docker. This setup mimics the cloud environment and allows for easy switching between local and cloud databases.

### Initial Setup

1. Ensure Docker is installed on your system. If not, download and install Docker from [Docker's official website](https://www.docker.com/products/docker-desktop).

2. Navigate to the `API` directory where the `Dockerfile` and `docker-compose.yml` files are located.

3. Build and run the Docker container with the following command:
    ```bash
    docker-compose up --build
    ```
    This command builds the MongoDB image and runs it as a container. The MongoDB service will be accessible on `localhost:27017`.

### Switching Between Local and Cloud MongoDB Atlas

To switch between the local MongoDB instance and a cloud MongoDB Atlas instance, modify the initialization of the `Database` class in `API/database.py`.

- For local MongoDB, set `use_local` to `True`:
    ```python
    db = Database(db_name="YourDatabaseName", use_local=True)
    ```

- For cloud MongoDB Atlas, set `use_local` to `False` and replace `"your_cloud_mongodb_atlas_uri"` with your actual MongoDB Atlas URI:
    ```python
    db = Database(db_name="YourDatabaseName", use_local=False)
    ```

### Troubleshooting

- If you encounter any issues with the Docker container, ensure Docker is running and try rebuilding the container.
- For connection issues, verify that the MongoDB URI in `API/database.py` is correctly set according to your setup (local or cloud).

This setup allows for a flexible development environment, closely mirroring the production setup without the need for external MongoDB hosting during development.
## Testing

To run the tests, use the following command:

```bash
pytest
```

## License

This project is licensed under the APACHE License - see the [LICENSE](LICENSE) file for details.
