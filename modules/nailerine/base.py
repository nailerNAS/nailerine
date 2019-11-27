import asyncio
from asyncio import sleep
from time import time

from telethon import TelegramClient
from telethon.events import NewMessage, register
from telethon.tl import custom
from telethon.tl.custom.dialog import Dialog
from telethon.tl.custom.message import Message

from config import zero
from core import hints, misc
from core.misc import handlers
from modules.anti_flood.controller import Controller

anti_flood = Controller().anti_flood


@register(NewMessage(outgoing=True, pattern=r'(?i)ping'))
async def ping(event: NewMessage.Event):
    before = time()
    await event.edit('pong')
    diff = time() - before
    diff = round(diff, 2)

    await event.edit(f'I replied within {diff} seconds')


# noinspection PyTypeChecker,PyUnusedLocal
@register(NewMessage(outgoing=True, pattern=r'(?i)ra$'))
async def read_all(event: NewMessage.Event):
    await event.edit('Nailerine is reading dialogs. . .')

    client: TelegramClient = event.client
    count = 0

    coros = []

    async for dialog in client.iter_dialogs():
        dialog: Dialog
        if dialog.unread_count:
            message: Message = dialog.message
            coros.append(client.send_read_acknowledge(dialog.entity, max_id=message.id))

    await asyncio.wait(coros)

    await event.edit(f'Nailerine has marked {len(coros)} dialogs as read')
    await sleep(15)
    await event.delete()


@register(NewMessage(outgoing=True, pattern=r'@all'))
async def mention_all(event: NewMessage.Event):
    client: TelegramClient = event.client
    users: hints.IntList = []

    async for user in client.iter_participants(await event.get_input_chat()):
        users.append(user.id)
        if len(users) >= 50:
            text = ''
            for user_id in users:
                text += f'<a href="tg://user?id={user_id}">{zero}</a> '
            await event.reply(text, parse_mode='html')
            users = []

    if users:
        text = ''
        for user_id in users:
            text += f'<a href="tg://user?id={user_id}">{zero}</a> '
        await event.reply(text, parse_mode='html')


@register(NewMessage(outgoing=True, pattern=r'\.kill'))
async def shutdown(event: hints.EventLike):
    await event.edit('Nailerine is shutting down, goodbye')

    try:
        misc.dp.stop_polling()

        for client in misc.clients.values():
            await client.disconnect()
    except:
        pass

    import sys
    sys.exit(1)


@register(NewMessage(outgoing=True, pattern=r'\.u$'))
async def no_u(event: hints.EventLike):
    client: TelegramClient = event.client
    if event.is_reply:
        reply_message: custom.Message = await event.get_reply_message()
        sender_id = reply_message.from_id
        await event.edit(f'no [u](tg://user?id={sender_id})')
    else:
        message = await client.get_messages(await event.get_input_chat(), max_id=event.id, limit=1)
        if message:
            message: custom.Message = message[0]
            sender_id = message.from_id
            await message.reply(f'no [u](tg://user?id={sender_id})')
            await event.delete()


@register(NewMessage(outgoing=True, pattern=r'(.+)?\.sh'))
async def replace_shrugs(event: hints.EventLike):
    text = event.text.replace('.sh', '¯\_(ツ)_/¯')
    await event.edit(text)


@register(NewMessage(outgoing=True, func=lambda e: e.raw_text == '🌚'))
async def moon_animation(event: hints.EventLike):
    moon = '🌚🌑🌒🌓🌔🌕🌝🌕🌖🌗🌘🌑🌚'
    moon += moon[::-1]
    client: TelegramClient = event.client

    async with client.action(await event.get_input_chat(), 'game'):
        last_c = event.raw_text
        for moon_c in moon:
            if moon_c == last_c:
                continue

            last_c = moon_c

            await event.edit(moon_c)
            if moon_c in ('🌝', '🌚'):
                await sleep(5)
            await sleep(0.5)


@register(NewMessage(outgoing=True, pattern=r'\.up\s(.+)'))
async def fake_update_required(event: hints.EventLike):
    text = event.pattern_match.group(1)
    await event.edit(f'[{text}](tg://need_update_for_some_feature)')


handlers.extend(
    (
        ping,
        read_all,
        mention_all,
        shutdown,
        no_u,
        replace_shrugs,
        moon_animation,
        fake_update_required,
    )
)
