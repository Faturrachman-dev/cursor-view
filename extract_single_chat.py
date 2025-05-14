#!/usr/bin/env python3
"""
Script to extract a single Cursor chat conversation with proper handling of code blocks.
This is a targeted solution to extract code blocks correctly from a specific session.
"""

import os
import json
import platform
import sqlite3
import pathlib
import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

# Target session ID to extract
TARGET_SESSION_ID = "5c439b02-9d08-4fd2-9b22-8e47cef5aa23"
TARGET_WORKSPACE_ID = "334534297f9918a349a41baaf6accab7"
OUTPUT_FILE = f"export/cursor-chat-{TARGET_SESSION_ID}-fixed.json"

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

def find_global_db():
    """Find the global database file."""
    cursor_path = get_cursor_storage_path()
    print(f"Cursor storage path: {cursor_path}")
    
    # Look for the global database
    global_db = cursor_path / "User" / "globalStorage" / "state.vscdb"
    if global_db.exists():
        print(f"Found global database: {global_db}")
        return global_db
    
    return None

def extract_bubbles_for_session(db_path, session_id):
    """Extract all bubbles related to a specific session ID."""
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # Check if cursorDiskKV table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cursorDiskKV'")
        if not cursor.fetchone():
            print("cursorDiskKV table not found in database")
            conn.close()
            return []
        
        # Get all bubbles for our target session
        cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
        
        bubbles = []
        for key, value in cursor.fetchall():
            if value is None:
                continue
                
            try:
                # Extract the composer ID from the key (format: bubbleId:composerId:bubbleId)
                key_parts = key.split(":")
                if len(key_parts) >= 2:
                    composer_id = key_parts[1]
                    
                    # Check if this bubble belongs to our target session
                    if session_id.startswith(composer_id):
                        bubble_data = json.loads(value)
                        bubbles.append(bubble_data)
            except json.JSONDecodeError:
                print(f"Could not parse JSON for key: {key}")
            except Exception as e:
                print(f"Error processing key {key}: {e}")
        
        conn.close()
        return bubbles
    
    except Exception as e:
        print(f"Error accessing database: {e}")
        return []

def process_bubble(bubble):
    """Process a bubble to extract its content, including code blocks as separate fields."""
    # First get regular text content
    text = (bubble.get("text") or bubble.get("richText") or bubble.get("code") or 
           bubble.get("codeSnippet") or bubble.get("content") or bubble.get("markdown") or "").strip()
    
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
    
    # Check for nested content structure
    if not text and bubble.get("parts"):
        for part in bubble.get("parts", []):
            if isinstance(part, dict):
                part_text = (part.get("text") or part.get("code") or part.get("content") or "").strip()
                if part_text:
                    text = part_text
                    break
    
    if not text and not code_blocks:
        return None
    
    # Determine role - user is type 1, assistant is type 2
    role = "user" if bubble.get("type") == 1 else "assistant"
    
    # Construct structured message with separate content and codeBlocks fields
    message = {
        "role": role,
        "content": text,
    }
    
    # Only add codeBlocks if there are any
    if code_blocks:
        message["codeBlocks"] = code_blocks
    
    return message

def create_chat_export(bubbles):
    """Create a chat export with properly processed messages."""
    messages = []
    
    # Process each bubble to extract its content properly
    for bubble in bubbles:
        message = process_bubble(bubble)
        if message:
            messages.append(message)
    
    # Create the chat export
    export = {
        "project": {
            "name": "cursor-view",
            "rootPath": "/d%3A/Projects/cursor/cursor-view",
            "workspace_id": TARGET_WORKSPACE_ID
        },
        "messages": messages,
        "date": datetime.datetime.now().timestamp(),
        "session_id": TARGET_SESSION_ID,
        "workspace_id": TARGET_WORKSPACE_ID,
        "db_path": str(find_global_db())
    }
    
    return export

def save_export(export_data, output_file):
    """Save the export data to a file."""
    # Create export directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save the export
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"Chat export saved to {output_file}")
    
    # Print some stats
    print(f"Number of messages: {len(export_data['messages'])}")
    code_blocks_count = sum(1 for msg in export_data['messages'] if 'codeBlocks' in msg)
    total_blocks = sum(len(msg.get('codeBlocks', [])) for msg in export_data['messages'])
    print(f"Messages with code blocks: {code_blocks_count} (total blocks: {total_blocks})")

def main():
    """Extract and export a single chat conversation with code blocks properly handled."""
    print(f"Extracting chat for session ID: {TARGET_SESSION_ID}")
    
    # Find the global database
    db_path = find_global_db()
    if not db_path:
        print("Global database not found, cannot proceed.")
        return
    
    # Extract bubbles for the target session
    bubbles = extract_bubbles_for_session(db_path, TARGET_SESSION_ID)
    print(f"Found {len(bubbles)} bubbles for session {TARGET_SESSION_ID}")
    
    # Create the chat export
    export = create_chat_export(bubbles)
    
    # Save the export
    save_export(export, OUTPUT_FILE)
    
    print("Export complete!")

if __name__ == "__main__":
    main() 