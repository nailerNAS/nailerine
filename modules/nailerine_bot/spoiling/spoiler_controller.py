from asyncio import sleep

from aiogram import Bot
from aiogram.types import CallbackQuery
from aiojobs import create_scheduler

from modules.nailerine.spoiling import utils_async
from modules.nailerine_bot.spoiling import utils


class SpoilerController:
    __slots__ = ['_expanders', '_tasks']

    def __init__(self):
        self._expanders = {}
        self._tasks = {}

    async def expand(self, query: CallbackQuery, bot: Bot):
        self._expanders[query.inline_message_id] = query.from_user.id

        spoiler_id = None

        try:
            spoiler_id = int(query.data.replace('spoiler ', '', 1))
        except:
            await bot.edit_message_text('Sorry, Nailerine has forgotten this spoiler')
            await query.answer('Sorry, Nailerine has forgotten this spoiler')

        spoiler_text = await utils_async.get_spoiler(spoiler_id)

        markup = utils.get_collapse_markup(spoiler_id)

        await bot.edit_message_text(text=f'Unveiled:\n{spoiler_text}',
                                    inline_message_id=query.inline_message_id,
                                    parse_mode='html',
                                    reply_markup=markup)

        await query.answer('unveiled for 30 seconds')

        if query.inline_message_id not in self._tasks:
            sch = await create_scheduler()
            await sch.spawn(self._collapser(spoiler_id, query.inline_message_id, bot))
            self._tasks[query.inline_message_id] = sch

    async def collapse(self, query: CallbackQuery, bot: Bot):
        if query.inline_message_id not in self._expanders:
            self._expanders[query.inline_message_id] = query.from_user.id
        elif self._expanders[query.inline_message_id] != query.from_user.id:
            await query.answer('you did not expand this spoiler so you cannot collapse it', show_alert=True)

            return

        spoiler_id = int(query.data.replace('collapse ', '', 1))
        markup = utils.get_expand_markup(spoiler_id)
        await bot.edit_message_text(text='spoiler',
                                    inline_message_id=query.inline_message_id,
                                    reply_markup=markup)

        if query.inline_message_id in self._tasks:
            await self._tasks.pop(query.inline_message_id).close()

        await query.answer('collapsed')

    async def _collapser(self, spoiler_id: int, inline_message_id, bot: Bot):
        await sleep(15)
        await bot.edit_message_reply_markup(inline_message_id=inline_message_id)
        await sleep(15)
        markup = utils.get_expand_markup(spoiler_id)
        await bot.edit_message_text(text='spoiler',
                                    inline_message_id=inline_message_id,
                                    reply_markup=markup)

        await self._tasks.pop(inline_message_id).close()
