import whisper

def transcribe_audio(file_path: str):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    transcription = result["text"]  # Extract the transcribed text

    # Extracting raw timestamps
    raw_timestamps = [(segment['start'], segment['end']) for segment in result["segments"]]

    return transcription, raw_timestamps
