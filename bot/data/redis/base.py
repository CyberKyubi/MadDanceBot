from enum import Enum
from typing import Optional

from redis.asyncio.client import Redis
import redis.asyncio as aioredis


class RedisBase:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.redis: Optional[Redis] = None

    async def connect(self) -> Redis:
        self.redis = await aioredis.from_url(self.dsn)
        return self.redis

    async def disconnect(self) -> None:
        if self.redis:
            await self.redis.close()