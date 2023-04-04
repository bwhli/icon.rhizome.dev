import redis.asyncio as redis
from rich import inspect

from icon_rhizome_dev import ENV


class RedisClient:
    def __init__(self) -> None:
        pass

    @classmethod
    async def set(
        cls,
        key: str,
        value: str,
        ttl: int = None,
    ) -> None:
        r = await redis.from_url(ENV["REDIS_DB_URL"])
        if ttl is None:
            await r.set(key, value)
        else:
            await r.setex(key, ttl, value)
        return

    @classmethod
    async def get(cls, key: str) -> str:
        r = await redis.from_url(ENV["REDIS_DB_URL"])
        result = await r.get(key)
        return result
