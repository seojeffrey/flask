
from sqlalchemy import Column, String, DateTime, BigInteger
import datetime

from sqlalchemy.orm import declarative_base

from library.custom_model import EasyModel

BaseModel = declarative_base()


class User(BaseModel, EasyModel):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fullname = Column(String(50))
    email = Column(String(100), index=True, unique=True)
    password = Column(String(255))


class Board(BaseModel, EasyModel):
    __tablename__ = 'board'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner = Column(String(100), nullable=False, index=True)
    name = Column(String(50))
    create_datetime = Column(DateTime, default=datetime.datetime.utcnow(), index=True)


class BoardArticle(BaseModel, EasyModel):
    __tablename__ = 'board_article'
    id = Column(BigInteger, primary_key=True)
    board_id = Column(BigInteger, nullable=False, index=True)
    owner = Column(String(100), nullable=False, index=True)
    title = Column(String(100), nullable=False, index=True)
    content = Column(String(255))
    create_datetime = Column(DateTime, default=datetime.datetime.utcnow(), index=True)
    last_update_datetime = Column(DateTime, default=datetime.datetime.utcnow())

