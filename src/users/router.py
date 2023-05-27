import logging

import sqlalchemy.exc
from fastapi import APIRouter, HTTPException, status

from src.common.dependencies import dbSession
from src.users.models import User
from src.users.schemas import UserCreate, UserResponse

user_router = APIRouter(prefix='/users', tags=['users'])

logger = logging.getLogger()


@user_router.post("/", response_model=UserResponse)
async def create_user(new_user: UserCreate, db: dbSession):
    try:
        created_user = await User.create(db=db, user_name=new_user.name)
        return UserResponse(id=created_user.id, access_token=created_user.access_token)
    except sqlalchemy.exc.IntegrityError as exc:
        logger.warning(f'User "{new_user.name}" creation error: {exc}')
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'User with the name "{new_user.name}" already exists'
        )
