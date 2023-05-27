import io

from pydub import AudioSegment

from src.constants import MP3_FORMAT, WAV_FORMAT


def save_sound_data(record_path, record_data):
    sound = AudioSegment.from_file(io.BytesIO(record_data), format=WAV_FORMAT)
    record_mp3_bytes = io.BytesIO()
    sound.export(record_mp3_bytes, format=MP3_FORMAT)
    record_mp3_bytes.seek(0)
    record_path.write_bytes(record_mp3_bytes.read())
