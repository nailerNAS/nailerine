from telethon import events

import core
from core.misc import hints
from modules.nailerine.wipers.from_to_wiper import misc, utils
from telethon import events

import core
from core.misc import hints
from modules.nailerine.wipers.from_to_wiper import misc, utils


def is_ready(event: hints.EventLike) -> bool:
    from_ = misc.from_to_dict[event.chat_id]['from']
    to = misc.from_to_dict[event.chat_id]['to']

    return all((from_, to))


async def notify_error(event: hints.EventLike):
    from_ = misc.from_to_dict[event.chat_id]['from']
    to = misc.from_to_dict[event.chat_id]['to']

    if all((not from_, not to)):
        await event.edit('Nailerine FTW, both `from` and `to` are not set', parse_mode='markdown')
        return
    elif not from_:
        await event.edit('Nailerine FTW, `from` is not set', parse_mode='markdown')
    elif not to:
        await event.edit('Nailerine FTW, `to` is not set', parse_mode='markdown')


@events.register(events.NewMessage(outgoing=True, pattern=r'\.from', func=lambda e: e.is_reply))
async def set_from(event: hints.EventLike):
    misc.from_to_dict[event.chat_id]['from'] = event.reply_to_msg_id
    await event.edit(f'Nailerine FTW: `from` is set to {event.reply_to_msg_id}', parse_mode='markdown')


@events.register(events.NewMessage(outgoing=True, pattern=r'\.to', func=lambda e: e.is_reply))
async def set_to(event: hints.EventLike):
    misc.from_to_dict[event.chat_id]['to'] = event.reply_to_msg_id
    await event.edit(f'Nailerine FTW: `to` is set to {event.reply_to_msg_id}', parse_mode='markdown')


@events.register(events.NewMessage(outgoing=True, pattern=r'\.ftw total ((own|all))'))
async def get_total(event: hints.EventLike):
    if not is_ready(event):
        await notify_error(event)
        return

    own = event.pattern_match.group(1) == 'own'
    result = await utils.get_total(event,
                                   misc.from_to_dict[event.chat_id]['from'],
                                   misc.from_to_dict[event.chat_id]['to'],
                                   own)
    await event.edit(f'Nailerine FTW, {result} messages selected')


@events.register(events.NewMessage(outgoing=True, pattern=r'\.ftw wipe ((own|all))'))
async def from_to_wipe(event: hints.EventLike):
    if not is_ready(event):
        await notify_error(event)
        return

    own = event.pattern_match.group(1) == 'own'
    result = await utils.wipe_from_to(event,
                                      misc.from_to_dict[event.chat_id]['from'],
                                      misc.from_to_dict[event.chat_id]['to'],
                                      own)
    await event.respond(f'Nailerine FTW, {result} delete requests sent')
    misc.from_to_dict.pop(event.chat_id)


core.misc.handlers.extend((set_from, set_to, get_total, from_to_wipe))
