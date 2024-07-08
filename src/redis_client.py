import time

import redis.asyncio as redis

from src.config import REDIS_URL
from src.exceptions import CustomHTTPException
from src.logging import logger

MAX_RETRIES = 3

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


async def try_command(f, *args, **kwargs):
    count = 0

    while True:
        try:
            return await f(*args, **kwargs)
        except redis.ConnectionError as e:
            count += 1

            if count > MAX_RETRIES:
                logger.critical(str(e))
                raise CustomHTTPException(
                    status_code=500, reason=f"Internal Server Error: {str(e)}"
                )

            backoff = count * 5
            print(f"Retrying in {backoff} seconds")
            time.sleep(backoff)
