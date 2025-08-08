import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
from pyannote.audio import Pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pyannote diarization pipeline
# Requires: set PYANNOTE_AUTH_TOKEN env variable with your Huggingface token
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token=os.getenv("PYANNOTE_AUTH_TOKEN"))

@app.post("/api/conversation")
async def conversation(file: UploadFile = File(...)):
    if file.content_type not in ["audio/wav", "audio/mpeg", "audio/mp3"]:
        raise HTTPException(status_code=400, detail="Unsupported audio format")

    # Save temp file
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # STT transcription using speech_recognition + Google STT (free tier)
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(temp_path)
    with audio_file as source:
        audio_data = recognizer.record(source)

    try:
        transcript = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        transcript = "Could not understand audio"
    except sr.RequestError as e:
        transcript = f"STT request failed; {e}"

    # Speaker diarization (up to 2 speakers)
    diarization = pipeline(temp_path)
    diarized_segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        diarized_segments.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker,
        })

    return {
        "transcript": transcript,
        "diarization": diarized_segments,
    }
