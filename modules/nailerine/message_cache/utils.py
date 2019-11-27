from modules.db_model.cached_message import CachedMessage
from modules.db_model.context import Context
from modules.utils import aiowrap


@aiowrap
def add_message(chat_id: int,
                user_id: int,
                message_id: int,
                chat_name: str = None,
                user_name: str = None,
                text: str = None,
                file_id: str = None):
    call_args = {k: v for (k, v) in locals().items() if v}

    cm = CachedMessage(**call_args)
    with Context() as c:
        c.add(cm)


@aiowrap
def get_message(message_id: int, chat_id: int = None) -> CachedMessage:
    with Context(False) as c:
        cm: CachedMessage = (c.query(CachedMessage)
                             .filter_by(message_id=message_id,
                                        chat_id=chat_id)
                             .first())
        return cm


@aiowrap
def delete_message(id: int = None, message_id: int = None, chat_id: int = None):
    if not (id or (message_id or chat_id)):
        raise ValueError('Either id, message_id or message_id and chat_id must be specified')

    with Context() as c:
        if id:
            cm = c.query(CachedMessage).get(id)
        else:
            pre_call = {'message_id': message_id}
            if chat_id:
                pre_call['chat_id'] = chat_id
            cm = c.query(CachedMessage).filter_by(**pre_call).first()

        if cm:
            c.delete(cm)
