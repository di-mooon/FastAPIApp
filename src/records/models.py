from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship

from src.constants import MAX_FILENAME_LENGTH
from src.database import Base

if TYPE_CHECKING:
    from src.users.models import User


class Record(Base):
    __tablename__ = "records"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(MAX_FILENAME_LENGTH), nullable=False)
    sha256: Mapped[str] = mapped_column(String(256), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped[User] = relationship(back_populates='records')

    def __repr__(self):
        return f'<Record "{self.id}">'

    @classmethod
    async def create(cls, db: AsyncSession, user_id: int, record_name: str, record_sha256: str) -> Record:
        new_record = Record(user_id=user_id, name=record_name, sha256=record_sha256)
        db.add(new_record)
        await db.flush()
        return await cls.get_by_id(db=db, record_id=new_record.id)

    @classmethod
    async def get_by_id(cls, db: AsyncSession, record_id: str) -> Record | None:
        query = select(cls).where(cls.id == record_id)
        return await db.scalar(query)

    @classmethod
    async def get_record_by_sha256(cls, db: AsyncSession, record_sha256: str) -> Record | None:
        query = select(cls).where(cls.sha256 == record_sha256).options(joinedload(cls.user))
        return await db.scalar(query)
