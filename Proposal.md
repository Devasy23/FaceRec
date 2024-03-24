# Face Recognition System Proposal

## Date: 19.03.2024

### Project Team:
- [Devansh Shah](@devansh-shah-11)
- [Devasy Patel](@Devasy23)

## Project Plan
### Phase-I: Collection of Dataset and Requirement Setup
#### Detailed Documentation:
**Date:** JAN 05, 2024

**Phase Overview:**
The primary objective of Phase-I was to assemble a comprehensive dataset for training a robust face recognition model. The dataset's size and diversity are critical to ensuring the effectiveness of the subsequent model development phases.

**Tasks:**
1. **Dataset Acquisition and Preprocessing:**
   - Setup the camera system to capture images
   - Ensure a uniform background and lighting for all
   - Implement preprocessing steps to ensure data quality and consistency.
   - Add metadata like age, gender to help in future (for latency)

2. **Documentation:**
   - Document the sources, size, and characteristics of the collected dataset.

**Timeline:**
- Start Date: 6/1/2024
- End Date: 31/1/2024

**Collaboration with Development Team:**
To ensure seamless collaboration between our team and the development team responsible for frontend and backend tasks (80%), the following tasks and responsibilities have been outlined:
- **Data Capturing:**
   - Verify the setup and standardize the format
   - Set up the entire system to capture images of all the subjects
- **Data Storage and Processing:**
   - Setup all the Django API Endpoints related to image processing and storing, and MongoDB Database
   - Setup Django Server and handle API Endpoint up to image encoding

**Example Code Snippet:**
```python
# Assume 'image_data' is the Base64-encoded image sent as a POST request to the endpoint
image_data = request.POST.get('image')
# Decode the Base64-encoded image data to a NumPy array
img_data = base64.b64decode(image_data)
image = Image.open(io.BytesIO(img_data))
# after this point we’ll take over
# Save the image to the temp_db directory
filename = f'tm_system_{i}_image.jpg'
filepath = os.path.join(temp_db_dir, filename)
image.save(filepath)
```
#### Explanation:
1. **Endpoint Communication:**
   - The TM systems team is responsible for capturing the image and sending the Base64-encoded image data as a POST request to the designated endpoint.
2. **Image Decoding:**
   - The Django server (our team's responsibility) receives the POST request and decodes the Base64-encoded image data using the provided example snippet.
3. **Image Processing and Storage:**
   - Our team takes over from the point of image decoding.
   - Further image processing, storage, and any additional tasks are handled by our team.

**Communication:**
Weekly communication should be scheduled to take updates and maintain transparency. We look forward to a successful collaboration and the timely completion of Phase-I.
### Phase-II: Prototype Implementation
#### Tasks from Our End:
- Setup all API endpoints using FastAPI for image processing and storing
- Setup and use the MongoDB Database
- Extensive Testing
- Modifying the backend code according to frontend setup
- Changing various functionalities in backend to support multiple images for a person
- Integrating collected database in MongoDB and migrate from local to MongoDB Atlas
- Setting up Vector Search in MongoDB database
- Utility function for efficient vector search
- New Endpoint for recognizing the face

#### Tasks required from T.M Systems:
- Update the frontend code to support collection of multiple images for a single user
- Add frontend interface for testing of Vector Search using the API endpoint provided

### Phase-III: Training the Model
This phase is pivotal for the project, focusing on creating a robust and effective face recognition model through meticulous training and validation processes.

#### Key Tasks and Innovations:

1. **Triplet Loss Function Implementation**:
   - Utilizing Triplet Loss as the cornerstone of our model to enhance the accuracy in distinguishing between different individuals.
   - This involves crafting a training strategy that effectively verifies the similarity between the vector embeddings of faces.

2. **Support for Multiple Face Embeddings**:
   - Developing a system architecture capable of managing multiple embeddings per employee to boost recognition precision.
   - This will involve refining data models and possibly the vector search mechanism to handle composite embeddings data.

3. **Extended Test Coverage**:
   - The goal is to extend test coverage to 100% for all new and previously created endpoints, up from the current 86%.
   - This ensures robustness and reliability across all functionalities of the Face Recognition System.

4. **Local MongoDB Atlas Setup and Integration**:
   - Collaborating with the TM systems team for a local MongoDB Atlas setup and ensuring seamless integration with the project.
   - This also involves establishing a coherent system that supports both MongoDB and MongoDB Atlas, enhancing data management and scalability.

5. **Dockerization**:
   - Creating a dockerized version of the project and database for ease of deployment, scalability, and maintenance.
   - Dockerization will aid in ensuring compatibility and efficiency across different development and production environments.

6. **Interoperability between MongoDB and MongoDB Atlas**:
   - Ensuring a seamless flow of operations between local and cloud-based databases to optimize performance and accessibility.

#### Additional Considerations:
- **Data Pipeline Optimization**: Streamlining the data pipeline for efficient training and validation cycles.
- **Resource Allocation for Training**: Ensuring adequate computational resources are available for the training phase, including GPU specifications and cloud instances.

### Deliverables for Phase-III:
- A fully trained and validated face recognition model utilizing Triplet Loss.
- An expanded and optimized backend to support multiple embeddings per employee with robust API endpoints.
- Increased test coverage ensuring the reliability of all system components.
- A dockerized version of the project for streamlined deployment and maintenance.
- Enhanced data management systems with seamless MongoDB and MongoDB Atlas interoperability.

### Future Phases Deliverables

Following the successful completion of Phase-III, the project will proceed to subsequent phases focusing on optimization, deployment, and scalability.

#### Phase-IV: Implementing Optimization Techniques
- **Deliverables**: Enhanced system performance through optimized algorithms and codebase refinements. This phase will also focus on minimizing latency and maximizing efficiency in face recognition tasks.

#### Phase-V: Deployment
- **Deliverables**: Deployment of the face recognition system in a real-world environment with complete backend and frontend integration. This includes rigorous testing on a wider scale to validate the model's performance.

#### Tasks required from T.M Systems:
- Integrate the API endpoint with frontend
- Elaborate testing on your employees to validate the model’s performance

#### Phase-VI: Scaling the System
- **Deliverables**: A strategic plan for scaling the system to accommodate a growing number of users and data. This will involve scalable cloud services, database expansion plans, and computational resource management.
- This phase involves planning for how to scale the FaceRec System if it is successful. This includes considering factors such as the number of users, the amount of data, and the computational requirements.
- The deadline for this phase is June.
