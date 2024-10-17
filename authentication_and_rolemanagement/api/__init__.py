from fastapi import FastAPI

# Initialize FastAPI
app = FastAPI()

# Import routes to register them
from .auth import router as auth_router

# Include the auth router
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
