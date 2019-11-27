from asyncio import sleep
from datetime import timedelta
from random import randint

from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.patched import MessageService

from core import hints


async def omw(event: NewMessage.Event) -> int:
    client: TelegramClient = event.client
    offset = timedelta(days=-2)

    messages = []
    count = 0

    async for message in client.iter_messages(await event.get_input_chat(), offset_date=offset):
        if not isinstance(message, MessageService):
            messages.append(message)
            if len(messages) >= 100:
                await client.delete_messages(await event.get_input_chat(), messages)
                count += len(messages)
                messages = []
                await sleep(randint(1, 5))

    if messages:
        await client.delete_messages(await event.get_input_chat(), messages)
        count += len(messages)

    return count


async def periodic_omw(event: NewMessage.Event, chats: hints.OmwChats):
    while event.chat_id in chats:
        result = await omw(event)
        if result:
            await event.respond(f'OMW has just deleted {result} messages (48 hours offset)')
        delta = timedelta(hours=1)
        await sleep(delta.total_seconds())
