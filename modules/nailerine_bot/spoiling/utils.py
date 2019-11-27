from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_expand_markup(id: int) -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text='expand',
                                  callback_data=f'spoiler {id}')
    markup = InlineKeyboardMarkup()
    markup.insert(button)

    return markup


def get_collapse_markup(id: int) -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text='collapse',
                                  callback_data=f'collapse {id}')
    markup = InlineKeyboardMarkup()
    markup.insert(button)

    return markup
