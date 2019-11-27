from modules.db_model.misc import Session, SessionType


class Context:
    __slots__ = ['session', 'commit']

    def __init__(self, commit: bool = True):
        self.commit = commit
        self.session = Session()

    def __enter__(self) -> SessionType:
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.commit:
            self.session.commit()
        Session.remove()
