from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers from separate files (make sure you created these)
from auth import router as auth_router
from stt_diarization import router as stt_router
from image_analysis import router as image_router
from summarizer import router as summarizer_router

app = FastAPI()

# Configure CORS (adjust origins to your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.vercel.app"],  # replace with your actual frontend URL or ['*'] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(stt_router, prefix="/api")
app.include_router(image_router, prefix="/api")
app.include_router(summarizer_router, prefix="/api")
