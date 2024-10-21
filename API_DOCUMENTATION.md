# API Documentation

## Overview
This document provides a detailed description of each API endpoint in the FaceRec project, including inputs, outputs, and how various scenarios are handled.

## API Endpoints

### 1. Create a New Face Entry
**Endpoint**: `/api/face-entry/create`  
**Method**: `POST`  
**Description**: Receives an image and metadata to create a new face entry.

**Request Body**:
```json
{
  "Employeecode": "string",
  "Name": "string",
  "gender": "string",
  "Department": "string",
  "Image": "base64 encoded image"
}
```

**Response**:
- **Success (201 Created)**:
  ```json
  {
    "message": "Face entry created successfully",
    "id": "unique identifier"
  }
  ```
- **Error (400 Bad Request)**:
  ```json
  {
    "error": "Invalid input data"
  }
  ```

### 2. Get All Face Entries
**Endpoint**: `/api/face-entry/data`  
**Method**: `GET`  
**Description**: Retrieves the list of all face entries.

**Response**:
- **Success (200 OK)**:
  ```json
  [
    {
      "id": "unique identifier",
      "Employeecode": "string",
      "Name": "string",
      "gender": "string",
      "Department": "string",
      "time": "timestamp",
      "embeddings": "array of numbers",
      "Image": "base64 encoded image"
    },
    ...
  ]
  ```

### 3. Update a Face Entry
**Endpoint**: `/api/face-entry/update/{Employeecode}`  
**Method**: `PUT`  
**Description**: Updates the details of an existing face entry.

**Request Body**:
```json
{
  "Name": "string",
  "gender": "string",
  "Department": "string"
}
```

**Response**:
- **Success (200 OK)**:
  ```json
  {
    "message": "Face entry updated successfully"
  }
  ```
- **Error (404 Not Found)**:
  ```json
  {
    "error": "Face entry not found"
  }
  ```

### 4. Delete a Face Entry
**Endpoint**: `/api/face-entry/delete/{Employeecode}`  
**Method**: `DELETE`  
**Description**: Deletes a specific face entry by employee code.

**Response**:
- **Success (200 OK)**:
  ```json
  {
    "message": "Face entry deleted successfully"
  }
  ```
- **Error (404 Not Found)**:
  ```json
  {
    "error": "Face entry not found"
  }
  ```

## Error Handling
- **400 Bad Request**: Returned when the input data is invalid or missing required fields.
- **404 Not Found**: Returned when the requested resource (face entry) is not found in the database.
- **500 Internal Server Error**: Returned when there is an unexpected error on the server.

## Conclusion
This documentation provides a comprehensive guide to using the FaceRec API. Following these guidelines will help ensure proper integration and usage of the API endpoints.

