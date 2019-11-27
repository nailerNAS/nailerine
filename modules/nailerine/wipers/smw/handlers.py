import datetime

from telethon import events

from core import misc
from core.misc import hints
from modules.nailerine.wipers.smw import smw, utils
from modules.utils import find_client_name


@events.register(events.NewMessage(outgoing=True, pattern=r'\.smw\stotal\s((own|all))'))
async def smw_total(event: hints.EventLike):
    own = event.pattern_match.group(1) == 'own'
    total = await smw.get_total(event.client, await event.get_input_chat(), own)
    await event.edit(f'Nailerine SMW, {total} messages can be wiped')


@events.register(events.NewMessage(outgoing=True, pattern=r'\.smw\swipe\s((own|all))'))
async def smw_wipe(event: hints.EventLike):
    own = event.pattern_match.group(1) == 'own'
    result = await smw.wipe_seen_messages(event.client, await event.get_input_chat(), own)
    await event.respond(f'Nailerine SMW, {result} delete requests sent')


@events.register(events.NewMessage(outgoing=True, pattern=r'\.smw auto status'))
async def status_auto_smw(event: hints.EventLike):
    now = utils.ukr_time()
    next_dt: datetime = await utils.get_next_date(event.chat_id)
    if not next_dt:
        await event.edit(f'`Nailerine auto SMW is not enabled in this chat`')
        return

    delta = await utils.get_delta(event.chat_id)
    now = now.strftime(utils.fmt)
    next_dt = next_dt.strftime(utils.fmt)

    await event.edit(f'`Nailerine auto SMW, now:` **{now}**\n'
                     f'`Next date:` **{next_dt}**\n'
                     f'`Delta:` **{delta}**')


@events.register(events.NewMessage(outgoing=True, pattern=r'\.smw auto (?P<hour>\d{1,2}):(?P<minute>\d{1,2})'))
async def enable_auto_smw(event: hints.EventLike):
    hour = event.pattern_match.group('hour')
    minute = event.pattern_match.group('minute')
    client_name = find_client_name(event.client)

    await utils.enable_chat(event.chat_id, client_name, int(hour), int(minute))
    await event.edit('`Nailerine has enabled auto SMW for this chat`')


@events.register(events.NewMessage(outgoing=True, pattern=r'\.smw auto disable'))
async def disable_auto_smw(event: hints.EventLike):
    await utils.disable_chat(event.chat_id)
    await event.edit(f'`Nailerine has disabled auto SMW for this chat`')


misc.handlers.extend((smw_total,
                      smw_wipe,
                      status_auto_smw,
                      enable_auto_smw,
                      disable_auto_smw))
