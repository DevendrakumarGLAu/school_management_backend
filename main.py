import os
import django



# Set your Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  # change to your project settings path
django.setup()

from fastapi import FastAPI
from routers.api_router import api_router


app = FastAPI(title="School Management API", version="1.0")

# Include routers
app.include_router(api_router, prefix="/api_v1")

@app.get("/")
def home():
    return {"message": "Welcome to School Management API"}
