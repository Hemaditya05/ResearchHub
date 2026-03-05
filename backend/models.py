from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    papers = relationship("Paper", back_populates="owner")
    chats = relationship("Chat", back_populates="user")


class Paper:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content


class Chat:
    def __init__(self, message, response):
        self.message = message
        self.response = response
