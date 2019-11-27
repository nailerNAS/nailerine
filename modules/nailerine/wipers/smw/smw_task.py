import asyncio
import logging
from datetime import datetime, timedelta
from typing import List

from telethon import TelegramClient

from core import misc
from modules.db_model.context import Context
from modules.db_model.smw import SmwChat
from modules.nailerine.wipers.smw import smw, utils
from modules.utils import aiowrap

log = logging.getLogger(__name__)


class SmwTask:
    __slots__ = ['_running']

    def __init__(self):
        self._running = False

    async def task(self):
        if self._running:
            return

        self._running = True

        while await utils.chats_available():
            chats: List[SmwChat] = await utils.get_chats()
            for chat in chats:
                if datetime.utcnow() >= chat.next_date:
                    result = await self.wipe(chat)
                    await self.on_wipe(chat)
                    next_dt = await utils.get_next_date(chat.id)
                    log.warning('smw task has sent %s deletion requests in %s', result, chat.id)
                    await self.notify(chat, result, next_dt)
            await asyncio.sleep(timedelta(minutes=30).total_seconds())
        self._running = False

    async def wipe(self, smw_chat: SmwChat) -> int:
        client: TelegramClient = misc.clients[smw_chat.client_name]
        result = await smw.wipe_seen_messages(client, smw_chat.id, own=False)

        return result

    @aiowrap
    def on_wipe(self, smw_chat: SmwChat):
        with Context() as c:
            smw_chat: SmwChat = c.query(SmwChat).get(smw_chat.id)
            smw_chat.next_date += timedelta(days=1)

    async def notify(self, smw_chat: SmwChat, result: int, next_dt: datetime):
        client: TelegramClient = misc.clients[smw_chat.client_name]
        s_next_dt = next_dt.strftime(utils.fmt)
        await client.send_message(smw_chat.id,
                                  f'```Nailerine auto SMW, {result} delete requests sent.\n'
                                  f'Next wipe is scheduled on {s_next_dt}.```')
