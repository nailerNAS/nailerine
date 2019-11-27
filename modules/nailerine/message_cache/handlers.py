import logging
from html import escape

from aiogram.types import ParseMode
from telethon.events import NewMessage, MessageDeleted, register
from telethon.utils import get_display_name, pack_bot_file_id

import config
from core.hints import EventLike
from core.misc import bot, handlers
from modules.db_model.cached_message import CachedMessage
from . import utils

log = logging.getLogger(__name__)


@register(NewMessage(incoming=True, chats=config.commandos_id, blacklist_chats=True))
async def cache_message(event: EventLike):
    await utils.add_message(chat_id=event.chat_id,
                            user_id=event.sender_id,
                            message_id=event.id,
                            chat_name=get_display_name(await event.get_chat()),
                            user_name=get_display_name(await event.get_sender()),
                            text=event.raw_text,
                            file_id=pack_bot_file_id(event.media) if event.media else None)


@register(MessageDeleted)
async def revive_message(event: MessageDeleted.Event):
    for msg_id in event.deleted_ids:
        revived: CachedMessage = await utils.get_message(msg_id, event.chat_id)
        if revived:
            try:
                text = escape(revived.text) if revived.text else None
                file_id = revived.file_id
                mention = f'<a href="tg://user?id={revived.user_id}">{revived.user_name}</a>'

                text = f'{mention} at {revived.chat_name}\n{text}'

                if file_id:
                    await bot.send_document(chat_id=config.commandos_id,
                                            document=file_id,
                                            caption=text,
                                            parse_mode=ParseMode.HTML,
                                            disable_notification=True)

                else:
                    await bot.send_message(chat_id=config.commandos_id,
                                           text=text,
                                           parse_mode=ParseMode.HTML,
                                           disable_notification=True)
            except Exception as ex:
                log.exception('error during reviving %s', revived)

            finally:
                await utils.delete_message(revived.id)


handlers.extend((cache_message,
                 revive_message))
