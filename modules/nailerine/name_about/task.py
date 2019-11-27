import asyncio
import logging
from datetime import datetime

import pytz
from telethon.tl.functions.account import UpdateProfileRequest

from core import misc

log = logging.getLogger(__name__)

utc = pytz.utc
tz = pytz.timezone('Europe/Kiev')


def get_local_time() -> datetime:
    dt = datetime.utcnow()
    dt: datetime = utc.localize(dt)

    return dt.astimezone(tz)


class Task:
    _running = False
    _task = None

    @classmethod
    async def start(cls):
        if cls._running:
            return

        log.info('starting task')

        cls._running = True
        cls._task = asyncio.create_task(cls.task())

    @classmethod
    async def stop(cls):
        log.info('stopping task')

        cls._task.cancel()
        await cls._task
        cls._task = None
        cls._running = False

    @classmethod
    def is_running(cls) -> bool:
        return cls._running

    @classmethod
    async def task(cls):
        fmt = '%H:%M'
        prev = ''
        while True:
            curr = get_local_time().strftime(fmt)
            if curr != prev:
                log.debug('updating abouts names to %s', curr)
                prev = curr
                for client in misc.clients.values():
                    await client(UpdateProfileRequest(about=f'{curr} EEST'))
            await asyncio.sleep(5)


misc.startup_funcs.append(Task.start)
