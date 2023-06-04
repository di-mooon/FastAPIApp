import io
from uuid import UUID

from fastapi import Request
from pydub import AudioSegment

from src.constants import MP3_FORMAT, WAV_FORMAT


def save_sound_data(record_path, record_data):
    sound = AudioSegment.from_file(io.BytesIO(record_data), format=WAV_FORMAT)
    record_mp3_bytes = io.BytesIO()
    sound.export(record_mp3_bytes, format=MP3_FORMAT)
    record_mp3_bytes.seek(0)
    record_path.write_bytes(record_mp3_bytes.read())


def get_url_download_record(request: Request, record_id: UUID, user_access_token: UUID):
    protocol = 'https' if request.url.is_secure else 'http'
    app_hostname = request.url.hostname
    app_port = request.url.port
    return f"{protocol}://{app_hostname}:{app_port}/records?record_id={record_id}&user_token={user_access_token}"
