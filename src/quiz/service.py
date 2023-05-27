from __future__ import annotations

import logging

from httpx import AsyncClient, ConnectError, ConnectTimeout, ReadTimeout

QUIZ_URL = 'https://jservice.io/api/random'

logger = logging.getLogger()


async def fetch_question_from_api(num_questions: int) -> list[dict] | None:
    try:
        async with AsyncClient() as client:
            response = await client.get(url=QUIZ_URL, params={'count': num_questions})
            logger.info(f'Success get {num_questions} questions from {QUIZ_URL}')
            return response.json()
    except (ConnectError, ConnectTimeout, ReadTimeout) as exc:
        logger.error(f'Connection error {QUIZ_URL}: {exc}')
