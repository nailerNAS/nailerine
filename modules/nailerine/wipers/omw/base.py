from datetime import timedelta

from aiojobs import create_scheduler
from telethon import TelegramClient
from telethon.events import register, NewMessage

from core import hints
from core.misc import handlers
from modules.nailerine.wipers.omw.util import omw, periodic_omw

chats: hints.OmwChats = {}


@register(NewMessage(outgoing=True, pattern=r'omw$'))
async def omw_status(event: NewMessage.Event):
    client: TelegramClient = event.client
    offset = timedelta(days=-2)

    messages = await client.get_messages(await event.get_input_chat(), limit=0, offset_date=offset)

    text = f'OMW is {"enabled" if event.chat_id in chats else "disabled"} in this chat\n'
    text += f'There are {messages.total} old messages (48 hours offset)'

    await event.edit(text)


@register(NewMessage(outgoing=True, pattern=r'omw now$'))
async def omw_now(event: NewMessage.Event):
    result = await omw(event)
    await event.edit(f'{result} messages were removed by OMW')


@register(NewMessage(outgoing=True, pattern=r'omw auto$'))
async def omw_auto(event: NewMessage.Event):
    if event.chat_id in chats:
        await chats.pop(event.chat_id).close()
        await event.edit(f'Nailerine has disabled OMW for this chat')

    else:
        chats[event.chat_id] = await create_scheduler()
        await chats[event.chat_id].spawn(periodic_omw(event, chats))
        await event.edit('Nailerine has enabled OMW for this that')


handlers.extend((omw_status, omw_now, omw_auto))
