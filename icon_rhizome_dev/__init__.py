import os
from functools import lru_cache

from dotenv import load_dotenv


@lru_cache(maxsize=1)
def load_env():
    load_dotenv()
    return {
        "ABLY_PUBLISH_KEY": os.getenv("ABLY_PUBLISH_KEY"),
        "AWS_ACCESS_KEY": os.getenv("AWS_ACCESS_KEY"),
        "AWS_SECRET_KEY": os.getenv("AWS_SECRET_KEY"),
        "ICON_API_ENDPOINT": os.getenv("ICON_API_ENDPOINT"),
        "REDIS_DB": os.getenv("REDIS_DB"),
        "REDIS_DB_PORT": os.getenv("REDIS_DB_PORT"),
        "REDIS_DB_URL": os.getenv("REDIS_DB_URL"),
    }


ENV = load_env()
