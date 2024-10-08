# 🖼️ Face Recognition Project

This project uses **Flask**, **FastAPI**, **DeepFace**, and **MongoDB** to create a face recognition system. It allows users to register faces with associated metadata, update their information, and delete their data.

<p align="center">
    <a href="https://github.com/devansh-shah-11/FaceRec/actions/workflows/python-app.yml"><img src="https://github.com/devansh-shah-11/FaceRec/actions/workflows/python-app.yml/badge.svg" alt="Python application"></a>
    <a href="https://github.com/devansh-shah-11/FaceRec/actions/workflows/codeql.yml"><img src="https://github.com/devansh-shah-11/FaceRec/actions/workflows/codeql.yml/badge.svg" alt="CodeQL"></a>
    <a href="https://codecov.io/gh/devansh-shah-11/FaceRec"><img src="https://codecov.io/gh/devansh-shah-11/FaceRec/branch/main/graph/badge.svg" alt="codecov"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=alert_status" alt="Quality Gate Status"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=bugs" alt="Bugs"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=code_smells" alt="Code Smells"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=duplicated_lines_density" alt="Duplicated Lines (%)"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec&metric=ncloc" alt="Lines of Code"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec&metric=security_rating" alt="Security Rating"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec&metric=sqale_rating" alt="Sqale Rating"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec&metric=sqale_index" alt="Sqale Index"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec&metric=reliability_rating" alt="Reliability Rating"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec&metric=vulnerabilities" alt="Vulnerabilities"></a>
</p>

## 🚀 Get Started

These instructions will get you a copy of the project up and running on your local machine for development.

### 📋 Prerequisites

This project requires **Python 3.7** or later.

### 📥 Installing

1. Clone this repository to your local system using the link:

    ```bash
    git clone https://github.com/Devasy23/FaceRec.git
    ```

2. Navigate to the project directory:

    ```bash
    cd FaceRec
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### 🏁 Running the Server

To start Flask and FastAPI, run the following command:

```bash
python main.py
```
## 📂 Project Structure

| Directory/File      | Description                                       |
|---------------------|---------------------------------------------------|
| `requirements.txt`  | Contains the Python dependencies for the project. |
| `API/`              | Contains code for the FastAPI application.       |
| `FaceRec/`          | Contains all files for the HTML, CSS, and Flask application. |
| `main.py`           | Contains code to start FastAPI and Flask together.|

## 🗄️ Database Schema

Create a new connection in MongoDB and connect using the following URL:

```arduino
URL: mongodb://localhost:27017/8000
```
Create the database using:

- **Database Name:** `DatabaseName`
- **Collection Name:** `CollectionName`

Add data by importing the JSON file from the `database.mongo` folder:

```bash
{DatabaseName}.{CollectionName}.json
```
## 🗄️ Database Schema

The database contains a `faceEntries` collection with the following schema:

| Field         | Description                                                   |
|---------------|---------------------------------------------------------------|
| `id`         | A unique identifier for the face entry.                      |
| `Employeecode` | A unique employee ID associated with the image.              |
| `Name`       | The name of the person in the image.                         |
| `gender`     | The gender of the person.                                    |
| `Department` | The department of the person.                                |
| `time`       | The time the face entry was created.                         |
| `embeddings` | The embeddings of the face image.                            |
| `Image`      | Base64 encoded image file.                                   |

## 🔄 Function Flow

1. **`create_new_faceEntry()`**: This function receives a POST request with an image and metadata. It extracts the face from the image, calculates the embeddings, and stores the data in the database.

2. **`Data()`**: This function sends a GET request to the `/data` endpoint of the FastAPI app to get the list of Face Entries from MongoDB.

3. **`update()`**: This function is used to update the details of the face entry in the database.

4. **`read()`**: This function sends a GET request with a specific Employeecode to read the information related to that particular Employeecode.

5. **`delete()`**: This function is used to delete specific employee data.

## 🧪 Testing

To run the tests, use the following command:

```bash
pytest
```
## 📜 License
This project is licensed under the APACHE License - see the LICENSE file for details.
