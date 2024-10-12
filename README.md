<h1> Face Recognition Project </h1>

**FaceRec** is an innovative face recognition project utilizing **Flask**, **FastAPI**, **DeepFace**, and **MongoDB** to create a Face recognition system. This application empowers users to register faces along with associated metadata, update their information, and delete their data, creating a comprehensive face recognition system.

<p align="center">
    <a href="https://github.com/devansh-shah-11/FaceRec/actions/workflows/python-app.yml"><img src="https://github.com/devansh-shah-11/FaceRec/actions/workflows/python-app.yml/badge.svg" alt="Python application"></a>
    <a href="https://github.com/devansh-shah-11/FaceRec/actions/workflows/codeql.yml"><img src="https://github.com/devansh-shah-11/FaceRec/actions/workflows/codeql.yml/badge.svg" alt="CodeQL"></a>
    <a href="https://codecov.io/gh/devansh-shah-11/FaceRec"><img src="https://codecov.io/gh/devansh-shah-11/FaceRec/branch/main/graph/badge.svg" alt="codecov"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=alert_status" alt="Quality Gate Status"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=bugs" alt="Bugs"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=code_smells" alt="Code Smells"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=duplicated_lines_density" alt="Duplicated Lines (%)"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=ncloc" alt="Lines of Code"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=security_rating" alt="Security Rating"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=sqale_rating" alt="Sqale Rating"></a>
    <!-- <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=coverage" alt="Coverage"></a> -->
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=sqale_index" alt="Sqale Index"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=reliability_rating" alt="Reliability Rating"></a>
    <a href="https://sonarcloud.io/dashboard?id=Devasy23_FaceRec"><img src="https://sonarcloud.io/api/project_badges/measure?project=Devasy23_FaceRec&metric=vulnerabilities" alt="Vulnerabilities"></a>
</p>

## 🚀 Features

- **Real-Time Face Recognition:** Detect and recognize faces seamlessly in real-time.
- **User-Friendly Interface:** Easy to use with a clean design for enhanced user experience.
- **Metadata Management:** Register, update, and delete face entries with ease.
- **Scalable Architecture:** Built to handle multiple users and extensive datasets.

## 📦 Getting Started

These instructions will guide you through setting up the project on your local machine for development.

### Prerequisites

Make sure you have **Python 3.10 or later** installed.

### Installation Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Devasy23/FaceRec.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd FaceRec
   ```

3. **Install the Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

To start the Flask and FastAPI applications, run the following command:
```bash
python main.py
```

Your application will be available at `http://localhost:5000`.

<details>
<summary> <span style="font-size: 1.5em;"><strong>Project Structure</strong></span></summary>

- `requirements.txt`: Contains the Python dependencies for the project.
- `API/`: Contains the code for the FastAPI application.
- `FaceRec/`: Contains all files related to the HTML, CSS, and Flask application.
- `Model-Training/`: Contains scripts for training models.
- `docs/`: Contains documentation files.
- `test-faces/`: Contains test data for face recognition.
- `main.py`: Contains code to start both FastAPI and Flask applications.

</details>

## Function Flow

1. `create_new_faceEntry()`: Receives a POST request with an image and metadata. It extracts the face, calculates the embeddings, and stores the data in the database.
2. `Data()`: Sends a GET request to the `/data` endpoint of the FastAPI app to get the list of Face Entries from MongoDB.
3. `update()`: Updates the details of the face entry in the database.
4. `read()`: Sends a GET request with a specific `Employeecode` to read the related information.
5. `delete()`: Deletes the specific employee data.

## Sequence Diagram

![image.png](sequence-diagram.png)

## 🗄️ Database Schema

1. **Create a New Connection in MongoDB** using the following URL:
   ```
   mongodb://localhost:27017/8000
   ```

2. **Create a Database:**
   - **Database Name**: `DatabaseName`
   - **Collection Name**: `CollectionName`

3. **Import Data by Using a JSON File:**
   - From the `database.mongo` folder -> `{DatabaseName}.{CollectionName}.json`

### The `faceEntries` Collection Schema:

- `id`: A unique identifier for the face entry.
- `Employeecode`: A unique employee ID associated with the image.
- `Name`: The name of the person in the image.
- `gender`: The gender of the person.
- `Department`: The department of the person.
- `time`: The timestamp of when the face entry was created.
- `embeddings`: The embeddings of the face image.
- `Image`: Base64 encoded image file.

## 🔄 Function Flow

1. **`create_new_faceEntry()`**: Receives a POST request with an image and metadata. It extracts the face from the image, calculates the embeddings, and stores the data in the database.
  
2. **`Data()`**: Sends a GET request to the `/data` endpoint of the FastAPI app to retrieve the list of face entries from MongoDB.
  
3. **`update()`**: Updates the details of a face entry in the database.
  
4. **`read()`**: Sends a GET request with a specific `Employeecode` to retrieve related information.
  
5. **`delete()`**: Deletes a specific employee's data from the database.

## 🧪 Testing

To run the tests for this project, use the following command:
```bash
pytest
```

## 👥 Our Valuable Contributors ❤️✨
Thanks to all the amazing people who have contributed to **FaceRec**! 💖

[![Contributors](https://contrib.rocks/image?repo=Devasy23/FaceRec)](https://github.com/Devasy23/FaceRec/graphs/contributor)

## 📄 License

This project is licensed under the **APACHE License** - see the [LICENSE](LICENSE) file for details.
