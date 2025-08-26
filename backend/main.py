from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil

# Create the FastAPI app instance
app = FastAPI()

# --- Directory Setup ---
# Get the path to the frontend directory
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
# Create a directory to store temporary audio files
temp_audio_dir = os.path.join(os.path.dirname(__file__), "temp_audio")
os.makedirs(temp_audio_dir, exist_ok=True)


# --- API Endpoints ---

@app.post("/api/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """
    Receives an audio file, saves it temporarily, and will eventually
    send it for transcription.
    """
    # Define the path to save the uploaded file
    file_path = os.path.join(temp_audio_dir, audio_file.filename)
    
    # Save the uploaded file to the temporary directory
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio_file.file, buffer)
    
    print(f"Successfully saved audio file to: {file_path}")
    
    # For now, we'll just return a success message.
    # In the next step, we'll process this file.
    return JSONResponse(
        status_code=200,
        content={"message": "Audio file received successfully.", "filename": audio_file.filename}
    )


# --- Serve Frontend ---
@app.get("/")
def serve_index():
    """Serves the main index.html file for the root path."""
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    """Serves other static files from the frontend directory."""
    file_path = os.path.join(frontend_dir, full_path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    # Fallback to index.html for single-page application routing
    return FileResponse(os.path.join(frontend_dir, "index.html"))