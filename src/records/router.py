import logging
import os.path
from hashlib import sha256
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, UploadFile, status
from fastapi.responses import FileResponse

from config.config import BASE_DIR
from src.common.dependencies import DBSession
from src.constants import MP3_FORMAT
from src.records.exceptions import RecordNotFoundError
from src.records.models import Record
from src.records.schemas import RecordResponse
from src.records.service import save_sound_data, get_url_download_record
from src.users.dependencies import CurrentUser

record_router = APIRouter(prefix='/records', tags=['records'])

logger = logging.getLogger()

RECORDS_DIR = BASE_DIR / 'sounds'
RECORDS_DIR.mkdir(exist_ok=True)


@record_router.post("/", response_model=RecordResponse)
async def add_record(user: CurrentUser, file: UploadFile, request: Request, db: DBSession):
    file_data = await file.read()
    record_sha256 = sha256(file_data).hexdigest()
    record_path = RECORDS_DIR / record_sha256

    if not record_path.exists():
        try:
            save_sound_data(record_path=record_path, record_data=file_data)
        except Exception as exc:
            logger.error(f'File save error: {exc}')
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid file')

    created_record = await Record.get_by_sha256(db=db, record_sha256=record_sha256)

    if not created_record or created_record and created_record.user_id != user.id:
        filename, ext = os.path.splitext(file.filename)
        created_record = await Record.create(
            db=db,
            user_id=user.id,
            record_name=f'{filename}.{MP3_FORMAT}',
            record_sha256=record_sha256
        )

    url = get_url_download_record(request=request, record_id=created_record.id, user_access_token=user.access_token)
    return {"url": url}


@record_router.get("/", response_class=FileResponse)
async def download_record(user: CurrentUser, record_id: UUID, db: DBSession):
    record = await Record.get_by_id(db=db, record_id=record_id)
    if not record:
        raise RecordNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail='Record not found')

    record_path = RECORDS_DIR / record.sha256
    if not record_path.exists():
        raise RecordNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail='Record not found')

    if record.user_id != user.id:
        raise RecordNotFoundError(status_code=status.HTTP_403_FORBIDDEN, detail='No record access')

    return FileResponse(filename=record.name, path=record_path)
