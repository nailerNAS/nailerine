import asyncio
import random

from telethon import TelegramClient

from core.misc import hints


async def get_total(event: hints.EventLike, from_: int, to: int, own: bool = True) -> int:
    client: TelegramClient = event.client
    entity = await event.get_input_chat()

    messages = await client.get_messages(entity,
                                         limit=None,
                                         from_user='me' if own else None,
                                         max_id=max(from_, to) + 1,
                                         min_id=min(from_, to) - 1)
    return len(messages)


async def wipe_from_to(event: hints.EventLike, from_: int, to: int, own: bool = False) -> int:
    client: TelegramClient = event.client
    entity = await event.get_input_chat()

    messages = []
    count = 0

    async for message in client.iter_messages(entity,
                                              from_user='me' if own else None,
                                              max_id=max(from_, to) + 1,
                                              min_id=min(from_, to) - 1):
        messages.append(message.id)
        if len(messages) >= 100:
            await client.delete_messages(entity, messages)
            count += len(messages)
            messages = []

            await asyncio.sleep(random.randint(1, 5))

    if messages:
        await client.delete_messages(entity, messages)
        count += len(messages)

    return count
