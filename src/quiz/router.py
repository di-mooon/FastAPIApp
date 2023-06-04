import logging

from fastapi import HTTPException, status
from fastapi.routing import APIRouter

from src.common.dependencies import DBSession
from src.quiz.models import Quiz
from src.quiz.schemas import QuizCreate, QuizResponse, QuizRequest
from src.quiz.service import fetch_question_from_api

quiz_router = APIRouter(prefix='/quiz', tags=['quiz'])
logger = logging.getLogger()


@quiz_router.post('/', response_model=QuizResponse)
async def create_questions(quiz_request: QuizRequest, db: DBSession):
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
            created_question = QuizCreate(question=question['question'], answer=question['answer'])
            new_questions[question['question']] = created_question

        exists_questions = Quiz.read_by_questions(db=db, questions=list(new_questions.keys()))

        async for exists_question in exists_questions:
            logger.info(f'Question "{exists_question.question}" already exists')
            del new_questions[exists_question.question]

        await Quiz.create(db=db, questions=list(new_questions.values()))
        num_created_questions += len(new_questions)

    logger.info(f'Created {num_created_questions} questions')
    last_question = await Quiz.get_last_question(db)

    return QuizResponse(question=last_question.question, answer=last_question.answer, created=last_question.created)
