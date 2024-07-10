from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import os
import shutil
import json
import base64
import warnings
import logging

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

from transcription_service import transcribe_audio  # Correct import for transcription
from summarization_service import summarize_text  # Correct import for summarization
from timestamp_service import extract_timestamps  # Correct import for timestamps
from file_handling import save_files  # Import your save_files function

app = FastAPI()
# Directory to save results
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Pydantic model for the response
class TranscriptionResponse(BaseModel):
    transcription: str
    summary: str
    timestamps: list
    audio_file: str  # Store as base64 encoded string

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>Welcome to the Transcription and Summarization API</h1>"

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    try:
        # Save uploaded file to the results directory
        file_location = os.path.join(RESULTS_DIR, file.filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Transcription
        transcription, raw_timestamps = transcribe_audio(file_location)
        
        # Extract timestamps
        timestamps = extract_timestamps(transcription)

        # Summarization
        summary = summarize_text(transcription)

        # Read audio file as bytes
        with open(file_location, "rb") as audio_file:
            audio_bytes = audio_file.read()

        # Convert audio bytes to base64 encoded string
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

        # Save transcription, summary, and timestamps to files with meaningful names
        base_name = os.path.splitext(file.filename)[0]  # Get the base name without extension
        transcription_filename = f"{base_name}_transcription.txt"
        summary_filename = f"{base_name}_summary.txt"
        timestamps_filename = f"{base_name}_timestamps.json"

        save_files(transcription, summary, timestamps, transcription_filename, summary_filename, timestamps_filename)

        return JSONResponse(content={
            "transcription": transcription,
            "summary": summary,
            "timestamps": timestamps,
            "audio_file": audio_base64
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
