from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.utils import parse_username


async def join(client: TelegramClient, link: str):
    username, is_hash = parse_username(link)
    if is_hash:
        await client(ImportChatInviteRequest(username))
    else:
        entity = await client.get_entity(username)
        await client(JoinChannelRequest(entity))


async def leave(client: TelegramClient, link: str):
    entity = await client.get_entity(link)
    await client(LeaveChannelRequest(entity))


async def send(client: TelegramClient, link: str, text):
    await client.send_message(link, text)
