from fastapi import HTTPException


class RecordNotFoundError(HTTPException):
    pass
