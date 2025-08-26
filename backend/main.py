from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

# Create the FastAPI app instance
app = FastAPI()

# Get the path to the frontend directory
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")

# --- API Endpoints ---

@app.get("/api")
def read_root():
    """A simple 'Hello World' endpoint to confirm the API is running."""
    return {"message": "Welcome to the SpeakWise AI API!"}


# --- Serve Frontend ---

@app.get("/")
def serve_frontend():
    """Serves the main index.html file."""
    return FileResponse(os.path.join(frontend_dir, "index.html"))