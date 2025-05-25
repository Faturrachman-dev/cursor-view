# Technical Context

## Operating System
- OS: Windows
- Path Separator: \
- CLI: PowerShell

## API Endpoints
- `GET /api/chats` - Get list of all chats
- `GET /api/chat/:session_id` - Get specific chat details
- `DELETE /api/chat/:session_id` - Delete a specific chat
- `GET /api/chat/:session_id/export` - Export chat as HTML or JSON

## Data Structure Consistency
### Session ID Usage
The application handles session IDs consistently across endpoints:
- `session_id` is stored directly on the chat object returned by `extract_chats()`
- All API endpoints should use `chat.get('session_id')` to match chats by ID
- Fixed pattern mismatch in `delete_chat` function that was causing 404 errors

## Local Development
- Server runs on http://127.0.0.1:5000
- Frontend is a React application in the `/frontend` directory
- Server is a Flask application (`server.py`)

## Database Structure
- SQLite databases used for chat storage
- Cursor chat data stored in `cursorDiskKV` and `ItemTable` tables

## Technologies
- Backend: Python, Flask, SQLite
- Frontend: React, JavaScript
- Data: JSON, Markdown

## Development Environment
- Local development server
- Browser-based UI testing

