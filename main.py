from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from API import run_fastapi_app
from FaceRec.app.main import run_flask

# Initialize logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to run Flask app with exception handling
def run_flask_app():
    try:
        run_flask()
    except Exception as e:
        logger.error(f"Error starting Flask app: {e}")

# Function to run FastAPI app with exception handling
def run_fastapi_app_with_handling():
    try:
        run_fastapi_app()
    except Exception as e:
        logger.error(f"Error starting FastAPI app: {e}")

# Multithreading used to start both FastAPI and Flask apps at the same time.
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_flask_app)
        executor.submit(run_fastapi_app_with_handling)
