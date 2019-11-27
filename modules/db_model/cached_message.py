from sqlalchemy import Column, String, Integer

from .misc import Base


class CachedMessage(Base):
    __tablename__ = 'cached_messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    message_id = Column(Integer, nullable=False)
    file_id = Column(String)
    chat_name = Column(String)
    user_name = Column(String)
    text = Column(String)
