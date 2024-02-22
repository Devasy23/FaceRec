from fastapi import FastAPI
import uvicorn
from API import route

Fastapp = FastAPI()
# API Router
Fastapp.include_router(route.router)

@Fastapp.get("/")
def read_root():
    return {"Hello": "FASTAPI"}

#function to run server of FastAPI
def run_fastapi_app():
    uvicorn.run(Fastapp, host="127.0.0.1", port=8000)
