import asyncio
import logging
from datetime import timedelta

import aiojobs
from telethon import events, utils, TelegramClient

from core import misc
from core.misc import hints
from modules.anti_flood.controller import Controller

log = logging.getLogger(__name__)

controller = Controller(threshold=3, timeout=timedelta(seconds=10))
enabled_chats = set()
tasks: hints.IntTaskDict = {}


def c_anti_mention_filter(event: hints.EventLike) -> bool:
    return all((event.chat_id in enabled_chats,
                event.mentioned))


def c_auto_am_filter(event: hints.EventLike) -> bool:
    return all((event.chat_id not in enabled_chats,
                event.mentioned))


async def hour_am(event: hints.EventLike):
    await asyncio.sleep(timedelta(hours=1).total_seconds())

    if event.chat_id in enabled_chats:
        enabled_chats.remove(event.chat_id)

    name = utils.get_display_name(await event.get_chat())

    log.info('expiring automatic anti-mention for %s', name)
    await event.respond(f"`Nailerine's automatic anti-mention mode for {name} has been disabled.`",
                        parse_mode='markdown')

    if event.chat_id in tasks:
        asyncio.create_task(tasks.pop(event.chat_id).close())


@events.register(events.NewMessage(outgoing=True, pattern=r'\.am'))
async def toggle_anti_mention(event: hints.EventLike):
    name = utils.get_display_name(await event.get_chat())

    if event.chat_id in enabled_chats:
        enabled_chats.remove(event.chat_id)
        if event.chat_id in tasks:
            await tasks.pop(event.chat_id).close()
        log.info('disabling anti-mention mode for %s', name)
        await event.edit(f'`Nailerine has disabled anti-mention mode for {name}`',
                         parse_mode='markdown')

    else:
        enabled_chats.add(event.chat_id)
        log.info('enabling anti-mention mode for %s', name)
        await event.edit(f'`Nailerine has enabled anti-mention mode for {name}`',
                         parse_mode='markdown')


@events.register(events.NewMessage(incoming=True, func=c_anti_mention_filter))
async def suppress(event: hints.EventLike):
    client: TelegramClient = event.client
    log.debug('suppressing %s', event.id)
    await client.send_read_acknowledge(await event.get_input_chat(), event, clear_mentions=True)
    await event.forward_to('me')


@events.register(events.NewMessage(incoming=True, func=c_auto_am_filter))
async def auto_am_check(event: hints.EventLike):
    if controller.is_over_limit(event.chat_id):
        enabled_chats.add(event.chat_id)
        name = utils.get_display_name(await event.get_chat())

        scheduler = await aiojobs.create_scheduler()
        await scheduler.spawn(hour_am(event))
        tasks[event.chat_id] = scheduler

        log.warning('automatic anti-mention triggered for %s', name)
        await event.reply(f"```Nailerine's automatic anti-mention mode has been enabled for {name} for one hour.\n"
                          f"This chat was a bit spammy :|```", parse_mode='markdown')
    else:
        controller.on_message_sent(event.chat_id)


misc.handlers.extend((toggle_anti_mention,
                      suppress,
                      auto_am_check))
