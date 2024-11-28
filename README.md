# Async Chat API

This repository contains a Async Chat API application that works as a conversational chatbot. It provides endpoints to create and manage conversations with a chatbot using RESTful API design. The backend uses SQLAlchemy for ORM (Object Relational Mapping) with a SQLite database, and includes integration with OpenAI's API for generating chatbot responses.

## Features

- **Create Conversations**: Start a new conversation session with the chatbot.
- **Send Messages**: Send messages to the chatbot and get AI-generated responses.
- **View Conversations**: Retrieve a list of all conversations, or view details of a specific conversation.
- **Database Integration**: Uses SQLAlchemy for ORM with a SQLite database to persist conversation data.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/tanaymurdia/Async-Chat-API.git
   cd Async-Chat-API
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   
   To run this project, you need to set up a `.env` file in the root directory of your project and configure your environment variables.
   Create a `.env` file:

   In the root of your project, create a new file named `.env`.

   Open the `.env` file and add the following line, replacing `your-openai-api-key` with your actual OpenAI API key:

   ```env
   OPENAI_API_KEY=your-openai-api-key
   ```

   Make sure not to share this API key publicly or commit it to version control.

   ```bash
   python -m uvicorn app.main:app --reload
   ```

   This will start the app on `http://127.0.0.1:8000`.

7. **Testing**

   ```bash
   python -m pytest tests/test_app.py
   ```

   This will run the test in the directory `tests/test_app.py`.

## Usage

### Endpoints

- **POST `/conversations/`**

  Create a new conversation.

- **POST `/conversations/{conversation_id}/ask-message/`**

  Send a message to a specific conversation and get a chatbot response.

- **GET `/conversations/`**

  Retrieve a list of all conversations.

- **GET `/conversations/{conversation_id}/`**

  Retrieve the details of a specific conversation by ID.

## Design Choices

### FastAPI

FastAPI was chosen for its high performance and ease of use in building APIs. It supports asynchronous programming, which is beneficial for I/O-bound operations like database access and API calls to OpenAI.

### SQLAlchemy

SQLAlchemy is used for ORM due to its flexibility and ability to work with different types of databases with minimal configuration changes. Utilizing SQLAlchemy's ORM capabilities helps in easily mapping classes to database tables and supports complex queries.

### Dependency Injection

FastAPI's `Depends` is used for managing dependency injection, particularly to manage database sessions (`get_db`). This ensures that each request gets a fresh database session, thus maintaining the state effectively.

### OpenAI Integration

The use of OpenAI's API provides dynamic and intelligent responses for conversations. This adds significant value by enabling AI-generated responses that can be used for developing advanced conversational agents.

### Endpoints Design

- **Create Conversation**: Designed as a standalone method to initialize chat sessions and organized around RESTful principles.
- **Send Message**: This endpoint not only saves the user's message but also generates and saves the chatbot's multiple responses in one go, reducing round trips.
- **Read Conversations**: These endpoints support pagination and detail retrieval, making them efficient for handling large datasets.

### Error Handling

The error handling mechanism alerts users to situations such as invalid conversation IDs, adhering to HTTP status codes conventions for clear client-side error diagnoses.
