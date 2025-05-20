from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routes import router as api_router  # Optional

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# CORS for frontend - allow access from your frontend on localhost:8080
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080" ,
                   "https://ansaar-connect-hub.vercel.app/"],  # Frontend allowed domain
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Optional: Include routes
app.include_router(api_router, prefix="/api")
