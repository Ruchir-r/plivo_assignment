import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import vision

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google Vision client requires GOOGLE_APPLICATION_CREDENTIALS env var pointing to your JSON key file
client = vision.ImageAnnotatorClient()

@app.post("/api/image")
async def analyze_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Unsupported image type")

    content = await file.read()
    image = vision.Image(content=content)

    response = client.label_detection(image=image)

    if response.error.message:
        raise HTTPException(status_code=500, detail=response.error.message)

    labels = [label.description for label in response.label_annotations]
    description = ", ".join(labels)

    return {"description": description}
