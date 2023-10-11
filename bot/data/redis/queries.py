from enum import Enum
from typing import Optional, Type, TypeVar

from pydantic import BaseModel
from redis.asyncio.client import Redis
import orjson

from .models.new_publication import NewPublicationModel
from .models.publications import CategorizedPublicationsModel
from .models.publications_pages import UpcomingPublicationsPagesModel, ArchivedPublicationsPagesModel, PagesConfigModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class RedisKeys(int, Enum):
    new_publication = 0
    categorized_publications = 1
    upcoming_publications_pages = 2
    archived_publications_pages = 3
    pages_config = 4


class RedisQueries:
    def __init__(self, redis: Redis, user_id: int = None):
        self._redis = redis
        self._user_id: Optional[int] = user_id

    def _generate_key(self, key: RedisKeys) -> str:
        match key:
            case RedisKeys.new_publication:
                return ":".join(map(str, ("new_publication", self._user_id)))
            case RedisKeys.categorized_publications:
                return ":".join(map(str, ("categorized_publications", self._user_id)))
            case RedisKeys.upcoming_publications_pages:
                return ":".join(map(str, ("upcoming_publications_pages", self._user_id)))
            case RedisKeys.archived_publications_pages:
                return ":".join(map(str, ("archived_publications_pages", self._user_id)))
            case RedisKeys.pages_config:
                return ":".join(map(str, ("pages_config", self._user_id)))

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

    async def _get_model(self, key_enum: RedisKeys, model_cls: Type[ModelType]) -> ModelType:
        model_data = await self._read(key=self._generate_key(key_enum))
        if not model_data:
            return model_cls()
        return model_cls(**model_data)

    async def _save_model(self, key_enum: RedisKeys, model: BaseModel):
        await self._write(key=self._generate_key(key_enum), data=model.model_dump())

    async def get_new_publication(self) -> NewPublicationModel:
        return await self._get_model(key_enum=RedisKeys.new_publication, model_cls=NewPublicationModel)

    async def save_new_publication(self, model: NewPublicationModel):
        await self._save_model(key_enum=RedisKeys.new_publication, model=model)

    async def get_categorized_publications(self) -> CategorizedPublicationsModel:
        return await self._get_model(key_enum=RedisKeys.categorized_publications, model_cls=CategorizedPublicationsModel)

    async def save_categorized_publications(self, model: CategorizedPublicationsModel):
        await self._save_model(key_enum=RedisKeys.categorized_publications, model=model)

    async def get_upcoming_publications_pages(self) -> UpcomingPublicationsPagesModel:
        return await self._get_model(key_enum=RedisKeys.upcoming_publications_pages, model_cls=UpcomingPublicationsPagesModel)

    async def save_upcoming_publications_pages(self, model: UpcomingPublicationsPagesModel):
        await self._save_model(key_enum=RedisKeys.upcoming_publications_pages, model=model)

    async def get_archived_publications_pages(self) -> ArchivedPublicationsPagesModel:
        return await self._get_model(key_enum=RedisKeys.archived_publications_pages, model_cls=ArchivedPublicationsPagesModel)

    async def save_archived_publications_pages(self, model: ArchivedPublicationsPagesModel):
        await self._save_model(key_enum=RedisKeys.archived_publications_pages, model=model)

    async def get_pages_config(self) -> PagesConfigModel:
        return await self._get_model(key_enum=RedisKeys.pages_config, model_cls=PagesConfigModel)

    async def save_pages_config(self, model: PagesConfigModel):
        await self._save_model(key_enum=RedisKeys.pages_config, model=model)