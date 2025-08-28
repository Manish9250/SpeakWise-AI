from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from faster_whisper import WhisperModel
from dotenv import load_dotenv
from TTS.api import TTS
import google.generativeai as genai
import os
import shutil
import json
import uuid # Used for generating unique filenames
import torch

# --- Load Environment Variables ---
load_dotenv()

# --- Model & API Configuration ---
# Whisper Model (Speech-to-Text)
whisper_model_size = "base.en"
print("Loading Whisper model...")
try:
    whisper_model = WhisperModel(whisper_model_size, device="cpu", compute_type="int8")
    print("Whisper model loaded successfully.")
except Exception as e:
    print(f"Error loading Whisper model: {e}")
    whisper_model = None

# Coqui TTS Model (Text-to-Speech)
print("Loading Coqui XTTSv2 model...")
tts = None
try:
    # **CHANGE 1: Check if a GPU is available**
    use_gpu = torch.cuda.is_available()
    if use_gpu:
        print("GPU detected! Loading TTS model on GPU.")
    else:
        print("No GPU detected. Loading TTS model on CPU (will be slower).")

    # **CHANGE 2: Use the high-quality XTTS v2 model**
    tts_model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
    
    # **CHANGE 3: Enable GPU usage in the TTS library**
    tts = TTS(model_name=tts_model_name, progress_bar=True, gpu=use_gpu)
    print("Coqui XTTSv2 model loaded successfully.")
except Exception as e:
    print(f"Error loading Coqui TTS model: {e}")
    tts = None

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    GEMINI_API_KEY = os.getenv("GENAI_API_KEY_1") 
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.0-flash')

# --- FastAPI App Initialization ---
app = FastAPI()

# --- Directory Setup ---
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
temp_audio_dir = os.path.join(os.path.dirname(__file__), "temp_audio")
os.makedirs(temp_audio_dir, exist_ok=True)


# --- Helper Functions (No changes here) ---
def calculate_transcript_with_pauses(segments):
    final_transcript = ""
    previous_word_end_time = 0.0
    for segment in segments:
        for word in segment.words:
            start_time, end_time = word.start, word.end
            if previous_word_end_time > 0:
                pause_duration = start_time - previous_word_end_time
                if pause_duration > 0.1:
                    num_dots = int(pause_duration / 0.1)
                    final_transcript += "." * num_dots
            final_transcript += " " + word.word
            previous_word_end_time = end_time
    return final_transcript.strip()

def get_ai_feedback(transcript: str):
    prompt = f"""
    You are an expert English language tutor. A student has spoken the following sentence, including their natural pauses represented by dots(one dot is equal to 0.1 seconds).
    The user's speech: "{transcript}"

    Your task is to provide feedback in three distinct parts. Please respond with ONLY a valid JSON object with the following three keys:
    1. "conversationalReply": A natural, friendly, and conversational reply to what the user said. Do not mention that you are an AI.
    2. "phraseSuggestion": A more natural or grammatically correct way the user could have phrased their sentence.
    3. "detailedAnalysis": A brief, bulleted list explaining the specific grammatical errors or areas for improvement in the original sentence. If there are no errors, provide a compliment on their good phrasing.

    Example JSON format:
    {{
      "conversationalReply": "Oh, you're a student at IIT Madras? That's really impressive! What are you studying there?",
      "phraseSuggestion": "I'm a student at IIT Madras, pursuing a degree in Data Science.",
      "detailedAnalysis": [
        "Your sentence was grammatically correct!",
        "Using 'pursuing a degree in' sounds slightly more formal and is common in academic or professional contexts."
      ]
    }}
    """
    try:
        response = gemini_model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Error getting feedback from Gemini: {e}")
        return None

# --- API Endpoints ---
@app.post("/api/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    if whisper_model is None or tts is None:
        return JSONResponse(status_code=500, content={"error": "A required AI model is not available."})

    temp_input_path = os.path.join(temp_audio_dir, audio_file.filename)
    with open(temp_input_path, "wb") as buffer:
        shutil.copyfileobj(audio_file.file, buffer)

    try:
        segments, _ = whisper_model.transcribe(temp_input_path, word_timestamps=True)
        transcript_with_pauses = calculate_transcript_with_pauses(list(segments))

        if not transcript_with_pauses:
            return JSONResponse(status_code=400, content={"error": "No speech detected."})

        ai_feedback = get_ai_feedback(transcript_with_pauses)
        if not ai_feedback:
            return JSONResponse(status_code=500, content={"error": "Failed to get AI feedback."})

        print("Generating AI speech with Coqui TTS...")
        # **NEW**: Create a unique filename for the AI response
        unique_id = uuid.uuid4()
        temp_output_filename = f"ai_response_{unique_id}.wav"
        temp_output_path = os.path.join(temp_audio_dir, temp_output_filename)
        
        tts.tts_to_file(
            text=ai_feedback["conversationalReply"], 
            file_path=temp_output_path,
            speaker=tts.speakers[0], # Use the first default speaker
            language=tts.languages[0] # Use the first default language
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "transcript": transcript_with_pauses,
                "feedback": ai_feedback,
                "audio_filename": temp_output_filename  # **NEW**: Send the filename instead of data
            }
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to process audio."})
    finally:
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)
        # We will not delete the AI audio file here, as the frontend needs to fetch it.
        # A proper production app would have a cleanup job for old files.

# **NEW**: This endpoint serves the generated audio files
@app.get("/api/audio/{filename}")
async def get_audio_file(filename: str):
    file_path = os.path.join(temp_audio_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/wav")
    return JSONResponse(status_code=404, content={"error": "File not found"})

# --- Serve Frontend ---
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    file_path = os.path.join(frontend_dir, full_path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_dir, "index.html"))
