from pydantic import BaseModel

class FileMetadataSchema(BaseModel):
    filename: str
    status: str
    upload_progress: int
    resumable: bool

    class Config:
        orm_mode = True
