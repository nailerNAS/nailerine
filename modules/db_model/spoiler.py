from sqlalchemy import Column, Integer, String

from modules.db_model.misc import Base


class Spoiler(Base):
    __tablename__ = 'Spoilers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False, unique=True)
