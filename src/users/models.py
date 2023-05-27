from __future__ import annotations

import uuid

from sqlalchemy import String, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(length=50),
        nullable=False,
        unique=True,
        index=True
    )
    access_token: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        default=uuid.uuid4,
        index=True
    )
    records: Mapped[list[Record]] = relationship(
        'Record',
        back_populates='user',
        cascade="save-update, merge, refresh-expire, expunge, delete, delete-orphan",
    )

    def __repr__(self):
        return f'<User "{self.name}">'

    @classmethod
    async def create(cls, db: AsyncSession, user_name: str) -> User:
        new_user = User(name=user_name)
        db.add(new_user)
        await db.flush()
        return await cls.get_by_id(db=db, user_id=new_user.id)

    @classmethod
    async def get_by_id(cls, db: AsyncSession, user_id: int) -> User | None:
        query = select(cls).where(cls.id == user_id).options(selectinload(cls.records))
        return await db.scalar(query.order_by(cls.id))

    @classmethod
    async def get_by_token(cls, db: AsyncSession, user_token: str) -> User | None:
        query = select(cls).where(cls.access_token == user_token)
        return await db.scalar(query)


from src.records.models import Record  # noqa: E402
