from __future__ import annotations

import logging

import uvicorn
from fastapi import FastAPI, HTTPException

from API import route

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Fastapp = FastAPI()

# API Router
Fastapp.include_router(route.router)


@Fastapp.get("/")
def read_root():
    try:
        return {"Hello": "FASTAPI"}
    except Exception as e:
        logger.error(f"Error in root endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Function to run FastAPI server
def run_fastapi_app():
    try:
        uvicorn.run(Fastapp, host="127.0.0.1", port=8000)
    except Exception as e:
        logger.error(f"Error starting FastAPI server: {e}")
        raise
