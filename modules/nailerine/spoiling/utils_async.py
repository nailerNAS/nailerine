from asyncio import get_event_loop
from io import StringIO

from telethon import TelegramClient
from telethon.events import NewMessage

from config import mini_nailerine
from core import hints
from modules.nailerine.spoiling import utils_sync

loop = get_event_loop()


async def get_spoiler(id: int) -> hints.StrOrNone:
    return await loop.run_in_executor(None, utils_sync.get_spoiler, id)


async def add_spoiler(text: str) -> int:
    return await loop.run_in_executor(None, utils_sync.add_spoiler, text)


async def del_spoilers() -> int:
    return await loop.run_in_executor(None, utils_sync.del_spoilers)


async def do_spoil(event: NewMessage.Event):
    client: TelegramClient = event.client

    member_ids = [member.id for member in await client.get_participants(await event.get_input_chat())]

    string = StringIO()
    string.write('<pre>[\n')

    for member_id in member_ids:
        string.write(f'\t{member_id},\n')

    string.write(']</pre>')

    spoiler_id = await add_spoiler(string.getvalue())
    string.close()
    results = await client.inline_query(mini_nailerine, f'idspoiler {spoiler_id}')
    if results:
        await results[0].click(await event.get_input_chat())
    else:
        await event.edit('Mini Nailerine did not respond :(')
