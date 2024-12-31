import asyncio
from typing import Any, Awaitable, Callable, Dict, MutableMapping, Optional
import time
from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, User
from cachetools import TTLCache

DEFAULT_TTL = 300  # in seconds
DEFAULT_KEY = "default"
allowed_texts = ['/start']
loop = asyncio.get_event_loop()

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(
        self,
        *,
        default_key: Optional[str] = DEFAULT_KEY,
        default_ttl: float = DEFAULT_TTL,
        **ttl_map: float,
    ) -> None:
        """
        :param default_key: The cache key to be used by default.
        Set to None to disable throttling by default.
        :param default_ttl: The TTL in default cache
        :param ttl_map: Creates additional cache instances with different TTL
        """
        if default_key:
            ttl_map[default_key] = default_ttl

        self.default_key = default_key
        self.caches: Dict[str, MutableMapping[int, None]] = {}
        self.allowed_texts = allowed_texts

        for name, ttl in ttl_map.items():
            self.caches[name] = TTLCache(maxsize=10_000, ttl=ttl)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Optional[Any]:
        user: Optional[User] = data.get("event_from_user", None)

        if user is not None:
            throttling_key = get_flag(data, "throttling_key", default=self.default_key)
            if throttling_key and event.text and event.text in self.allowed_texts:
                return await handler(event, data)

            if throttling_key and user.id in self.caches[throttling_key]:
                remaining_time = round(self.caches[throttling_key][user.id] - time.time())
                return await event.reply(f"⏳ Пожалуйста, подождите еще {remaining_time} секунд, прежде чем отправить этот запрос. . .")
            self.caches[throttling_key][user.id] = time.time() + DEFAULT_TTL

        return await handler(event, data)
