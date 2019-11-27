import logging
from collections import defaultdict
from datetime import datetime, timedelta

from core import hints
from modules.anti_flood.wtf_exception import WtfException

log = logging.getLogger(__name__)


class Controller:
    __slots__ = ['_chats', '_threshold', '_timeout']

    def __init__(self, threshold: int = 2, timeout: timedelta = timedelta(minutes=2)):
        self._chats: hints.ChatDatesDict = defaultdict(list)
        self._threshold = threshold
        self._timeout = timeout

    def _validate_cache(self, chat_id: int):
        min_datetime = datetime.now() - self._timeout
        self._chats[chat_id] = [date for date in self._chats[chat_id] if date >= min_datetime]

    def is_over_limit(self, chat_id, adhoc_threshold: int = None) -> bool:
        self._validate_cache(chat_id)
        result = len(self._chats[chat_id]) >= (adhoc_threshold if adhoc_threshold else self._threshold)
        if result:
            log.warning('%s is over limit', chat_id)

        return result

    def on_message_sent(self, chat_id: int):
        self._chats[chat_id].append(datetime.now())

    def anti_flood(self, adhoc_threshold: int = None):
        def decorator(fn):
            async def wrapped(event):
                if hasattr(event, 'chat_id'):
                    chat_id = event.chat_id
                elif hasattr(event, 'sender_id'):
                    chat_id = event.sender_id
                else:
                    raise WtfException

                if not self.is_over_limit(chat_id, adhoc_threshold):
                    self.on_message_sent(chat_id)

                    return await fn(event)

            return wrapped

        return decorator
