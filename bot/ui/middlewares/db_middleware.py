from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


class DBMiddleware(BaseMiddleware):
    def __init__(self, db_async_session: async_sessionmaker[AsyncSession]):
        super().__init__()
        self.db_async_session = db_async_session

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        data["db"] = self.db_async_session
        return await handler(event, data)
