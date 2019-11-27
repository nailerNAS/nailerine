from telethon import events
from telethon.events import NewMessage, StopPropagation, MessageEdited

from core import misc
from core.hints import EventLike
from . import utils

SED_PATTERN = r'^\.s/((?:\\/|[^/])+)/((?:\\/|[^/])*)(/.*)?'


@events.register(NewMessage(outgoing=True, pattern=SED_PATTERN))
@events.register(MessageEdited(outgoing=True, pattern=SED_PATTERN))
async def sed(event: EventLike):
    message = await utils.doit(event.message, event.pattern_match)
    if message:
        utils.last_msgs[event.chat_id].append(message)

    # Don't save sed commands or we would be able to sed those
    raise StopPropagation


@events.register(NewMessage)
async def catch_all(event):
    utils.last_msgs[event.chat_id].append(event.message)


@events.register(MessageEdited)
async def catch_edit(event):
    for i, message in enumerate(utils.last_msgs[event.chat_id]):
        if message.id == event.id:
            utils.last_msgs[event.chat_id][i] = event.message


misc.handlers.extend((sed,
                      catch_all,
                      catch_edit))
