import os

from dotenv import load_dotenv

env_file = ".dev.env"

if os.getenv("ENV") == "production":
    env_file = ".prod.env"

load_dotenv(env_file, override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
