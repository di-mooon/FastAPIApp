from datetime import datetime

from pydantic import BaseModel, Field


class QuizCreate(BaseModel):
    question: str
    answer: str


class QuizResponse(QuizCreate):
    created: datetime


class QuizRequest(BaseModel):
    questions_num: int = Field(gt=0, le=100, default=10)
