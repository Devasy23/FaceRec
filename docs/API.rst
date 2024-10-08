Available Endpoints
===============
1. Root Endpoint
------------------
* URL: ``/``
* Method: ``GET``
* Inputs: None
* Description: Returns a greeting message to confirm that the FastAPI server is running.
* Expected Output: ``{"Hello": "FASTAPI"}``

2. Create New Face Entry
------------------
* URL: ``/create_new_faceEntry``
* Method: ``POST``
* Inputs:
   - ``EmployeeCode`` (string): Unique identifier for the employee.
   - ``Name`` (string): Name of the employee.
   - ``gender`` (string): Gender of the employee.
   - ``Department`` (string): Department of the employee.
   - ``Images`` (list of strings): List of base64 encoded image strings.
* Description: Creates a new face entry in the database.
* Expected Output: ``{"message": "Face entry created successfully"}``
* Scenarios:
   - Success: The entry is created successfully with all required fields.
   - Failure: Missing or invalid fields result in an error.

3. Get All Face Entries
------------------
* URL: ``/Data/``
* Method: ``GET``
* Inputs: None
* Description: Retrieves all face entries from the database.
* Expected Output: List of face entries.
* Scenarios:
    - Success: Returns all entries in the database.
    - Failure: Database connection issues or no entries available.

4. Update Face Entry
------------------
* URL: ``/update/{employee_code}``
* Method: ``PUT``
* Inputs:
   - ``employee_code`` (path parameter): Employee code to identify the entry.
   - JSON body with fields to update (e.g., ``Name``, ``gender``, ``Department``, ``Images``).
* Description: Updates the specified fields of a face entry.
* Expected Output: ``{"message": "Face entry updated successfully"}``
* Scenarios:
   - Success: The entry is updated with the provided fields.
   - Failure: Invalid employee_code or fields result in an error.

5. Delete Face Entry
------------------
* URL: ``/delete/{employee_code}``
* Method: ``DELETE``
* Inputs:
   - ``employee_code`` (path parameter): Employee code to identify the entry.
* Description: Deletes a face entry from the database.
* Expected Output: ``{"message": "Face entry deleted successfully"}``
* Scenarios:
   - Success: The entry is deleted.
   - Failure: Invalid ``employee_code`` or entry does not exist.
