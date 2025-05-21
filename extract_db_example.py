#!/usr/bin/env python3
"""
Test script to extract ALL RAW BUBBLE DATA for a specific internal composerId
from Cursor's global database.
"""

import os
import json
import platform
import sqlite3
import pathlib
import hashlib
import urllib.parse
from pathlib import Path

# --- User Configuration ---
# THIS IS THE INTERNAL COMPOSER ID YOU IDENTIFIED FROM THE PREVIOUS SCRIPT'S OUTPUT
# For example, if 'session_internal_id_dd1ba98f-1de8-453d-a720-bb251c1a78e0.json' was your chat.
TARGET_INTERNAL_COMPOSER_ID = "dd1ba98f-1de8-453d-a720-bb251c1a78e0"

# Contextual information (will be included in the output JSON for reference)
PROJECT_PATH_OF_INTEREST = "D:/Projects/apps"
UI_LABEL_FOR_CHAT = "3203ebc054e9bb3065e786ee05fe8345"

OUTPUT_FILENAME = f"raw_session_data_for_internal_id_{TARGET_INTERNAL_COMPOSER_ID}.json"
# --- End User Configuration ---

# This is the MD5 hash of the project URI, calculated for completeness in output JSON.
calculated_target_workspace_id = ""
try:
    project_path_obj = pathlib.Path(PROJECT_PATH_OF_INTEREST).resolve()
    folder_uri_str = project_path_obj.as_uri()
    calculated_target_workspace_id = hashlib.md5(folder_uri_str.encode('utf-8')).hexdigest()
except Exception:
    pass # Not critical if this fails for this script's purpose

def get_cursor_storage_path():
    system = platform.system()
    home = pathlib.Path.home()
    if system == "Windows": return home / "AppData" / "Roaming" / "Cursor"
    else: raise RuntimeError(f"Unsupported platform: {system}")

def find_global_db():
    cursor_path = get_cursor_storage_path()
    print(f"Cursor storage path: {cursor_path}")
    global_db_path = cursor_path / "User" / "globalStorage" / "state.vscdb"
    if global_db_path.exists():
        print(f"Found global database: {global_db_path}")
        return global_db_path
    else:
        print(f"Global database not found at: {global_db_path}")
        raise FileNotFoundError(f"Global database not found at {global_db_path}")

def normalize_db_path(db_path_str):
    if not db_path_str: return ""
    try: decoded_path = urllib.parse.unquote(db_path_str)
    except Exception: decoded_path = db_path_str
    if decoded_path.lower().startswith("file:///"):
        decoded_path = decoded_path[8:]
        if len(decoded_path) > 2 and decoded_path[0] == '/' and decoded_path[2] == ':':
            decoded_path = decoded_path[1:]
    normalized = decoded_path.replace('\\', '/').lower()
    return normalized.rstrip('/')

def j(cur, table, key): # Helper to get JSON from ItemTable
    try:
        cur.execute(f"SELECT value FROM {table} WHERE key=?", (key,))
        row = cur.fetchone()
        if row and row[0] is not None:
            try: return json.loads(row[0])
            except Exception as e: print(f"Failed to parse JSON for key '{key}' in '{table}'. Value: {row[0][:200]}... Error: {e}")
    except Exception as e: print(f"SQLite error querying key '{key}' in '{table}': {e}")
    return None


def extract_raw_data_for_target_composer():
    global_db_path = find_global_db()
    if not global_db_path: return

    raw_bubbles_for_target_session = []
    
    print(f"\n=== Extracting RAW bubbles from Global Database (cursorDiskKV) for TARGET_INTERNAL_COMPOSER_ID: {TARGET_INTERNAL_COMPOSER_ID} ===")
    try:
        conn = sqlite3.connect(f"file:{global_db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cursorDiskKV'")
        if cursor.fetchone():
            # The key format is bubbleId:<composerId>:<bubbleTimestamp>
            query = "SELECT key, value FROM cursorDiskKV WHERE key LIKE ?"
            like_pattern = f"bubbleId:{TARGET_INTERNAL_COMPOSER_ID}:%" # Filter by the specific composerId
            print(f"Using LIKE pattern for cursorDiskKV: '{like_pattern}'")
            cursor.execute(query, (like_pattern,))
            
            for key, value_str in cursor.fetchall():
                try:
                    if value_str is None: continue
                    bubble_data = json.loads(value_str) # This is the raw bubble dictionary
                    raw_bubbles_for_target_session.append(bubble_data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for key {key}: {e}. Value snippet: {value_str[:200]}...")
                except Exception as e:
                    print(f"Error processing key {key} from global_cursorDiskKV: {e}. Value: {value_str[:100]}...")
        else:
            print("cursorDiskKV table not found in global database.")
        conn.close()
    except Exception as e:
        print(f"Error during global DB (cursorDiskKV) extraction: {e}")
            
    print(f"\nFound {len(raw_bubbles_for_target_session)} raw bubble structures for internal composer ID '{TARGET_INTERNAL_COMPOSER_ID}'.")

    # Attempt to get project info for this composerId from composer.composerData (best effort for context)
    session_project_path = "Unknown Project Path"
    session_project_name = "Unknown Project"
    try:
        conn = sqlite3.connect(f"file:{global_db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        composer_data = j(cursor, "ItemTable", "composer.composerData")
        if composer_data and "allComposers" in composer_data:
            for composer_entry in composer_data["allComposers"]:
                if composer_entry.get("composerId") == TARGET_INTERNAL_COMPOSER_ID:
                    db_folder_path_raw = composer_entry.get("folderPath")
                    if db_folder_path_raw:
                        session_project_path = normalize_db_path(db_folder_path_raw)
                        session_project_name = Path(session_project_path).name if session_project_path else "Unknown Project"
                        print(f"Found project path '{session_project_path}' for internal ID '{TARGET_INTERNAL_COMPOSER_ID}' via composer.composerData.")
                    break
        conn.close()
    except Exception as e:
        print(f"Note: Could not retrieve precise project path from composer.composerData for {TARGET_INTERNAL_COMPOSER_ID}: {e}")
    
    # If composer.composerData didn't yield a path, use the user-provided one for context
    if session_project_path == "Unknown Project Path" and PROJECT_PATH_OF_INTEREST:
        session_project_path = PROJECT_PATH_OF_INTEREST
        session_project_name = Path(PROJECT_PATH_OF_INTEREST).name

    # Save the raw bubbles
    try:
        with open(OUTPUT_FILENAME, "w", encoding='utf-8') as f:
            json.dump({
                "project_context": { 
                    "name": session_project_name, 
                    "rootPath": session_project_path,
                    "ui_label_if_known": UI_LABEL_FOR_CHAT,
                    "workspace_id_hash_of_project_path": calculated_target_workspace_id or "not_calculated"
                },
                "internal_composer_id": TARGET_INTERNAL_COMPOSER_ID,
                "db_source": str(global_db_path),
                "raw_bubbles": raw_bubbles_for_target_session # Store the list of raw bubble dicts
            }, f, indent=2, ensure_ascii=False)
        print(f"\nSaved RAW session data for internal composer ID '{TARGET_INTERNAL_COMPOSER_ID}' to '{OUTPUT_FILENAME}'")
        if not raw_bubbles_for_target_session:
            print("WARNING: No bubbles were found for this internal composer ID. The output file will have an empty 'raw_bubbles' list.")
        else:
            print(f"The file contains {len(raw_bubbles_for_target_session)} raw message bubbles.")
            print("You can now inspect this JSON file to see the full structure of each message, including any MCP/tool call data.")

    except Exception as e:
        print(f"Error saving raw session data to '{OUTPUT_FILENAME}': {e}")

if __name__ == "__main__":
    if not TARGET_INTERNAL_COMPOSER_ID:
        print("ERROR: TARGET_INTERNAL_COMPOSER_ID is not set. Please identify the internal composer ID for your chat and set it at the top of the script.")
    else:
        extract_raw_data_for_target_composer()