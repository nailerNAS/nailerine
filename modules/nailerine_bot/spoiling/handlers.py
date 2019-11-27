from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, CallbackQuery

from core import misc
from core.misc import client_ids
from modules.nailerine.spoiling import utils_async
from modules.nailerine_bot.spoiling import utils
from modules.nailerine_bot.spoiling.spoiler_controller import SpoilerController

controller = SpoilerController()


def c_inline_filter(query: InlineQuery) -> bool:
    return query.query.startswith('spoiler ')


def c_inline_filter_v2(query: InlineQuery) -> bool:
    return all((query.from_user.id in client_ids,
                query.query.startswith('idspoiler ')))


def c_callback_filter_expand(query: CallbackQuery) -> bool:
    return query.data.startswith('spoiler ')


def c_callback_filter_collapse(query: CallbackQuery) -> bool:
    return query.data.startswith('collapse ')


@misc.dp.inline_handler(c_inline_filter)
async def send_veiled_spoiler(query: InlineQuery):
    text = query.query.replace('spoiler ', '', 1)
    spoiler_id = await utils_async.add_spoiler(text)

    markup = utils.get_expand_markup(spoiler_id)

    content = InputTextMessageContent('spoiler')
    article = InlineQueryResultArticle(id='1',
                                       title='spoiler',
                                       input_message_content=content,
                                       reply_markup=markup,
                                       description='spoiler')

    await query.answer([article])


@misc.dp.inline_handler(c_inline_filter_v2)
async def send_viled_spoiler_v2(query: InlineQuery):
    spoiler_id = int(query.query.replace('idspoiler ', '', 1))

    markup = utils.get_expand_markup(spoiler_id)

    content = InputTextMessageContent('spoiler')
    article = InlineQueryResultArticle(id='1',
                                       title='spoiler',
                                       input_message_content=content,
                                       reply_markup=markup,
                                       description='spoiler')

    await query.answer([article])


@misc.dp.callback_query_handler(c_callback_filter_expand)
async def unveil_spoiler(query: CallbackQuery):
    await controller.expand(query, misc.bot)


@misc.dp.callback_query_handler(c_callback_filter_collapse)
async def veil_spoiler(query: CallbackQuery):
    await controller.collapse(query, misc.bot)
