from __future__ import annotations

import logging
import sys
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor

from API import run_fastapi_app
from FaceRec.app.main import run_flask


def start_apps():
    """Starts FastAPI and Flask applications concurrently."""
    try:
        # We are using ThreadPoolExecutor for concurrent execution
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(run_flask): 'Flask',  # to start flask app
                # to start fastapi app
                executor.submit(run_fastapi_app): 'FastAPI',
            }
            # for monitoring the apps
            for future in as_completed(futures):
                app_name = futures[future]
                try:
                    future.result()  # Checks for Errors
                except Exception as e:
                    logging.error(
                        f"{app_name} application failed to start: {e}")
                    sys.exit(1)  # Exit if any application fails
    except Exception as e:
        logging.error(f"An error occurred while starting applications: {e}")


if __name__ == '__main__':
    start_apps()  # for running apps
