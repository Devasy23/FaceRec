# Face Recognition System Proposal

## Date: 19.03.2024

### Project Team:
- [Devansh Shah](@devansh-shah-11)
- [Devasy Patel](@Devasy23)

## Project Plan

### Phase-I: Research of existing solutions
- Reviewing existing FaceRec systems
- Identifying points of improvement and defining our action plan

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

### Phase-III: Training the model
#### Tasks from Our End:
- Setup data pipeline
- Validation of Dataset
- Review specifications of the GPU
- Training a Face Recognition model
- Validating the results of the model and providing seamless inference

#### Tasks required from T.M Systems:
- Setting up a Cloud Instance for model training

### Phase-IV: Implementing Optimization Techniques
#### Tasks from Our End:

### Phase-V: Deployment
#### Tasks from Our End:
- Work on storing the model (good option is hugging face private repo) for faster loading and inference
- Provide an API endpoint for running the model prediction

#### Tasks required from T.M Systems:
- Integrate the API endpoint with frontend
- Elaborate testing on your employees to validate the model’s performance

### Phase-VI: Planning how to scale
- This phase involves planning for how to scale the FaceRec System if it is successful. This includes considering factors such as the number of users, the amount of data, and the computational requirements. 
- The deadline for this phase is June.
