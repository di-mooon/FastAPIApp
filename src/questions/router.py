import logging

from fastapi import HTTPException, status
from fastapi.routing import APIRouter

from src.common.dependencies import dbSession
from src.questions.models import Question
from src.questions.schemas import QuestionCreate, QuestionResponse, QuizRequest
from src.questions.service import fetch_question_from_api

question_router = APIRouter(prefix='/questions', tags=['questions'])
logger = logging.getLogger()


@question_router.post('/', response_model=QuestionResponse)
async def create_questions(quiz_request: QuizRequest, db: dbSession):
    num_created_questions = 0
    while num_created_questions < quiz_request.questions_num:
        data = await fetch_question_from_api(num_questions=quiz_request.questions_num - num_created_questions)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='The service is temporarily unavailable'
            )
        new_questions = {}
        for question in data:
            created_question = QuestionCreate(question=question['question'], answer=question['answer'])
            new_questions[question['question']] = created_question

        exists_questions = Question.read_by_questions(db=db, questions=list(new_questions.keys()))

        async for exists_question in exists_questions:
            logger.info(f'Question "{exists_question.question}" already exists')
            del new_questions[exists_question.question]

        await Question.create(db=db, questions=list(new_questions.values()))
        num_created_questions += len(new_questions)

    logger.info(f'Created {num_created_questions} questions')
    last_question = await Question.get_last_question(db)

    return QuestionResponse(question=last_question.question, answer=last_question.answer, created=last_question.created)
