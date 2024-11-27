import asyncio
from fastapi import FastAPI
import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database_py import Base, engine
from httpx import AsyncClient

SQLITE_TEST_DATABASE_URL = "sqlite:///:memory:"
TestEngine = create_engine(
    SQLITE_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestEngine)

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=TestEngine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=TestEngine)

@pytest_asyncio.fixture(scope="function")
async def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_conversation(client):
    response = await client.post("/conversations/")
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_conversations_empty(client):
    response = await client.get("/conversations/")
    assert response.status_code == 200
    assert len(response.json()) == 0

@pytest.mark.asyncio
async def test_get_conversations(client):
    await client.post("/conversations/")
    response = await client.get("/conversations/")
    assert response.status_code == 200
    assert "id" in response.json()[0]

@pytest.mark.asyncio
async def test_get_conversations_with_id(client):
    await client.post("/conversations/")
    response = await client.get("/conversations/1/")
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_conversations_with_id_not_exists(client):
    response = await client.get("/conversations/10/")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_message(client):
    await client.post("/conversations/")
    message_data = {"content": "Hello, World!"}
    response = await client.post("/conversations/1/ask-message/", json=message_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["sender"] == "chatbot"

@pytest.mark.asyncio
async def test_create_message_non_existent_conversation(client):
    message_data = {"content": "This should fail"}
    response = await client.post("/conversations/10/ask-message/", json=message_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Conversation not found"}

@pytest.mark.asyncio
async def test_read_conversations_large_limit(client):
    for _ in range(5):
        await client.post("/conversations/")
    
    response = await client.get("/conversations/?skip=0&limit=1000")
    assert response.status_code == 200
    assert len(response.json()) == 5 

@pytest.mark.asyncio
async def test_read_conversations_zero_limit(client):
    response = await client.get("/conversations/?skip=0&limit=0")
    assert response.status_code == 200
    assert len(response.json()) == 0

@pytest.mark.asyncio
async def test_create_conversation_invalid_data(client):
    response = await client.post("/conversations/1/ask-message/", json={"wrong_field": "oops"})
    assert response.status_code == 422 

@pytest.mark.asyncio
async def test_get_conversation_string_id(client):
    response = await client.get("/conversations/foo/")
    assert response.status_code == 422 

@pytest.mark.asyncio
async def test_create_message_non_numeric_id(client):
    message_data = {"content": "Invalid ID test"}
    response = await client.post("/conversations/foo/ask-message/", json=message_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_concurrent_create_conversations(client):
    # Initiate several post requests at once, potentially using asyncio.gather
    responses = await asyncio.gather(*[client.post("/conversations/") for _ in range(5)])
    for response in responses:
        assert response.status_code == 200
        assert "id" in response.json()