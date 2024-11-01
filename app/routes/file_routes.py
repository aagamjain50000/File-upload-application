from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..models import FileMetadata
from ..database import get_db
from ..utils.progress_tracker import calculate_progress
from ..utils.resumable_upload import save_file_chunk, is_file_complete

import os
import logging


router = APIRouter()

UPLOAD_DIR = "uploads"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)



# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_files(files: list[UploadFile], db: Session = Depends(get_db)):
    for file in files:
        try:
            file_path = os.path.join(UPLOAD_DIR, file.filename)

            # Read the file chunk
            file_content = await file.read()
            save_file_chunk(file_path, file_content)

            # Get the total size from headers, but check if it's present
            total_size = int(file.headers.get("content-length", len(file_content)))  # Default to the length of the read content

            # Check if the file upload is complete
            if is_file_complete(file_path, total_size):
                upload_progress = 100
                status = "Uploaded"
            else:
                upload_progress = calculate_progress(file_path, total_size)
                status = "In Progress"

            logger.info(f"Processing file: {file.filename}, Status: {status}, Progress: {upload_progress}")

            # Save or update metadata
            metadata = db.query(FileMetadata).filter_by(filename=file.filename).first()
            if metadata:
                logger.info(f"Updating metadata for {file.filename}")
                metadata.status = status
                metadata.upload_progress = upload_progress
            else:
                logger.info(f"Creating new metadata for {file.filename}")
                metadata = FileMetadata(
                    filename=file.filename, 
                    status=status, 
                    upload_progress=upload_progress, 
                    resumable=True
                )
                db.add(metadata)

            db.commit()
            logger.info(f"Metadata for {file.filename} saved successfully.")
            
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            db.rollback()  # Rollback in case of error
            raise HTTPException(status_code=500, detail=f"Error uploading file {file.filename}: {str(e)}")

    return {"message": "Files uploaded successfully"}

@router.get("/files")
async def list_files(db: Session = Depends(get_db)):
    files = os.listdir(UPLOAD_DIR)
    return {"files": [{"filename": f} for f in files]}

@router.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = os.path.join(UPLOAD_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

@router.get("/preview/{file_name}")
async def preview_file(file_name: str):
    file_path = os.path.join(UPLOAD_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(file_path, "r") as f:
        content = f.read()
    return {"content": content[:1000]}  # Preview first 1000 characters
