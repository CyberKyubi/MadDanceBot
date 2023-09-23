from enum import Enum
from typing import Optional


from redis.asyncio.client import Redis
import redis.asyncio as aioredis


class RedisKeys(int, Enum):
    new_publication = 0


class RedisStorage:
    def __init__(self, dsn: str):
        self.dsn = dsn

        self._redis: Optional[Redis] = None

    async def connect(self):
        self._redis = await aioredis.from_url(self.dsn)

    async def disconnect(self) -> None:
        if self._redis:
            await self._redis.close()

    async def _generate_key(self, key: RedisKeys):
        match key:
            case RedisKeys.new_publication:
                return