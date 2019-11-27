from asyncio import get_event_loop
from functools import wraps, partial
from typing import Callable, Awaitable

from telethon import TelegramClient

from core import misc


def aiowrap(fn: Callable) -> Callable[[], Awaitable]:
    @wraps(fn)
    def decorator(*args, **kwargs):
        wrapped = partial(fn, *args, **kwargs)

        return get_event_loop().run_in_executor(None, wrapped)

    return decorator


def find_client_name(client: TelegramClient):
    for name, client_ in misc.clients.items():
        if client_ == client:
            return name
