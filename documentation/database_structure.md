# Cursor SQLite Database Structure

This document provides information about the database structure that Cursor View interacts with. Understanding this structure is essential for maintaining and extending the application.

## Database Locations

Cursor stores its data in SQLite databases in two main locations:

1. **Global Storage Database**:
   - Windows: `%APPDATA%\Roaming\Cursor\User\globalStorage\state.vscdb`
   - macOS: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`
   - Linux: `~/.config/Cursor/User/globalStorage/state.vscdb`

2. **Workspace Databases**:
   - Windows: `%APPDATA%\Roaming\Cursor\User\workspaceStorage\<workspace_id>\state.vscdb`
   - macOS: `~/Library/Application Support/Cursor/User/workspaceStorage/<workspace_id>/state.vscdb`
   - Linux: `~/.config/Cursor/User/workspaceStorage/<workspace_id>/state.vscdb`

## Table Structure

The SQLite databases used by Cursor contain several important tables:

### cursorDiskKV

This is a key-value storage table with the following schema:

```sql
CREATE TABLE cursorDiskKV (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

Key chat-related entries in this table include:

1. **Chat Bubbles**: Stored with keys like `bubbleId:<composer_id>:<bubble_id>`
   - Contains the text content, code blocks, and metadata for each message
   - Each bubble represents one message in a chat (either from user or assistant)

2. **Composer Data**: Stored with keys like `composerData:<composer_id>`
   - Contains metadata about the chat session (title, creation date, etc.)

Example of a bubble entry in JSON format:

```json
{
  "type": 2,           // 1 for user, 2 for assistant
  "text": "Hello...",  // The message text content
  "codeBlocks": [      // Optional code blocks
    {
      "content": "console.log('Hello');",
      "languageId": "javascript"
    }
  ],
  "isThought": false,  // Whether this is a thought bubble
  "thinking": {},      // Thought process data (if applicable)
  "toolFormerData": {} // Tool call data (if applicable)
}
```

### ItemTable

This is another key-value storage table with a similar schema:

```sql
CREATE TABLE ItemTable (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

Important keys in this table include:

1. **Chat Data**: Stored with key `workbench.panel.aichat.view.aichat.chatdata`
   - Contains all chat tabs and their bubbles
   - Structured as a JSON object with a `tabs` array

2. **History Entries**: Stored with key `history.entries`
   - Contains information about files that have been opened
   - Used for extracting project information

3. **Composer Data**: Stored with key `composer.composerData`
   - Contains metadata about all composer sessions

Example of chat data structure in ItemTable:

```json
{
  "tabs": [
    {
      "tabId": "session_id_here",
      "bubbles": [
        {
          "type": 1,
          "text": "User message here",
          "codeBlocks": []
        },
        {
          "type": 2,
          "text": "Assistant response here",
          "codeBlocks": []
        }
      ]
    }
  ]
}
```

## Data Structure

### Chat Messages

Chat messages (or "bubbles") have the following structure:

| Field | Type | Description |
|-------|------|-------------|
| type | integer | 1 for user messages, 2 for assistant messages |
| text | string | The main text content of the message |
| codeBlocks | array | Array of code blocks with content and language |
| isThought | boolean | Whether this is a thought bubble (AI thinking) |
| thinking | object | Contains thought process data for AI |
| toolFormerData | object | Contains tool call information |
| capabilityType | integer | Indicates the capability type of the message |

### Code Blocks

Code blocks have the following structure:

| Field | Type | Description |
|-------|------|-------------|
| content | string | The code content |
| languageId | string | The programming language identifier |

### Composer Data

Composer data (chat session metadata) has the following structure:

| Field | Type | Description |
|-------|------|-------------|
| composerId | string | Unique ID for the chat session |
| name | string | Title of the chat session |
| createdAt | string/number | Creation timestamp (ISO string or milliseconds) |
| lastUpdatedAt | string/number | Last update timestamp |

## Extracting Data

### From cursorDiskKV

To extract chat data from cursorDiskKV:

1. Connect to the database in read-only mode
2. Query for keys that match the pattern `bubbleId:%`
3. Parse the JSON value for each key
4. Extract relevant fields (text, code blocks, etc.)

```python
con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
cur = con.cursor()
cur.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
for k, v in cur.fetchall():
    if v is not None:
        bubble = json.loads(v)
        composer_id = k.split(":")[1]
        # Process the bubble...
```

### From ItemTable

To extract chat data from ItemTable:

1. Connect to the database in read-only mode
2. Query for the key `workbench.panel.aichat.view.aichat.chatdata`
3. Parse the JSON value
4. Extract tabs and bubbles

```python
con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
cur = con.cursor()
cur.execute("SELECT value FROM ItemTable WHERE key=?", ("workbench.panel.aichat.view.aichat.chatdata",))
row = cur.fetchone()
if row and row[0]:
    chat_data = json.loads(row[0])
    if "tabs" in chat_data:
        for tab in chat_data["tabs"]:
            tab_id = tab.get("tabId", "unknown")
            # Process the tab and its bubbles...
```

## Schema Evolution

The Cursor application is actively developed, and the database schema may change over time. When maintaining Cursor View, it's important to:

1. Handle missing tables or fields gracefully
2. Check if tables exist before querying them
3. Use fallback mechanisms when expected data is not found
4. Test with different versions of Cursor

The server.py code includes safety checks like:

```python
# Check if table exists
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cursorDiskKV'")
if not cur.fetchone():
    con.close()
    return
```

This helps ensure the application remains compatible with different versions of Cursor's database schema. 