import builtins
import logging
import os
from functools import lru_cache

import rich
from dotenv import load_dotenv

# Replace built-in print with Rich's print.
builtins.print = rich.print


@lru_cache(maxsize=1)
def load_env():
    load_dotenv()
    return {
        "ABLY_PUBLISH_KEY": os.getenv("ABLY_PUBLISH_KEY"),
        "AWS_ACCESS_KEY": os.getenv("AWS_ACCESS_KEY"),
        "AWS_SECRET_KEY": os.getenv("AWS_SECRET_KEY"),
        "ENV": os.getenv("ENV"),
        "ICON_API_ENDPOINT": os.getenv("ICON_API_ENDPOINT"),
        "REDIS_DB": os.getenv("REDIS_DB"),
        "REDIS_DB_PORT": os.getenv("REDIS_DB_PORT"),
        "REDIS_DB_URL": os.getenv("REDIS_DB_URL"),
    }


ENV = load_env()

# Logging configuration.
logging.getLogger("faker").setLevel(logging.ERROR)
if ENV["ENV"] == "production":
    logging.basicConfig(level=logging.WARN)
else:
    logging.basicConfig(level=logging.DEBUG)
