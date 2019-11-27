import logging

from telethon.events import NewMessage, register

from core.misc import controller, handlers
from modules.nailerine.spoiling import utils_async

log = logging.getLogger(__name__)

flood = controller.anti_flood


@register(NewMessage(outgoing=True, pattern=r'(?i)spoil member_ids'))
async def spoil_member_ids(event: NewMessage.Event):
    await utils_async.do_spoil(event)


@register(NewMessage(incoming=True, pattern=r'(?i)spoil member_ids'))
@flood
async def spoil_member_ids_public(event: NewMessage.Event):
    log.warning('%s requested members spoiler in %s', event.sender_id, event.chat)
    await utils_async.do_spoil(event)


handlers.extend((spoil_member_ids,
                 spoil_member_ids_public))
