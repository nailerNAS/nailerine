from sqlalchemy import Column, Integer, String, DateTime

from modules.db_model.misc import Base


class SmwChat(Base):
    __tablename__ = 'smw_chats'

    id = Column(Integer, primary_key=True, autoincrement=False)
    next_date = Column(DateTime, nullable=False)
    client_name = Column(String, nullable=False)
