from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from telethon import TelegramClient
from telethon.tl.custom import Dialog


class Markups:
    cb = CallbackData('dialog', 'id', 'action')

    @classmethod
    async def dialogs_keyboard(cls, client: TelegramClient) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        d: Dialog
        async for d in client.iter_dialogs():
            button = InlineKeyboardButton(
                d.title,
                callback_data=cls.cb.new(id=d.id, action='s')
            )
            markup.insert(button)

        return markup
