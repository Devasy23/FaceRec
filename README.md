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

2. `register_face()`: This function ...

## Testing

To run the tests, use the following command:

```bash
pytest
```

## License

This project is licensed under the APACHE License - see the [LICENSE](LICENSE) file for details.
