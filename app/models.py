from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database_py import Base

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True, index=True)
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, index=True)
    sender = Column(Text, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    conversation = relationship("Conversation", back_populates="messages")