# Cursor View

Cursor View is a local tool to view, search, and export all your Cursor AI chat histories in one place. It works by scanning your local Cursor application data directories and extracting chat data from the SQLite databases.

**Privacy Note**: All data processing happens locally on your machine. No data is sent to any external servers.

<img width="761" alt="Screenshot 2025-05-01 at 8 22 43 AM-min" src="https://github.com/user-attachments/assets/39dbfa63-8630-4287-903c-f87833a9b435" />

## Setup & Running

1. Clone this repository
2. Install Python dependencies:
   ```
   python3 -m pip install -r requirements.txt
   ```
3. Install frontend dependencies and build (optional, pre-built files included):
   ```
   cd frontend
   npm install
   npm run build
   ```
4. Start the server:
   ```
   python3 server.py
   ```
5. Open your browser to http://localhost:5000

## Features

- Browse all Cursor chat sessions
- Search through chat history
- Export chats as JSON or standalone HTML
- Organize chats by project
- View timestamps of conversations
- Properly rendered code blocks with syntax highlighting
- Support for multiple programming languages in code blocks
- Delete chat sessions from history

## Recent Improvements (26-05-2025)

The following improvements have been made to enhance the application:

1. **Fixed Delete Chat Functionality**: Users can now successfully delete chat sessions from the history without encountering 404 errors.
2. **Fixed JSON Export**: Resolved issues with exporting chats as JSON format.
3. **Improved Error Handling**: Added detailed logging for better debugging and troubleshooting.
4. **Consistent API Endpoints**: Standardized the way session IDs are accessed across all API endpoints.
5. **Enhanced Documentation**: Added comprehensive documentation for server.py including API endpoints and database structure.

## About Code Block Support (26-05-2025)

Cursor View now properly extracts and displays code blocks from your Cursor chat conversations. The application:

1. Extracts code blocks from the SQLite database
2. Preserves language information for proper syntax highlighting
3. Renders code blocks separately from regular markdown text
4. Supports exports with formatted code blocks in both HTML and JSON formats

## Development

The application consists of two parts:
- A Python backend that extracts and processes chat data from Cursor's databases
- A React frontend that displays the chats in a user-friendly interface
