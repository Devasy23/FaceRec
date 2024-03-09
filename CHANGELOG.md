## [0.0.1] - 2024-03-08 - 2:30

### Added
- Implemented all test cases in `test_face_cycle`
- Implemented mock test cases for `test_face_cycle` to work on online runners

## [0.1.0] - 2024-03-08 - 17:10

### Added
- Updated `create_new_faceEntry` function in [`route.py`](route/route.py) to handle multiple images for each employee.
- Updated `test_face_lifecycle` function in [`test_face_cycle.py`](testing/test_face_cycle.py) to handle multiple images for each employee in the test data.

### Changed
- Modified the `Employee` model in [`route.py`](route/route.py) to include a list of images instead of a single image.
- Adjusted the mock data and assertions in [`test_face_cycle.py`](testing/test_face_cycle.py) to handle multiple images for each employee.

### Fixed
- Resolved an issue where the `create_new_faceEntry` function in [`route.py`](route/route.py) was not correctly processing multiple images for each employee.

## [0.1.1] - 2024-03-09 - 01:00

### Added
- Added logging statements to all the API endpoints in [`route.py`](route/route.py) for easier debugging.

### Changed
- Modified the `UpdateEmployee` models in [`route.py`](route/route.py) to include a list of images instead of a single image.
- Adjusted the mock data and assertions for update data in [`test_face_cycle.py`](testing/test_face_cycle.py) to handle multiple images for each employee.

## [0.1.2] - 2024-03-09 - 22:00

### Changed
- Merged code in [`route.py`](route/route.py) and [`test_face_cycle.py`](testing/test_face_cycle.py) to improve code organization and readability. Changes made by @Devasy23.
- Split `test_face_lifecycle` function in [`test_face_cycle.py`](testing/test_face_cycle.py) into multiple smaller test cases that execute in a particularly specified order. Changes made by @Devasy23.

### Fixed
- Resolved issues in the test cases of [`test_face_cycle.py`](testing/test_face_cycle.py) to ensure they pass with the updated code structure. Fixes made by @Devasy23.

### Removed
- Removed deprecated code from various modules to improve performance and maintainability. Changes made by @Devasy23.

## [0.1.3] - 2024-03-10 - 00:51

### Added
- Created a new file [`test_face_endpoints.py`](testing/test_face_endpoints.py) to separately test each endpoint. Changes made by @Devasy23
- Split the test cases in [`test_face_cycle.py`](testing/test_face_cycle.py) into smaller tests for each endpoint.
- Added new dependencies to the [`requirements.txt`](requirements.txt) file to support the latest features and improvements.

### Fixed
- Resolved various bugs and issues identified during the testing process.

### Removed
- Removed deprecated code and unused dependencies from the project.