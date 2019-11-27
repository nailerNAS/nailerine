from asyncio import sleep
from random import randint

from telethon import TelegramClient
from telethon.events import register, NewMessage

from core.misc import handlers


@register(NewMessage(outgoing=True, pattern=r'wom$'))
async def wipe_own_messages(event: NewMessage.Event):
    client: TelegramClient = event.client
    entity = await event.get_input_chat()
    me = await client.get_me(True)

    messages = []
    count = 0

    async for message in client.iter_messages(entity, from_user=me):
        messages.append(message)
        if len(messages) >= 100:
            await client.delete_messages(entity, messages)
            count += len(messages)
            messages = []
            await sleep(randint(1, 5))

    if messages:
        await client.delete_messages(entity, messages)
        count += len(messages)

    report = await client.send_message(me, f'Nailerine has sent {count} deletion requests')
    await sleep(15)
    await report.delete()


@register(NewMessage(outgoing=True, pattern=r'WAM$'))
async def wipe_all_messages(event: NewMessage.Event):
    client: TelegramClient = event.client
    entity = await event.get_input_chat()

    messages = []
    count = 0

    async for message in client.iter_messages(entity, reverse=True):
        messages.append(message)
        if len(messages) >= 100:
            await client.delete_messages(entity, messages)
            count += len(messages)
            messages = []
            await sleep(randint(1, 5))

    if messages:
        await client.delete_messages(entity, messages)
        count += len(messages)

    report = await event.respond(f'Nailerine has sent {count} deletion requests')
    await sleep(15)
    await report.delete()


handlers.extend((wipe_own_messages, wipe_all_messages))
