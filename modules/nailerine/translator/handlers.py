import io
from typing import Union

from telethon import events
from telethon.events import NewMessage
from telethon.tl.custom import Message

from core import misc
from .utils import translate, Translated, Detected, detect

Event = Union[Message, NewMessage.Event]


class Patterns:
    tr_help = r'\.tr help$'
    tr_reply = r'\.tr((?P<dest>\w{2,5})(-(?P<src>\w{2,5}))?)?'
    tr_inline = r'(\.tr((?P<dest>\w{2,5})(-(?P<src>\w{2,5}))?)?) .+'
    det_reply = r'\.det$'
    det_inline = r'(\.det ).+'


async def send_translated(text: str, event: Event, dest: str = None, src: str = None):
    dest = dest or 'en'
    src = src or 'auto'

    try:
        translated: Translated = await translate(text, dest=dest, src=src)
        text = f'{translated.src}->{translated.dest}\n{translated.text}'
    except Exception as ex:
        text = str(ex)

    if len(text) >= 4096:
        with io.BytesIO() as file:
            file.name = 'translated.txt'
            file.write(text.encode())
            file.seek(0)
            await event.reply(file=file)
    else:
        if event.out:
            await event.edit(text)
        else:
            await event.reply(text)


async def send_detected(text: str, event: Event):
    try:
        detected: Detected = await detect(text)
        text = f'Language: {detected.lang}\n' \
               f'Confidence: {detected.confidence}'
    except Exception as ex:
        text = str(ex)

    if event.out:
        await event.edit(text)
    else:
        await event.reply(text)


@events.register(NewMessage(outgoing=True, pattern=Patterns.tr_help))
async def tr_help(event: Event):
    await event.edit(f'```Nailerine translator module\n\n'
                     f'.tr text\n'
                     f'.tren text\n'
                     f'.tren-uk text')


@events.register(NewMessage(outgoing=True, pattern=Patterns.tr_reply, func=lambda e: e.is_reply))
async def tr_reply(event: Event):
    reply_message = await event.get_reply_message()
    text = reply_message.raw_text
    if not text:
        await event.edit('No text found')

        return

    groups = event.pattern_match.groupdict()
    groups['text'] = text
    groups['event'] = event

    await send_translated(**groups)


@events.register(NewMessage(outgoing=True, pattern=Patterns.tr_inline, func=lambda e: not e.is_reply))
async def tr_inline(event: Event):
    text = event.raw_text.replace(event.pattern_match.group(1), '')

    if not text:
        await event.edit('No text found')

        return

    groups = event.pattern_match.groupdict()
    groups['text'] = text
    groups['event'] = event

    await send_translated(**groups)


@events.register(NewMessage(outgoing=True, pattern=Patterns.det_reply, func=lambda e: e.is_reply))
async def det_reply(event: Event):
    reply_message = await event.get_reply_message()
    text = reply_message.raw_text
    if not text:
        await event.edit('No text found')

        return

    await send_detected(text, event)


@events.register(NewMessage(outgoing=True, pattern=Patterns.det_inline, func=lambda e: not e.is_reply))
async def det_inline(event: Event):
    text = event.raw_text.replace(event.pattern_match.group(1), '')

    if not text:
        await event.edit('No text found')

        return

    await send_detected(text, event)


misc.handlers.extend((tr_help,
                      tr_reply,
                      tr_inline,
                      det_reply,
                      det_inline))
