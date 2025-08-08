import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from google import genai
from pypdf import PdfReader
import docx
from bs4 import BeautifulSoup
import httpx

GOOGLE_API_KEY = os.getenv("API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY environment variable")

client = genai.Client(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-1.5-flash"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://quick-chat-app-oq7b.vercel.app"],  # change to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizeRequest(BaseModel):
    url: Optional[str] = None
    message: Optional[str] = None  # fallback plain text

def extract_text_from_pdf(file_bytes) -> str:
    reader = PdfReader(file_bytes)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_text_from_docx(file_bytes) -> str:
    doc = docx.Document(file_bytes)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_html(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator="\n", strip=True)

@app.post("/api/summarize")
async def summarize(
    file: UploadFile | None = File(default=None),
    url: str | None = Form(default=None),
):
    # Extract raw text
    if file:
        contents = await file.read()
        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(contents)
        elif file.content_type in ("application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
            text = extract_text_from_docx(contents)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    elif url:
        async with httpx.AsyncClient() as client_http:
            resp = await client_http.get(url)
            if resp.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to fetch URL content")
            text = extract_text_from_html(resp.text)
    else:
        raise HTTPException(status_code=400, detail="No file or URL provided")

    prompt = f"Summarize the following text briefly:\n\n{text}"

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                "temperature": 0.2,
                "max_output_tokens": 512
            },
        )
        summary = response.text
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generative AI error: {e}")
