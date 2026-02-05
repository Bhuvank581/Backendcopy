from fastapi import APIRouter, UploadFile, File
from infrastructure.container import container
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


##THIS IS ALL AI CODE! NEEDS TO BE CHECKED OVER AND REFACTORED###


@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    # Read uploaded bytes (okay for small test files)
    content = await file.read()

    # Log to stdout and logger for debugging when called from your Expo frontend
    msg = f"Received upload: filename={file.filename}, content_type={file.content_type}, bytes={len(content)}"
    print(msg)
    logger.info(msg)

    # Placeholder: you can forward to a use case or save to storage here
    # repo = container.get("repository")
    # use_case = SaveAudioUseCase(repo)
    # audio_entity = await use_case.execute(filename=file.filename,
    #                                       content_type=file.content_type,
    #                                       data=content)

    return {"message": "received", "filename": file.filename, "size": len(content)}