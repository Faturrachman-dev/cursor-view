#!/usr/bin/env python3
"""
Script to explore Cursor database structure, specifically looking at how code blocks are stored.
"""

import os
import platform
import sqlite3
import json
import pathlib
from pathlib import Path

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

def find_db_files():
    """Find all SQLite database files in Cursor storage, focusing on our target workspace."""
    cursor_path = get_cursor_storage_path()
    print(f"Cursor storage path: {cursor_path}")
    
    db_files = []
    
    # First try to find our specific workspace (334534297f9918a349a41baaf6accab7)
    workspace_id = "334534297f9918a349a41baaf6accab7"
    target_workspace = cursor_path / "User" / "workspaceStorage" / workspace_id / "state.vscdb"
    
    if target_workspace.exists():
        print(f"Found target workspace database: {target_workspace}")
        db_files.append(("Target Workspace DB", target_workspace))
    
    # Also get the global storage DB
    global_storage = cursor_path / "User" / "globalStorage" / "state.vscdb"
    if global_storage.exists():
        db_files.append(("Global State DB", global_storage))
    
    return db_files

def examine_code_blocks_in_db(db_path):
    """Examine the database for messages with code blocks."""
    print(f"\n=== Examining: {db_path} for code blocks ===")
    
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # Check if cursorDiskKV table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cursorDiskKV'")
        if cursor.fetchone():
            print("Analyzing cursorDiskKV table for code blocks...")
            
            # Look for bubble data that might contain code blocks
            cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
            rows = cursor.fetchall()
            
            for i, (key, value) in enumerate(rows):
                try:
                    if value is None:
                        continue
                        
                    data = json.loads(value)
                    
                    # Check for code-specific fields
                    has_code = False
                    code_content = None
                    
                    # Look for codeBlocks field which is likely to contain actual code
                    if "codeBlocks" in data:
                        has_code = True
                        code_content = data["codeBlocks"]
                        print(f"\nFound codeBlocks in bubble {key}:")
                        print(f"Type: {type(code_content)}")
                        
                        if isinstance(code_content, list):
                            print(f"Number of code blocks: {len(code_content)}")
                            for j, block in enumerate(code_content):
                                if isinstance(block, dict):
                                    print(f"  Code Block #{j+1} fields: {', '.join(block.keys())}")
                                    # Extract code or content
                                    if "code" in block:
                                        code_sample = block["code"]
                                        print(f"  Code sample: {code_sample[:200]}..." if len(code_sample) > 200 else code_sample)
                        
                    # Check for other code-related fields
                    for field in ["code", "codeSnippet", "suggestedCodeBlocks"]:
                        if field in data and data[field]:
                            has_code = True
                            code_content = data[field]
                            print(f"\nFound {field} in bubble {key}:")
                            print(f"Content: {str(code_content)[:200]}..." if len(str(code_content)) > 200 else str(code_content))
                    
                    # If we found code, print the whole bubble structure
                    if has_code:
                        print(f"Full bubble fields: {', '.join(data.keys())}")
                        print(f"Text content: {data.get('text', '')[:100]}..." if 'text' in data and len(data['text']) > 100 else data.get('text', ''))
                except Exception as e:
                    print(f"Error examining bubble {key}: {e}")
        
        # Check ItemTable for any composer data with code
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ItemTable'")
        if cursor.fetchone():
            print("\nAnalyzing ItemTable for code content...")
            
            # Look for composer data
            cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%composer%' OR key LIKE '%chat%'")
            rows = cursor.fetchall()
            
            for key, value in rows:
                try:
                    data = json.loads(value)
                    
                    # Check if this is composer data with messages
                    if isinstance(data, dict) and "allComposers" in data:
                        for composer in data["allComposers"]:
                            if "messages" in composer:
                                print(f"\nFound composer with {len(composer['messages'])} messages in {key}")
                                
                                # Look for code in messages
                                for msg in composer["messages"]:
                                    if "content" in msg and "```" in msg["content"]:
                                        print("Found message with code blocks (using ``` markdown):")
                                        print(f"Message content: {msg['content'][:200]}..." if len(msg['content']) > 200 else msg['content'])
                except:
                    # Skip entries that aren't valid JSON
                    pass
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Exploring Cursor database structure for code blocks")
    
    db_files = find_db_files()
    if not db_files:
        print("No Cursor database files found.")
        return
    
    print(f"Found {len(db_files)} database files:")
    for i, (db_type, db_path) in enumerate(db_files):
        print(f"{i+1}. {db_type}: {db_path}")
    
    # Examine each database for code blocks
    for _, db_path in db_files:
        examine_code_blocks_in_db(db_path)
    
    print("\nExploration complete!")

if __name__ == "__main__":
    main() 