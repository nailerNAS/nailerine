from typing import Union

import sqlalchemy as sa
import sqlalchemy.ext.declarative
from sqlalchemy.orm import sessionmaker

from config import conn_string

SessionType = Union[sa.orm.Session, sa.orm.scoped_session]

engine = sa.create_engine(conn_string)
Base = sa.ext.declarative.declarative_base(engine)
Session: SessionType = sa.orm.scoped_session(sa.orm.sessionmaker(engine))
