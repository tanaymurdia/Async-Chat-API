from sqlalchemy.orm import Session
from app import models, schemas

def get_conversation(db: Session, conversation_id: int):
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

def get_conversations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Conversation).offset(skip).limit(limit).all()

def create_conversation(db: Session):
    db_conversation = models.Conversation()
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def create_message(db: Session, sender:str , conversation_id: int, message: schemas.MessageCreate):
    db_message = models.Message(**message.dict(), conversation_id=conversation_id, sender = sender)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message