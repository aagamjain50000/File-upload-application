from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class FileMetadata(Base):
    __tablename__ = "file_metadata"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    status = Column(String)  # Example: "Uploaded", "In Progress"
    upload_progress = Column(Integer)  # Progress percentage
    resumable = Column(Boolean, default=False)  # Indicates resumable upload
