import os.path

from fastapi import UploadFile
from pydantic import BaseModel, validator

from src.constants import MAX_FILENAME_LENGTH, WAV_FORMAT


class RecordCreate(BaseModel):
    user_id: int
    access_token: str


class RecordResponse(BaseModel):
    url: str


class UploadFileWAW(UploadFile):
    @validator('filename')
    def validate_filename(cls, filename):
        _, ext = os.path.splitext(filename)
        if ext != WAV_FORMAT:
            raise ValueError(f'File must have the "{WAV_FORMAT}" format')
        if len(filename) > {MAX_FILENAME_LENGTH}:
            raise ValueError(f'File name cannot exceed {MAX_FILENAME_LENGTH} characters')
        return filename
