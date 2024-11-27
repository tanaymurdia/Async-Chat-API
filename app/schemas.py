from pydantic import BaseModel
from typing import List

class MessageBase(BaseModel): 
    content: str

class MessageCreate(MessageBase): pass

class Message(MessageBase): 
    id: int 
    conversation_id: int 
    sender: str
    model_config = {
        "from_attributes": True
    }

class Conversation(BaseModel): 
    id: int 
    messages: List[Message] = [] 
    model_config = {
        "from_attributes": True
    }