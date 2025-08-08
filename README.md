# Multi-Modal AI Playground

A full-stack AI Playground app with **Conversation Analysis**, **Image Analysis**, and **Document/URL Summarization**. Authenticated users can upload audio, images, and documents or provide URLs to get AI-powered insights with Google Vertex AI family of tools.

---

## Features

### 1. Authentication

* JWT-based user login.
* Token issuance and user profile retrieval.

### 2. Conversation Analysis

* Upload audio files.
* Speech-to-text transcription using an external STT vendor.
* Speaker diarization (up to 2 speakers).
* Summarization of the transcript.

### 3. Image Analysis

* Upload images.
* Generate detailed textual descriptions using Google Vertex AI models.

### 4. Document/URL Summarization

* Upload PDFs, DOC/DOCX files or provide URLs.
* Extract text from these inputs.
* Summarize content using Google Gemini API.

---

## Backend Structure

* `main.py`: The main FastAPI app mounting routers for all functionalities.
* `auth.py`: Handles authentication endpoints.
* `stt_diarization.py`: Handles audio upload, transcription, diarization, and transcript summarization.
* `image_analysis.py`: Handles image uploads and description generation.
* `summarizer.py`: Handles document/URL text extraction and summarization.
* Uses `fastapi`, `pydantic`, `passlib`, `python-jose`, `google-genai`, `pypdf`, `python-docx`, `beautifulsoup4`, and other dependencies.

---

## Frontend Structure

* React app with components for:

  * Login (`LoginPage`)
  * Conversation Analysis (upload audio, display transcript & diarization)
  * Image Analysis (upload image and show description)
  * Document/URL Summarization (upload doc/pdf or enter URL and get summary)
* Uses React state to handle JWT auth and skill selection dropdown.
* Communicates with backend API endpoints.

---
## Setup Instructions

### Backend

...

3. Set environment variables:

- `API_KEY` —  Google Vertex AI API key. - Saved for now with my free version - https://plivo-assignment-okge.onrender.com.

  **This should be saved securely in the environment variables section of Render backend service settings.**

- `SECRET_KEY` — JWT secret key (also stored in Render env vars).

...

## Deployment

- The **backend** FastAPI app is deployed on **Render**.  -  https://frontend-alpha-five-11.vercel.app/

- The **frontend** React app is deployed separately on **Vercel**.  
  The frontend should be configured to send requests to the backend URL deployed on Render.

- Both services should be launched and running simultaneously to enable full app functionality.

- **NOTE** The Render account uses the free tier so will take a few minuites to get up and running, until then the Vercel endpoints will show err-502 so some patience is unfortunately necessary.

---

## Environment Variables Summary

| Variable    | Description                      | Where to Set             |
|-------------|---------------------------------|-------------------------|
| `API_KEY`   | Google Vertex AI API key         | Render backend env vars  |
| `SECRET_KEY`| JWT signing secret key           | Render backend env vars  |
| `FRONTEND_URL` | Frontend deployment URL         | Backend CORS config      |

---

## API Endpoints

* `POST /api/token`: Authenticate user and receive JWT token.
* `GET /api/users/me`: Get logged-in user profile.
* `POST /api/stt/diarize`: Upload audio file for transcription & diarization.
* `POST /api/image/describe`: Upload image to get textual description.
* `POST /api/summarize`: Upload document or provide URL to get summary.

---

## Technologies Used

* **Backend**: FastAPI, Python, Google Vertex AI Generative Models, pypdf, python-docx, BeautifulSoup, JWT auth.
* **Frontend**: React, Vite, Fetch API.
* **Deployment**: Render / Vercel.

---

## License

MIT License

---

