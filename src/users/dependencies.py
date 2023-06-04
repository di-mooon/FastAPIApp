from typing import Annotated
from uuid import UUID

from fastapi import Depends, Query, status

from src.common.dependencies import DBSession
from src.users.exceptions import UserNotFoundError
from src.users.models import User


async def get_current_user(db: DBSession, user_token: UUID = Query()) -> User:
    user = await User.get_by_token(db=db, user_token=user_token)
    if not user:
        raise UserNotFoundError(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid token')
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
