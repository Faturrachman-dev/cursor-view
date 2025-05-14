#!/usr/bin/env python3
"""
Test script to diagnose code block extraction from Cursor chat history.
This script directly examines the database to verify if code blocks are being properly extracted.
"""

import os
import json
import platform
import sqlite3
import pathlib
import sys
from pathlib import Path

# Set up the target session ID from the exported JSON - update to our target chat
TARGET_SESSION_ID = "66277016-074e-4042-8c73-cffac308bed8"
TARGET_WORKSPACE_ID = "cfa37dd8546b5e0940fb840b6785b26b"

def get_cursor_storage_path():
    """Get the path where Cursor stores its data based on the OS."""
    system = platform.system()
    home = pathlib.Path.home()
    
    if system == "Windows":
        return home / "AppData" / "Roaming" / "Cursor"
    elif system == "Darwin":  # macOS
        return home / "Library" / "Application Support" / "Cursor"
    elif system == "Linux":
        return home / ".config" / "Cursor"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")

def find_cursor_dbs():
    """Find the relevant database files for the target chat."""
    cursor_path = get_cursor_storage_path()
    print(f"Cursor storage path: {cursor_path}")
    
    result = {
        "global_db": None,
        "workspace_db": None
    }
    
    # Look for the workspace database
    workspace_db = cursor_path / "User" / "workspaceStorage" / TARGET_WORKSPACE_ID / "state.vscdb"
    if workspace_db.exists():
        print(f"Found workspace database: {workspace_db}")
        result["workspace_db"] = workspace_db
    
    # Look for the global database
    global_db = cursor_path / "User" / "globalStorage" / "state.vscdb"
    if global_db.exists():
        print(f"Found global database: {global_db}")
        result["global_db"] = global_db
    
    return result

def examine_bubble(bubble_data, index):
    """Examine a bubble's data structure to understand how code blocks are stored."""
    print(f"\n--- Bubble #{index} ---")
    
    if not isinstance(bubble_data, dict):
        print(f"Not a dictionary: {type(bubble_data)}")
        return
    
    # Print keys in the bubble data
    print(f"Fields: {', '.join(bubble_data.keys())}")
    
    # Check for type
    if "type" in bubble_data:
        bubble_type = bubble_data["type"]
        role = "user" if bubble_type == 1 else "assistant"
        print(f"Type: {bubble_type} (role: {role})")
    
    # Check for basic text content
    if "text" in bubble_data:
        preview = bubble_data["text"][:100] + "..." if len(bubble_data["text"]) > 100 else bubble_data["text"]
        print(f"Text content: {preview}")
    
    # Check for codeBlocks field specifically
    if "codeBlocks" in bubble_data:
        code_blocks = bubble_data["codeBlocks"]
        print(f"codeBlocks found! Type: {type(code_blocks)}")
        
        if isinstance(code_blocks, list):
            print(f"Number of code blocks: {len(code_blocks)}")
            
            for i, block in enumerate(code_blocks):
                if isinstance(block, dict):
                    print(f"  Block #{i+1} fields: {', '.join(block.keys())}")
                    
                    # Check for content field
                    if "content" in block:
                        content = block["content"]
                        preview = content[:100] + "..." if len(content) > 100 else content
                        print(f"  Content: {preview}")
                    
                    # Check for languageId field
                    if "languageId" in block:
                        print(f"  Language: {block['languageId']}")

def j(cur, table, key):
    """Helper function to get JSON data from the database."""
    cur.execute(f"SELECT value FROM {table} WHERE key=?", (key,))
    row = cur.fetchone()
    if row:
        try:
            return json.loads(row[0])
        except Exception as e:
            print(f"Failed to parse JSON for {key}: {e}")
    return None

def trace_server_extraction_pipeline():
    """Simulate the server.py extraction pipeline to see where code blocks might be lost."""
    dbs = find_cursor_dbs()
    
    if not dbs["global_db"] and not dbs["workspace_db"]:
        print("No databases found!")
        return
    
    # First attempt to parse directly from the exported JSON file
    exported_json_path = os.path.join("export", f"cursor-chat-66277016 (3).json")
    if os.path.exists(exported_json_path):
        try:
            print(f"\n=== Analyzing exported JSON file {exported_json_path} ===")
            with open(exported_json_path, 'r') as f:
                exported_data = json.load(f)
            
            total_messages = len(exported_data.get("messages", []))
            messages_with_code_blocks = sum(1 for msg in exported_data.get("messages", []) 
                                         if "codeBlocks" in msg and msg["codeBlocks"])
            
            print(f"Total messages in exported JSON: {total_messages}")
            print(f"Messages with code blocks in exported JSON: {messages_with_code_blocks}")
            
            # Check for triple backticks which might indicate markdown code blocks
            markdown_code_blocks = sum(1 for msg in exported_data.get("messages", []) 
                                    if "content" in msg and "```" in msg["content"])
            print(f"Messages with markdown code blocks in exported JSON: {markdown_code_blocks}")
        except Exception as e:
            print(f"Error analyzing exported JSON: {e}")
    else:
        print(f"Exported JSON file not found: {exported_json_path}")
    
    # Extract all bubbles from the global database
    all_bubbles = []
    code_blocks_found = 0
    
    # Global database extraction
    if dbs["global_db"]:
        try:
            print("\n=== Extracting from Global Database ===")
            conn = sqlite3.connect(f"file:{dbs['global_db']}?mode=ro", uri=True)
            cursor = conn.cursor()
            
            # Check if cursorDiskKV table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cursorDiskKV'")
            if cursor.fetchone():
                # Look for bubbles related to our target session
                print(f"Looking for bubbles related to session ID: {TARGET_SESSION_ID}")
                cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
                
                for key, value in cursor.fetchall():
                    try:
                        # Extract the composer ID from the key (format: bubbleId:composerId:bubbleId)
                        key_parts = key.split(":")
                        if len(key_parts) >= 2:
                            composer_id = key_parts[1]
                            
                            # Check if this bubble belongs to our target session
                            if TARGET_SESSION_ID.startswith(composer_id):
                                bubble_data = json.loads(value)
                                all_bubbles.append(bubble_data)
                                
                                # Check if this bubble has code blocks
                                if "codeBlocks" in bubble_data and bubble_data["codeBlocks"]:
                                    code_blocks_found += 1
                    except json.JSONDecodeError:
                        print(f"Could not parse JSON for key: {key}")
                    except Exception as e:
                        print(f"Error processing key {key}: {e}")
            else:
                print("cursorDiskKV table not found in global database")
            
            # Also check for chat data in the ItemTable
            try:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ItemTable'")
                if cursor.fetchone():
                    chat_data = j(cursor, "ItemTable", "workbench.panel.aichat.view.aichat.chatdata")
                    if chat_data and "tabs" in chat_data:
                        print("Found chat data in ItemTable")
                        for tab in chat_data.get("tabs", []):
                            tab_id = tab.get("tabId", "unknown")
                            if tab_id.startswith(TARGET_SESSION_ID.split('-')[0]):  # Compare start of session ID
                                print(f"Found matching tab: {tab_id}")
                                for bubble in tab.get("bubbles", []):
                                    all_bubbles.append(bubble)
                                    if "codeBlocks" in bubble and bubble["codeBlocks"]:
                                        code_blocks_found += 1
                else:
                    print("ItemTable not found in global database")
            except Exception as e:
                print(f"Error checking ItemTable: {e}")
            
            conn.close()
        except Exception as e:
            print(f"Error during global DB extraction: {e}")
    
    # Workspace database extraction
    if dbs["workspace_db"]:
        try:
            print("\n=== Extracting from Workspace Database ===")
            conn = sqlite3.connect(f"file:{dbs['workspace_db']}?mode=ro", uri=True)
            cursor = conn.cursor()
            
            # Try to get chat data from workbench.panel.aichat.view.aichat.chatdata
            chat_data = j(cursor, "ItemTable", "workbench.panel.aichat.view.aichat.chatdata")
            if chat_data and "tabs" in chat_data:
                print("Found chat data in workspace ItemTable")
                for tab in chat_data.get("tabs", []):
                    tab_id = tab.get("tabId", "unknown")
                    if tab_id.startswith(TARGET_SESSION_ID.split('-')[0]):  # Compare start of session ID
                        print(f"Found matching tab: {tab_id}")
                        for bubble in tab.get("bubbles", []):
                            all_bubbles.append(bubble)
                            if "codeBlocks" in bubble and bubble["codeBlocks"]:
                                code_blocks_found += 1
            else:
                print("No chat data found in workspace database")
            
            conn.close()
        except Exception as e:
            print(f"Error during workspace DB extraction: {e}")
    
    print(f"\nFound total of {len(all_bubbles)} bubbles for target session")
    print(f"Bubbles with code blocks: {code_blocks_found}")
    
    # Examine a few bubbles to understand their structure
    for i, bubble in enumerate(all_bubbles[:5]):  # Examine first 5 bubbles
        examine_bubble(bubble, i+1)
    
    # Examine any bubbles with code blocks specifically
    code_block_bubbles = [b for b in all_bubbles if "codeBlocks" in b and b["codeBlocks"]]
    print(f"\n=== Examining bubbles with code blocks ({len(code_block_bubbles)}) ===")
    for i, bubble in enumerate(code_block_bubbles[:5]):  # Examine first 5 with code blocks
        examine_bubble(bubble, i+1)
    
    # Test our extraction function implementation
    print("\n=== Testing Full Extraction Pipeline ===")
    messages = []
    
    for bubble in all_bubbles:
        try:
            # Extract regular text
            text = (bubble.get("text", "") or bubble.get("richText", "") or bubble.get("code", "") or 
                   bubble.get("codeSnippet", "") or bubble.get("content", "") or bubble.get("markdown", "") or "").strip()
            
            # Extract code blocks as separate entities
            code_blocks = []
            if "codeBlocks" in bubble and isinstance(bubble["codeBlocks"], list):
                for block in bubble["codeBlocks"]:
                    if isinstance(block, dict):
                        code_content = block.get("content", "")
                        lang_id = block.get("languageId", "")
                        
                        if code_content:
                            code_blocks.append({
                                "content": code_content,
                                "language": lang_id
                            })
                            
            # Skip bubbles with no content
            if not text and not code_blocks:
                continue

            role = "user" if bubble.get("type") == 1 else "assistant"
            messages.append({"role": role, "content": text, "codeBlocks": code_blocks})
            
        except Exception as e:
            print(f"Error in extraction pipeline: {e}")
    
    # Count messages with code blocks
    messages_with_code = sum(1 for msg in messages if msg.get("codeBlocks"))
    print(f"Extracted {len(messages)} messages total")
    print(f"Messages with code blocks: {messages_with_code}")
    
    # Save the extracted messages
    output_file = "diagnostic_extraction_result.json"
    with open(output_file, "w") as f:
        json.dump({
            "project": {
                "name": "golang",
                "rootPath": "/d%3A/Projects/golang",
                "workspace_id": TARGET_WORKSPACE_ID
            },
            "messages": messages,
            "session_id": TARGET_SESSION_ID,
            "date": 1747157030.012
        }, f, indent=2)
    
    print(f"\nExtracted messages saved to {output_file}")
    
    # Do a final check on the format_chat_for_frontend function
    print("\n=== Simulating format_chat_for_frontend function ===")
    # Check if code blocks are preserved during formatting
    formatted_messages = [
        {"role": msg["role"], "content": msg["content"], "codeBlocks": msg.get("codeBlocks", [])}
        for msg in messages
    ]
    
    # Save the formatted messages
    formatted_file = "diagnostic_formatted_result.json"
    with open(formatted_file, "w") as f:
        json.dump({
            "project": {
                "name": "golang",
                "rootPath": "/d%3A/Projects/golang",
                "workspace_id": TARGET_WORKSPACE_ID
            },
            "messages": formatted_messages,
            "session_id": TARGET_SESSION_ID,
            "date": 1747157030.012
        }, f, indent=2)
    
    print(f"Formatted messages saved to {formatted_file}")
    print(f"Messages with code blocks after formatting: {sum(1 for msg in formatted_messages if msg.get('codeBlocks'))}")

if __name__ == "__main__":
    trace_server_extraction_pipeline() 