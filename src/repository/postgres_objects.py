from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Date

Base = declarative_base()


class Snippet(Base):
    __tablename__ = "snippet"

    id = Column(Integer, primary_key=True)

    code = Column(String(36), nullable=False)
    language = Column(String)
    title = Column(String)
    description = Column(Text)
    created_at = Column(DateTime)
