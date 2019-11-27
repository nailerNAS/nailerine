import logging
from typing import Union

from telethon import events
from telethon.events import NewMessage, MessageEdited
from telethon.tl.custom import Message
from telethon.tl.types import MessageEntityPre, MessageEntityCode

from core import misc
from .utils import paste

log = logging.getLogger(__name__)

Event = Union[NewMessage.Event, Message]


class AutoPaste:
    enabled = True


@events.register(NewMessage(outgoing=True, pattern=r'\.paste .+'))
@events.register(MessageEdited(outgoing=True, pattern=r'\.paste .+'))
async def inline_paste(event: Event):
    code = event.raw_text.replace('.paste ', '')
    url = await paste(code)
    await event.edit(url, link_preview=False)


@events.register(NewMessage(outgoing=True, pattern=r'\.paste$', func=lambda e: e.is_reply))
@events.register(MessageEdited(outgoing=True, pattern=r'\.paste$', func=lambda e: e.is_reply))
async def reply_paste(event: Event):
    reply = await event.get_reply_message()
    code = reply.raw_text
    url = await paste(code)

    if reply.out:
        await reply.edit(url, link_preview=False)
    else:
        await reply.reply(url, link_preview=False)


@events.register(NewMessage(outgoing=True))
@events.register(MessageEdited(outgoing=True))
async def auto_paste(event: Event):
    if not AutoPaste.enabled or not event.entities:
        return

    log.info('auto paste triggered for %s', event.id)

    text: str = event.raw_text
    replace_map = {}

    for entity in event.entities:
        if isinstance(entity, (MessageEntityPre, MessageEntityCode)):
            min_id = entity.offset
            max_id = min_id + entity.length

            code = text[min_id:max_id]
            url = await paste(code)
            replace_map[code] = f'({url})'

    for code, url in replace_map.items():
        text = text.replace(code, url)

    if text != event.raw_text:
        await event.edit(text)


@events.register(NewMessage(outgoing=True, pattern=r'\.ap (?P<mode>(on|off))$'))
async def auto_paste_toggle(event: Event):
    mode = event.pattern_match.group('mode') == 'on'
    AutoPaste.enabled = mode

    await event.edit('Autopaste mode is ' + ('enabled' if mode else 'disabled'))


misc.handlers.extend((inline_paste,
                      reply_paste,
                      auto_paste,
                      auto_paste_toggle))
