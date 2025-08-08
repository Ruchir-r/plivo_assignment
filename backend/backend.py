import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import aiohttp
import tempfile
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set your frontend url here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Helper imports for processing ----
import speech_recognition as sr
from pyannote.audio import Pipeline
from google.cloud import vision
import fitz  # PyMuPDF for PDF text extraction
import docx
from bs4 import BeautifulSoup
import requests


# --- 1. Conversation Analysis (STT + Diarization + Summary) ---
@app.post("/api/conversation")
async def conversation(file: UploadFile = File(...)):
    if file.content_type not in ["audio/wav", "audio/mpeg", "audio/mp3"]:
        raise HTTPException(status_code=400, detail="Unsupported audio format")

    # Save file temporarily
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 1. Transcription (Google Speech Recognition for demo)
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(temp_path)
    with audio_file as source:
        audio_data = recognizer.record(source)

    transcript = recognizer.recognize_google(audio_data)

    # 2. Diarization (pyannote.audio pretrained pipeline)
    # You need to set environment variable: PYANNOTE_AUTH_TOKEN for the pipeline to work or run locally with a model
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token=os.getenv("PYANNOTE_AUTH_TOKEN"))
    diarization = pipeline(temp_path)

    # Format diarization output
    diarized_text = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        diarized_text.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker,
        })

    # 3. Summarization (simple stub - just echo transcript here)
    summary = transcript[:min(len(transcript), 200)] + "..."  # Placeholder

    return {
        "transcript": transcript,
        "diarization": diarized_text,
        "summary": summary,
    }


# --- 2. Image Analysis ---
@app.post("/api/image")
async def image_analysis(file: UploadFile = File(...)):
    if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Unsupported image format")

    client = vision.ImageAnnotatorClient()

    content = await file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]

    description = ", ".join(labels)

    return {"description": description}


# --- 3. Summarization for documents and URLs ---

class SummarizeRequest(BaseModel):
    url: Optional[str] = None

@app.post("/api/summarize")
async def summarize(file: Optional[UploadFile] = File(None), req: SummarizeRequest = None):
    text = ""

    if file:
        if file.content_type == "application/pdf":
            # Extract text from PDF
            content = await file.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpf:
                tmpf.write(content)
                tmpf.flush()
                doc = fitz.open(tmpf.name)
                for page in doc:
                    text += page.get_text()
        elif file.content_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            # DOC/DOCX
            content = await file.read()
            with tempfile.NamedTemporaryFile(delete=False) as tmpf:
                tmpf.write(content)
                tmpf.flush()
                doc = docx.Document(tmpf.name)
                for para in doc.paragraphs:
                    text += para.text + "\n"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    elif req and req.url:
        # Fetch and parse URL
        async with aiohttp.ClientSession() as session:
            async with session.get(req.url) as resp:
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                text = soup.get_text()
    else:
        raise HTTPException(status_code=400, detail="No file or URL provided")

    # Dummy summary - first 300 chars (replace with real model call)
    summary = text[:300] + ("..." if len(text) > 300 else "")

    return {"summary": summary}
