import asyncio

from core import misc
from modules.nailerine.wipers.smw.misc import task

loop = asyncio.get_event_loop()


async def startup():
    loop.create_task(task.task())


misc.startup_funcs.append(startup())
