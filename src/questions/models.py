from __future__ import annotations

import logging
from datetime import datetime
from typing import AsyncIterator

from sqlalchemy import Text, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.questions.schemas import QuestionCreate

logger = logging.getLogger()


class Question(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime] = mapped_column(default=datetime.now)

    @classmethod
    async def create(cls, db: AsyncSession, questions: list[QuestionCreate]):
        new_questions = [Question(**question.dict()) for question in questions]
        db.add_all(new_questions)
        await db.flush()
        return new_questions

    @classmethod
    async def read_by_questions(cls, db: AsyncSession, questions: list) -> AsyncIterator[Question | None]:
        query = select(cls).filter(cls.question.in_(questions))
        stream = await db.stream_scalars(query)
        async for row in stream:
            yield row

    @classmethod
    async def get_last_question(cls, db: AsyncSession) -> Question:
        query = select(cls).order_by(cls.id.desc()).limit(1)
        return await db.scalar(query)
