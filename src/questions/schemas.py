from datetime import datetime

from pydantic import BaseModel, Field


class QuestionCreate(BaseModel):
    question: str
    answer: str


class QuestionResponse(QuestionCreate):
    created: datetime


class QuizRequest(BaseModel):
    questions_num: int = Field(gt=0, le=100, default=10)
