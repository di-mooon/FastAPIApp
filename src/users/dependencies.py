from typing import Annotated

from fastapi import Depends, Query, status

from src.common.dependencies import dbSession
from src.users.exceptions import UserNotFoundError
from src.users.models import User


async def get_current_user(db: dbSession, user_token: str = Query()) -> User:
    user = await User.get_by_token(db=db, user_token=user_token)
    if not user:
        raise UserNotFoundError(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid token')
    return user

currentUser = Annotated[User, Depends(get_current_user)]
