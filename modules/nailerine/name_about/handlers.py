import asyncio

from telethon import events
from telethon.events import NewMessage

from core import misc
from core.hints import EventLike
from .task import Task


@events.register(NewMessage(outgoing=True, pattern=r'\.time$'))
async def time_status(event: EventLike):
    if Task.is_running():
        await event.edit('Time task is running')
    else:
        await event.edit('Time task is not running')


@events.register(NewMessage(outgoing=True, pattern=r'\.time (?P<mode>(on|off))$'))
async def time_toggle(event: EventLike):
    mode = event.pattern_match.group('mode') == 'on'

    if mode:
        if Task.is_running():
            await event.edit('Time task was already running')
        else:
            await asyncio.gather(Task.start(),
                                 event.edit('Time task has been started'))
    else:
        if not Task.is_running():
            await event.edit("Time task wasn't running")
        else:
            await asyncio.gather(Task.start(),
                                 event.edit('Time task has been stopped'))


misc.handlers.extend((time_status,
                      time_toggle))
