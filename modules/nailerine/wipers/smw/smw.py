import asyncio
import random

from telethon import TelegramClient
from telethon.hints import EntityLike
from telethon.tl import custom


async def get_point(client: TelegramClient, entity: EntityLike, own: bool = True) -> int:
    all_ids = [user.id for user in await client.get_participants(entity)]
    got_ids = []

    point = -1

    async for message in client.iter_messages(entity):
        message: custom.Message
        if message.from_id not in got_ids:
            got_ids.append(message.from_id)
            if set(all_ids).issubset(got_ids):
                point = message.id
                break

    return point


async def get_total(client: TelegramClient, entity: EntityLike, own: bool = True) -> int:
    point = await get_point(client, entity, own)
    messages = await client.get_messages(entity,
                                         limit=0,
                                         from_user='me' if own else None,
                                         max_id=point)
    return messages.total


async def wipe_seen_messages(client: TelegramClient, entity: EntityLike, own: bool = True) -> int:
    point = await get_point(client, entity, own)

    messages = []
    count = 0

    async for message in client.iter_messages(entity,
                                              from_user='me' if own else None,
                                              max_id=point,
                                              reverse=True):
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
