from enum import Enum
from typing import Optional

from redis.asyncio.client import Redis
import orjson

from .models.new_publication import NewPublicationModel


class RedisKeys(int, Enum):
    new_publication = 0


class RedisQueries:
    def __init__(self, redis: Redis, user_id: int = None):
        self._redis = redis
        self._user_id: Optional[int] = user_id

    def _generate_key(self, key: RedisKeys) -> str:
        match key:
            case RedisKeys.new_publication:
                return ":".join(map(str, ("new_publication", self._user_id)))

    async def _read(self, key: str) -> dict:
        raw_result = await self._redis.get(key)
        if raw_result:
            data = orjson.loads(raw_result)
            return data
        return {}

    async def _write(self, key: str, data: dict):
        async with self._redis.pipeline() as pipe:
            await pipe.set(key, orjson.dumps(data))
            await pipe.execute()

    async def get_new_publication(self) -> NewPublicationModel:
        model = await self._read(key=self._generate_key(RedisKeys.new_publication))
        if not model:
            return NewPublicationModel()
        return NewPublicationModel(**model)

    async def save_new_publication(self, model: NewPublicationModel):
        await self._write(
            key=self._generate_key(RedisKeys.new_publication),
            data=model.model_dump())
