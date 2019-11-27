from modules.db_model.context import Context
from modules.db_model.spoiler import Spoiler
from core import hints


def get_spoiler(id: int) -> hints.StrOrNone:
    ret = None

    with Context() as c:
        spoiler = c.query(Spoiler).get(id)
        if spoiler:
            c.expunge_all()
            ret = spoiler.text

    return ret


def add_spoiler(text: str) -> int:
    with Context() as c:
        spoiler = c.query(Spoiler).filter_by(text=text).first()
        if not spoiler:
            spoiler = Spoiler(text=text)
            c.add(spoiler)
            c.commit()

        id = spoiler.id
        return id


def del_spoilers() -> int:
    count = 0

    with Context() as c:
        for spoiler in c.query(Spoiler).all():
            c.delete(spoiler)
            count += 1

    return count
