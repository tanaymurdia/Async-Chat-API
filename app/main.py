from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database_py import engine, Base, SessionLocal
from typing import List
from app.llm_query import get_open_ai_resp

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/conversations/", response_model=schemas.Conversation)
async def create_conversation(db: Session = Depends(get_db)):
    return crud.create_conversation(db=db)

@app.post("/conversations/{conversation_id}/ask-message/", response_model=schemas.Message)
async def create_message(conversation_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db)):
    conversation = crud.get_conversation(db=db, conversation_id=conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    new_message = schemas.MessageCreate(content= get_open_ai_resp(conversation, message.content))
    crud.create_message(db=db, sender = "user",conversation_id=conversation_id, message=message)
    print("Message: ", message.content, new_message.content)
    return crud.create_message(db=db, sender = "chatbot",conversation_id=conversation_id, message=new_message)

@app.get("/conversations/", response_model=List[schemas.Conversation])
async def read_conversations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    conversations = crud.get_conversations(db, skip=skip, limit=limit)
    return conversations

@app.get("/conversations/{conversation_id}/", response_model=schemas.Conversation)
async def read_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = crud.get_conversation(db=db, conversation_id=conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation