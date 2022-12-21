import os

from dotenv import load_dotenv


def load_env():
    load_dotenv()
    env = {
        key: os.getenv(key)
        for key in [
            "REDIS_DB",
            "REDIS_DB_PORT",
            "REDIS_DB_URL",
        ]
    }
    return env


ENV = load_dotenv()
