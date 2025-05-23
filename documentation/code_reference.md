# Cursor View Server Code Reference

This document provides a detailed reference for the main functions in the `server.py` file, including their parameters, return values, and usage examples.

## Table of Contents

1. [Database Functions](#database-functions)
2. [Data Extraction Functions](#data-extraction-functions)
3. [Data Processing Functions](#data-processing-functions)
4. [API Endpoint Functions](#api-endpoint-functions)
5. [Utility Functions](#utility-functions)

## Database Functions

### `cursor_root()`

Determines the platform-specific Cursor data directory.

**Parameters:** None

**Returns:** 
- `pathlib.Path`: Path to the Cursor application data directory

**Platform-specific paths:**
- Windows: `%APPDATA%\Roaming\Cursor`
- macOS: `~/Library/Application Support/Cursor`
- Linux: `~/.config/Cursor`

**Example:**
```python
cursor_dir = cursor_root()
print(f"Cursor data directory: {cursor_dir}")
```

### `workspaces(base: pathlib.Path)`

Enumerates workspace databases within the Cursor data directory.

**Parameters:**
- `base` (pathlib.Path): The Cursor data directory

**Yields:**
- `tuple[str, pathlib.Path]`: A tuple containing workspace ID and path to its database

**Example:**
```python
for workspace_id, db_path in workspaces(cursor_root()):
    print(f"Workspace: {workspace_id}, DB: {db_path}")
```

### `global_storage_path(base: pathlib.Path) -> pathlib.Path`

Locates the global storage database for Cursor.

**Parameters:**
- `base` (pathlib.Path): The Cursor data directory

**Returns:**
- `pathlib.Path`: Path to the global storage database, or None if not found

**Example:**
```python
global_db = global_storage_path(cursor_root())
print(f"Global storage DB: {global_db}")
```

## Data Extraction Functions

### `extract_chats(detailed_logging=False, target_session_id=None) -> list[Dict[str,Any]]`

Main function that orchestrates the chat extraction process.

**Parameters:**
- `detailed_logging` (bool, optional): Whether to enable detailed logging. Defaults to False.
- `target_session_id` (str, optional): If provided, only extract the chat with this session ID. Defaults to None.

**Returns:**
- `list[Dict[str,Any]]`: List of chat sessions with their messages and metadata

**Example:**
```python
# Get all chats
all_chats = extract_chats()

# Get a specific chat with detailed logging
specific_chat = extract_chats(detailed_logging=True, target_session_id="abcd1234")
```

### `iter_bubbles_from_disk_kv(db: pathlib.Path, detailed_logging=False, target_session_id=None)`

Extracts chat bubbles (messages) from the cursorDiskKV table.

**Parameters:**
- `db` (pathlib.Path): Path to the SQLite database
- `detailed_logging` (bool, optional): Whether to enable detailed logging. Defaults to False.
- `target_session_id` (str, optional): If provided, only extract bubbles for this session ID. Defaults to None.

**Yields:**
- `tuple[str,str,str,str,list,bool,dict,dict,int]`: A tuple containing composer ID, role, text, DB path, code blocks, is_thought flag, thinking data, tool former data, and capability type

**Example:**
```python
for composer_id, role, text, db_path, code_blocks, is_thought, thinking, tool_data, cap_type in iter_bubbles_from_disk_kv(db_path):
    print(f"Message from {role} in session {composer_id}: {text[:50]}...")
```

### `iter_chat_from_item_table(db: pathlib.Path, detailed_logging=False, target_session_id=None)`

Extracts chat data from the ItemTable.

**Parameters:**
- `db` (pathlib.Path): Path to the SQLite database
- `detailed_logging` (bool, optional): Whether to enable detailed logging. Defaults to False.
- `target_session_id` (str, optional): If provided, only extract data for this session ID. Defaults to None.

**Yields:**
- `tuple[str,str,str,str,list,bool,dict,dict,int]`: A tuple containing composer ID, role, text, DB path, code blocks, is_thought flag, thinking data, tool former data, and capability type

**Example:**
```python
for composer_id, role, text, db_path, code_blocks, is_thought, thinking, tool_data, cap_type in iter_chat_from_item_table(db_path):
    print(f"ItemTable message from {role} in session {composer_id}: {text[:50]}...")
```

### `iter_composer_data(db: pathlib.Path, detailed_logging=False, target_session_id=None)`

Extracts metadata about chat sessions.

**Parameters:**
- `db` (pathlib.Path): Path to the SQLite database
- `detailed_logging` (bool, optional): Whether to enable detailed logging. Defaults to False.
- `target_session_id` (str, optional): If provided, only extract data for this session ID. Defaults to None.

**Yields:**
- `tuple[str,dict,str]`: A tuple containing composer ID, composer data, and DB path

**Example:**
```python
for composer_id, data, db_path in iter_composer_data(db_path):
    print(f"Composer {composer_id} metadata: {data.get('title', 'Untitled')}")
```

## Data Processing Functions

### `format_chat_for_frontend(chat)`

Formats chat data for display in the frontend.

**Parameters:**
- `chat` (dict): The chat data to format

**Returns:**
- `dict`: Formatted chat data ready for frontend display

**Example:**
```python
formatted = format_chat_for_frontend(chat_data)
print(f"Formatted {len(formatted.get('messages', []))} messages for frontend")
```

### `generate_standalone_html(chat)`

Generates a standalone HTML file for a chat session.

**Parameters:**
- `chat` (dict): The chat data to convert to HTML

**Returns:**
- `str`: HTML content for the chat session

**Example:**
```python
html_content = generate_standalone_html(chat_data)
with open("chat_export.html", "w", encoding="utf-8") as f:
    f.write(html_content)
```

### `extract_project_name_from_path(root_path, debug=False)`

Attempts to infer project names from file paths.

**Parameters:**
- `root_path` (str): The file path to extract a project name from
- `debug` (bool, optional): Whether to enable debug logging. Defaults to False.

**Returns:**
- `str`: Extracted project name

**Example:**
```python
path = "/Users/username/Projects/cursor-view"
project_name = extract_project_name_from_path(path)
print(f"Extracted project name: {project_name}")  # Should return "cursor-view"
```

## API Endpoint Functions

### `get_chats()`

API endpoint that returns a list of all chat sessions.

**HTTP Method:** GET

**URL:** `/api/chats`

**Returns:**
- JSON array of chat sessions

### `get_chat(session_id)`

API endpoint that returns details of a specific chat session.

**HTTP Method:** GET

**URL:** `/api/chat/<session_id>`

**Parameters:**
- `session_id` (str): The ID of the chat session to retrieve

**Returns:**
- JSON object with chat session details

### `export_chat(session_id)`

API endpoint that exports a chat session as HTML or JSON.

**HTTP Method:** GET

**URL:** `/api/chat/<session_id>/export`

**Parameters:**
- `session_id` (str): The ID of the chat session to export
- `format` (str, query parameter): The export format, either "html" or "json" (default: "html")

**Returns:**
- HTML or JSON file as an attachment

### `delete_chat(session_id)`

API endpoint that deletes a specific chat session.

**HTTP Method:** DELETE

**URL:** `/api/chat/<session_id>`

**Parameters:**
- `session_id` (str): The ID of the chat session to delete

**Returns:**
- JSON object with success status

## Utility Functions

### `j(cur: sqlite3.Cursor, table: str, key: str)`

Helper function to extract JSON data from SQLite tables.

**Parameters:**
- `cur` (sqlite3.Cursor): SQLite cursor
- `table` (str): Table name
- `key` (str): Key to extract

**Returns:**
- Parsed JSON data or None if not found/invalid

**Example:**
```python
con = sqlite3.connect(db_path)
cur = con.cursor()
data = j(cur, "ItemTable", "workbench.panel.aichat.view.aichat.chatdata")
```

### `delete_chat_from_db(db_path, composer_id)`

Removes chat data from Cursor's databases.

**Parameters:**
- `db_path` (str): Path to the database file
- `composer_id` (str): Composer ID of the chat to delete

**Returns:**
- `bool`: True if deletion was successful, False otherwise

**Example:**
```python
success = delete_chat_from_db("/path/to/state.vscdb", "abcd1234")
print(f"Chat deletion {'succeeded' if success else 'failed'}")
```

### `workspace_info(db: pathlib.Path)`

Extracts project metadata from workspace databases.

**Parameters:**
- `db` (pathlib.Path): Path to the workspace database

**Returns:**
- `tuple[dict, dict]`: A tuple containing project info and composer metadata

**Example:**
```python
project_info, composer_meta = workspace_info(db_path)
print(f"Project name: {project_info.get('name', 'Unknown')}")
``` 