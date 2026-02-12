from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from infrastructure.config import settings
from infrastructure.container import container
from infrastructure.api.routes import health, audio
from infrastructure.persistence.in_memory_repository import InMemoryRepository
import logging
import os
import subprocess



class AudioFile(SQLModel, table=True):
    __tablename__ = "audiofiles"
    __table_args__ = {"schema": "public"}
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    filename: str
    content_type: str
    stored_filename: str 
    created_at:  datetime = Field(default_factory=datetime.utcnow)
DATABASE_URL = "postgresql+psycopg://postgres:postgres@db:5432/audiodb"

engine = create_engine(DATABASE_URL, echo=True)
    
app = FastAPI(
    title="Hexagonal API",
    description="FastAPI with Hexagonal Architecture",
    version="1.0.0",
    debug=settings.debug
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register routes
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    
@app.post("/api/v1/upload-audio")
async def upload_and_store(audio: UploadFile = File(...)):
    contents = await audio.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty upload")

    logger.info("Received upload filename=%s type=%s bytes=%d",
                audio.filename, audio.content_type, len(contents))

    # 1) Save upload to disk
    file_id = uuid4()
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}.webm")
    with open(input_path, "wb") as f:
        f.write(contents)

    # 2) Convert to MP3
    output_path = os.path.join(UPLOAD_DIR, f"{file_id}.mp3")
    try:
        convert_to_mp3(input_path, output_path)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail=f"ffmpeg failed: {e.stderr[-500:]}")



    # 4) Store in Postgres via SQLModel
    row = AudioFile(
        id=file_id,
        filename=audio.filename or "upload",
        content_type="audio/mpeg",
        stored_filename=f"{file_id}.mp3"
    )

    with Session(engine) as session:
        session.add(row)
        session.commit()


#async def convert_audio_format(receive_audio()):
    
def convert_to_mp3(input_path: str, output_path: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-i", input_path, "-vn", "-b:a", "192k", output_path],
        check=True,
        capture_output=True,
        text=True,
    )
    

# Initialize dependencies (Dependency Injection)
def _setup_dependencies():
    """Setup dependency injection container"""
    # Register repositories
    container.register("repository", InMemoryRepository())

_setup_dependencies()

app.include_router(health.router, prefix=settings.api_prefix, tags=["health"])
app.include_router(audio.router, prefix=settings.api_prefix, tags=["audio"])
