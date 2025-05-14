#!/usr/bin/env python3
"""
Simple API server to serve Cursor chat data for the web interface.
"""

import json
import uuid
import logging
import datetime
import os
import platform
import sqlite3
import argparse
import pathlib
from collections import defaultdict
from typing import Dict, Any, Iterable
from pathlib import Path
from flask import Flask, Response, jsonify, send_from_directory, request
from flask_cors import CORS
import markdown
import html

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='frontend/build')
CORS(app)

################################################################################
# Cursor storage roots
################################################################################
def cursor_root() -> pathlib.Path:
    h = pathlib.Path.home()
    s = platform.system()
    if s == "Darwin":   return h / "Library" / "Application Support" / "Cursor"
    if s == "Windows":  return h / "AppData" / "Roaming" / "Cursor"
    if s == "Linux":    return h / ".config" / "Cursor"
    raise RuntimeError(f"Unsupported OS: {s}")

################################################################################
# Helpers
################################################################################
def j(cur: sqlite3.Cursor, table: str, key: str):
    cur.execute(f"SELECT value FROM {table} WHERE key=?", (key,))
    row = cur.fetchone()
    if row:
        try:    return json.loads(row[0])
        except Exception as e: 
            logger.debug(f"Failed to parse JSON for {key}: {e}")
    return None

def iter_bubbles_from_disk_kv(db: pathlib.Path) -> Iterable[tuple[str,str,str,str,list]]:
    """Yield (composerId, role, text, db_path, code_blocks) from cursorDiskKV table."""
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        cur = con.cursor()
        # Check if table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cursorDiskKV'")
        if not cur.fetchone():
            con.close()
            return
        
        cur.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
    except sqlite3.DatabaseError as e:
        logger.debug(f"Database error with {db}: {e}")
        return
    
    db_path_str = str(db)
    
    for k, v in cur.fetchall():
        try:
            if v is None:
                continue
                
            bubble = json.loads(v)
            composer_id = k.split(":")[1] if ":" in k else ""
            if not composer_id:
                continue
        
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
            
            # Extract nested content
            if not text and bubble.get("parts"):
                for part in bubble.get("parts", []):
                    if isinstance(part, dict):
                        part_text = part.get("text", "") or part.get("code", "") or part.get("content", "")
                        if part_text and part_text.strip():
                            text = part_text.strip()
                            break
                            
            # Skip bubbles with no content
            if not text and not code_blocks:
                continue

            role = "user" if bubble.get("type") == 1 else "assistant"
            yield composer_id, role, text, db_path_str, code_blocks
            
        except Exception as e:
            logger.debug(f"Error processing bubble: {e}")

def iter_chat_from_item_table(db: pathlib.Path) -> Iterable[tuple[str,str,str,str,list]]:
    """Yield (composerId, role, text, db_path, code_blocks) from ItemTable."""
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        cur = con.cursor()
        
        # Try to get chat data from workbench.panel.aichat.view.aichat.chatdata
        chat_data = j(cur, "ItemTable", "workbench.panel.aichat.view.aichat.chatdata")
        if chat_data and "tabs" in chat_data:
            for tab in chat_data.get("tabs", []):
                tab_id = tab.get("tabId", "unknown")
                for bubble in tab.get("bubbles", []):
                    bubble_type = bubble.get("type")
                    if not bubble_type:
                        continue
                    
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
    
                    role = "user" if bubble_type == 1 else "assistant"
                    yield tab_id, role, text, str(db), code_blocks

    except Exception as e:
        logger.debug(f"Error in iter_chat_from_item_table: {e}")

def iter_composer_data(db: pathlib.Path) -> Iterable[tuple[str,dict,str]]:
    """Yield (composerId, composerData, db_path) from cursorDiskKV table."""
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        cur = con.cursor()
        # Check if table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cursorDiskKV'")
        if not cur.fetchone():
            con.close()
            return
        
        cur.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
    except sqlite3.DatabaseError as e:
        logger.debug(f"Database error with {db}: {e}")
        return
    
    db_path_str = str(db)
    
    for k, v in cur.fetchall():
        try:
            if v is None:
                continue
                
            composer_data = json.loads(v)
            composer_id = k.split(":")[1]
            yield composer_id, composer_data, db_path_str
            
        except Exception as e:
            logger.debug(f"Failed to parse composer data for key {k}: {e}")
            continue
    
    con.close()

################################################################################
# Workspace discovery
################################################################################
def workspaces(base: pathlib.Path):
    ws_root = base / "User" / "workspaceStorage"
    if not ws_root.exists():
        return
    for folder in ws_root.iterdir():
        db = folder / "state.vscdb"
        if db.exists():
            yield folder.name, db

def extract_project_name_from_path(root_path, debug=False):
    """
    Extract a project name from a path, skipping user directories.
    """
    if not root_path or root_path == '/':
        return "Root"
        
    path_parts = [p for p in root_path.split('/') if p]
    
    # Skip common user directory patterns
    project_name = None
    home_dir_patterns = ['Users', 'home']
    
    # Get current username for comparison
    current_username = os.path.basename(os.path.expanduser('~'))
    
    # Find user directory in path
    username_index = -1
    for i, part in enumerate(path_parts):
        if part in home_dir_patterns:
            username_index = i + 1
            break
    
    # If this is just /Users/username with no deeper path, don't use username as project
    if username_index >= 0 and username_index < len(path_parts) and path_parts[username_index] == current_username:
        if len(path_parts) <= username_index + 1:
            return "Home Directory"
    
    if username_index >= 0 and username_index + 1 < len(path_parts):
        # First try specific project directories we know about by name
        known_projects = ['genaisf', 'cursor-view', 'cursor', 'cursor-apps', 'universal-github', 'inquiry']
        
        # Look at the most specific/deepest part of the path first
        for i in range(len(path_parts)-1, username_index, -1):
            if path_parts[i] in known_projects:
                project_name = path_parts[i]
                if debug:
                    logger.debug(f"Found known project name from specific list: {project_name}")
                break
        
        # If no known project found, use the last part of the path as it's likely the project directory
        if not project_name and len(path_parts) > username_index + 1:
            # Check if we have a structure like /Users/username/Documents/codebase/project_name
            if 'Documents' in path_parts and 'codebase' in path_parts:
                doc_index = path_parts.index('Documents')
                codebase_index = path_parts.index('codebase')
                
                # If there's a path component after 'codebase', use that as the project name
                if codebase_index + 1 < len(path_parts):
                    project_name = path_parts[codebase_index + 1]
                    if debug:
                        logger.debug(f"Found project name in Documents/codebase structure: {project_name}")
            
            # If no specific structure found, use the last component of the path
            if not project_name:
                project_name = path_parts[-1]
                if debug:
                    logger.debug(f"Using last path component as project name: {project_name}")
        
        # Skip username as project name
        if project_name == current_username:
            project_name = 'Home Directory'
            if debug:
                logger.debug(f"Avoided using username as project name")
        
        # Skip common project container directories
        project_containers = ['Documents', 'Projects', 'Code', 'workspace', 'repos', 'git', 'src', 'codebase']
        if project_name in project_containers:
            # Don't use container directories as project names
            # Try to use the next component if available
            container_index = path_parts.index(project_name)
            if container_index + 1 < len(path_parts):
                project_name = path_parts[container_index + 1]
                if debug:
                    logger.debug(f"Skipped container dir, using next component as project name: {project_name}")
        
        # If we still don't have a project name, use the first non-system directory after username
        if not project_name and username_index + 1 < len(path_parts):
            system_dirs = ['Library', 'Applications', 'System', 'var', 'opt', 'tmp']
            for i in range(username_index + 1, len(path_parts)):
                if path_parts[i] not in system_dirs and path_parts[i] not in project_containers:
                    project_name = path_parts[i]
                    if debug:
                        logger.debug(f"Using non-system dir as project name: {project_name}")
                    break
    else:
        # If not in a user directory, use the basename
        project_name = path_parts[-1] if path_parts else "Root"
        if debug:
            logger.debug(f"Using basename as project name: {project_name}")
    
    # Final check: don't return username as project name
    if project_name == current_username:
        project_name = "Home Directory"
        if debug:
            logger.debug(f"Final check: replaced username with 'Home Directory'")
    
    return project_name if project_name else "Unknown Project"

def workspace_info(db: pathlib.Path):
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        cur = con.cursor()

        # Get file paths from history entries to extract the project name
        proj = {"name": "(unknown)", "rootPath": "(unknown)"}
        ents = j(cur,"ItemTable","history.entries") or []
        
        # Extract file paths from history entries, stripping the file:/// scheme
        paths = []
        for e in ents:
            resource = e.get("editor", {}).get("resource", "")
            if resource and resource.startswith("file:///"):
                paths.append(resource[len("file:///"):])
        
        # If we found file paths, extract the project name using the longest common prefix
        if paths:
            logger.debug(f"Found {len(paths)} paths in history entries")
            
            # Get the longest common prefix
            common_prefix = os.path.commonprefix(paths)
            logger.debug(f"Common prefix: {common_prefix}")
            
            # Find the last directory separator in the common prefix
            last_separator_index = common_prefix.rfind('/')
            if last_separator_index > 0:
                project_root = common_prefix[:last_separator_index]
                logger.debug(f"Project root from common prefix: {project_root}")
                
                # Extract the project name using the helper function
                project_name = extract_project_name_from_path(project_root, debug=True)
                
                proj = {"name": project_name, "rootPath": "/" + project_root.lstrip('/')}
        
        # Try backup methods if we didn't get a project name
        if proj["name"] == "(unknown)":
            logger.debug("Trying backup methods for project name")
            
            # Check debug.selectedroot as a fallback
            selected_root = j(cur, "ItemTable", "debug.selectedroot")
            if selected_root and isinstance(selected_root, str) and selected_root.startswith("file:///"):
                path = selected_root[len("file:///"):]
                if path:
                    root_path = "/" + path.strip("/")
                    logger.debug(f"Project root from debug.selectedroot: {root_path}")
                    
                    # Extract the project name using the helper function
                    project_name = extract_project_name_from_path(root_path, debug=True)
                    
                    if project_name:
                        proj = {"name": project_name, "rootPath": root_path}

        # composers meta
        comp_meta={}
        cd = j(cur,"ItemTable","composer.composerData") or {}
        for c in cd.get("allComposers",[]):
            comp_meta[c["composerId"]] = {
                "title": c.get("name","(untitled)"),
                "createdAt": c.get("createdAt"),
                "lastUpdatedAt": c.get("lastUpdatedAt")
            }
        
        # Try to get composer info from workbench.panel.aichat.view.aichat.chatdata
        chat_data = j(cur, "ItemTable", "workbench.panel.aichat.view.aichat.chatdata") or {}
        for tab in chat_data.get("tabs", []):
            tab_id = tab.get("tabId")
            if tab_id and tab_id not in comp_meta:
                comp_meta[tab_id] = {
                    "title": f"Chat {tab_id[:8]}",
                    "createdAt": None,
                    "lastUpdatedAt": None
                }
    except sqlite3.DatabaseError as e:
        logger.debug(f"Error getting workspace info from {db}: {e}")
        proj = {"name": "(unknown)", "rootPath": "(unknown)"}
        comp_meta = {}
    finally:
        if 'con' in locals():
            con.close()
            
    return proj, comp_meta

################################################################################
# GlobalStorage
################################################################################
def global_storage_path(base: pathlib.Path) -> pathlib.Path:
    """Return path to the global storage state.vscdb."""
    global_db = base / "User" / "globalStorage" / "state.vscdb"
    if global_db.exists():
        return global_db
    
    # Legacy paths
    g_dirs = [base/"User"/"globalStorage"/"cursor.cursor",
              base/"User"/"globalStorage"/"cursor"]
    for d in g_dirs:
        if d.exists():
            for file in d.glob("*.sqlite"):
                return file
    
    return None

################################################################################
# Extraction pipeline
################################################################################
def extract_chats() -> list[Dict[str,Any]]:
    root = cursor_root()
    logger.debug(f"Using Cursor root: {root}")

    # Diagnostic: Check for AI-related keys in the first workspace
    if os.environ.get("CURSOR_CHAT_DIAGNOSTICS"):
        try:
            first_ws = next(workspaces(root))
            if first_ws:
                ws_id, db = first_ws
                logger.debug(f"\n--- DIAGNOSTICS for workspace {ws_id} ---")
                con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
                cur = con.cursor()
                
                # List all tables
                cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cur.fetchall()]
                logger.debug(f"Tables in workspace DB: {tables}")
                
                # Search for AI-related keys
                if "ItemTable" in tables:
                    for pattern in ['%ai%', '%chat%', '%composer%', '%prompt%', '%generation%']:
                        cur.execute("SELECT key FROM ItemTable WHERE key LIKE ?", (pattern,))
                        keys = [row[0] for row in cur.fetchall()]
                        if keys:
                            logger.debug(f"Keys matching '{pattern}': {keys}")
                
                con.close()
                
            # Check global storage
            global_db = global_storage_path(root)
            if global_db:
                logger.debug(f"\n--- DIAGNOSTICS for global storage ---")
                con = sqlite3.connect(f"file:{global_db}?mode=ro", uri=True)
                cur = con.cursor()
                
                # List all tables
                cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cur.fetchall()]
                logger.debug(f"Tables in global DB: {tables}")
                
                # Search for AI-related keys in ItemTable
                if "ItemTable" in tables:
                    for pattern in ['%ai%', '%chat%', '%composer%', '%prompt%', '%generation%']:
                        cur.execute("SELECT key FROM ItemTable WHERE key LIKE ?", (pattern,))
                        keys = [row[0] for row in cur.fetchall()]
                        if keys:
                            logger.debug(f"Keys matching '{pattern}': {keys}")
                
                # Check for keys in cursorDiskKV
                if "cursorDiskKV" in tables:
                    cur.execute("SELECT DISTINCT substr(key, 1, instr(key, ':') - 1) FROM cursorDiskKV")
                    prefixes = [row[0] for row in cur.fetchall()]
                    logger.debug(f"Key prefixes in cursorDiskKV: {prefixes}")
                
                con.close()
            
            logger.debug("\n--- END DIAGNOSTICS ---\n")
        except Exception as e:
            logger.debug(f"Error in diagnostics: {e}")

    # map lookups
    ws_proj  : Dict[str,Dict[str,Any]] = {}
    comp_meta: Dict[str,Dict[str,Any]] = {}
    comp2ws  : Dict[str,str]           = {}
    sessions : Dict[str,Dict[str,Any]] = defaultdict(lambda: {"messages":[]})

    # 1. Process workspace DBs first
    logger.debug("Processing workspace databases...")
    ws_count = 0
    for ws_id, db in workspaces(root):
        ws_count += 1
        logger.debug(f"Processing workspace {ws_id} - {db}")
        proj, meta = workspace_info(db)
        ws_proj[ws_id] = proj
        for cid, m in meta.items():
            comp_meta[cid] = m
            comp2ws[cid] = ws_id
        
        # Extract chat data from workspace's state.vscdb
        msg_count = 0
        for cid, role, text, db_path, code_blocks in iter_chat_from_item_table(db):
            # Add the message
            sessions[cid]["messages"].append({
                "role": role, 
                "content": text,
                "codeBlocks": code_blocks if code_blocks else []
            })
            # Make sure to record the database path
            if "db_path" not in sessions[cid]:
                sessions[cid]["db_path"] = db_path
            msg_count += 1
            if cid not in comp_meta:
                comp_meta[cid] = {"title": f"Chat {cid[:8]}", "createdAt": None, "lastUpdatedAt": None}
                comp2ws[cid] = ws_id
        logger.debug(f"  - Extracted {msg_count} messages from workspace {ws_id}")
    
    logger.debug(f"Processed {ws_count} workspaces")

    # 2. Process global storage
    global_db = global_storage_path(root)
    if global_db:
        logger.debug(f"Processing global storage: {global_db}")
        # Extract bubbles from cursorDiskKV
        msg_count = 0
        for cid, role, text, db_path, code_blocks in iter_bubbles_from_disk_kv(global_db):
            sessions[cid]["messages"].append({
                "role": role, 
                "content": text,
                "codeBlocks": code_blocks if code_blocks else []
            })
            # Record the database path
            if "db_path" not in sessions[cid]:
                sessions[cid]["db_path"] = db_path
            msg_count += 1
            if cid not in comp_meta:
                comp_meta[cid] = {"title": f"Chat {cid[:8]}", "createdAt": None, "lastUpdatedAt": None}
                comp2ws[cid] = "(global)"
        logger.debug(f"  - Extracted {msg_count} messages from global cursorDiskKV bubbles")
        
        # Extract composer data
        comp_count = 0
        for cid, data, db_path in iter_composer_data(global_db):
            if cid not in comp_meta:
                created_at = data.get("createdAt")
                comp_meta[cid] = {
                    "title": f"Chat {cid[:8]}",
                    "createdAt": created_at,
                    "lastUpdatedAt": created_at
                }
                comp2ws[cid] = "(global)"
            
            # Record the database path
            if "db_path" not in sessions[cid]:
                sessions[cid]["db_path"] = db_path
                
            # Extract conversation from composer data
            conversation = data.get("conversation", [])
            if conversation:
                msg_count = 0
                for msg in conversation:
                    msg_type = msg.get("type")
                    if msg_type is None:
                        continue
                    
                    # Type 1 = user, Type 2 = assistant
                    role = "user" if msg_type == 1 else "assistant"
                    content = msg.get("text", "")
                    if content and isinstance(content, str):
                        # Check for code blocks in the message
                        code_blocks = []
                        if "codeBlocks" in msg and isinstance(msg["codeBlocks"], list):
                            for block in msg["codeBlocks"]:
                                if isinstance(block, dict):
                                    code_content = block.get("content", "")
                                    lang_id = block.get("languageId", "")
                                    if code_content:
                                        code_blocks.append({
                                            "content": code_content,
                                            "language": lang_id
                                        })
                        
                        sessions[cid]["messages"].append({
                            "role": role, 
                            "content": content,
                            "codeBlocks": code_blocks
                        })
                        msg_count += 1
                
                if msg_count > 0:
                    comp_count += 1
                    logger.debug(f"  - Added {msg_count} messages from composer {cid[:8]}")
        
        if comp_count > 0:
            logger.debug(f"  - Extracted data from {comp_count} composers in global cursorDiskKV")
        
        # Also try ItemTable in global DB
        try:
            con = sqlite3.connect(f"file:{global_db}?mode=ro", uri=True)
            chat_data = j(con.cursor(), "ItemTable", "workbench.panel.aichat.view.aichat.chatdata")
            if chat_data:
                msg_count = 0
                for tab in chat_data.get("tabs", []):
                    tab_id = tab.get("tabId")
                    if tab_id and tab_id not in comp_meta:
                        comp_meta[tab_id] = {
                            "title": f"Global Chat {tab_id[:8]}",
                            "createdAt": None,
                            "lastUpdatedAt": None
                        }
                        comp2ws[tab_id] = "(global)"
                    
                    for bubble in tab.get("bubbles", []):
                        content = ""
                        if "text" in bubble:
                            content = bubble["text"]
                        elif "content" in bubble:
                            content = bubble["content"]
                        
                        if content and isinstance(content, str):
                            role = "user" if bubble.get("type") == "user" else "assistant"
                            
                            # Extract code blocks from this bubble
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
                            
                            sessions[tab_id]["messages"].append({
                                "role": role, 
                                "content": content,
                                "codeBlocks": code_blocks
                            })
                            msg_count += 1
                logger.debug(f"  - Extracted {msg_count} messages from global chat data")
            con.close()
        except Exception as e:
            logger.debug(f"Error processing global ItemTable: {e}")

    # 3. Build final list
    out = []
    for cid, data in sessions.items():
        if not data["messages"]:
            continue
        ws_id = comp2ws.get(cid, "(unknown)")
        project = ws_proj.get(ws_id, {"name": "(unknown)", "rootPath": "(unknown)"})
        meta = comp_meta.get(cid, {"title": "(untitled)", "createdAt": None, "lastUpdatedAt": None})
        
        # Create the output object with the db_path included
        chat_data = {
            "project": project,
            "session": {"composerId": cid, **meta},
            "messages": data["messages"],
            "workspace_id": ws_id,
        }
        
        # Add the database path if available
        if "db_path" in data:
            chat_data["db_path"] = data["db_path"]
            
        out.append(chat_data)
    
    # Sort by last updated time if available
    out.sort(key=lambda s: s["session"].get("lastUpdatedAt") or 0, reverse=True)
    logger.debug(f"Total chat sessions extracted: {len(out)}")
    return out

def extract_project_from_git_repos(workspace_id, debug=False):
    """
    Extract project name from the git repositories in a workspace.
    Returns None if no repositories found or unable to access the DB.
    """
    if not workspace_id or workspace_id == "unknown" or workspace_id == "(unknown)" or workspace_id == "(global)":
        if debug:
            logger.debug(f"Invalid workspace ID: {workspace_id}")
        return None
        
    # Find the workspace DB
    cursor_base = cursor_root()
    workspace_db_path = cursor_base / "User" / "workspaceStorage" / workspace_id / "state.vscdb"
    
    if not workspace_db_path.exists():
        if debug:
            logger.debug(f"Workspace DB not found for ID: {workspace_id}")
        return None
        
    try:
        # Connect to the workspace DB
        if debug:
            logger.debug(f"Connecting to workspace DB: {workspace_db_path}")
        con = sqlite3.connect(f"file:{workspace_db_path}?mode=ro", uri=True)
        cur = con.cursor()
        
        # Look for git repositories
        git_data = j(cur, "ItemTable", "scm:view:visibleRepositories")
        if not git_data or not isinstance(git_data, dict) or 'all' not in git_data:
            if debug:
                logger.debug(f"No git repositories found in workspace {workspace_id}, git_data: {git_data}")
            con.close()
            return None
            
        # Extract repo paths from the 'all' key
        repos = git_data.get('all', [])
        if not repos or not isinstance(repos, list):
            if debug:
                logger.debug(f"No repositories in 'all' key for workspace {workspace_id}, repos: {repos}")
            con.close()
            return None
            
        if debug:
            logger.debug(f"Found {len(repos)} git repositories in workspace {workspace_id}: {repos}")
            
        # Process each repo path
        for repo in repos:
            if not isinstance(repo, str):
                continue
                
            # Look for git:Git:file:/// pattern
            if "git:Git:file:///" in repo:
                # Extract the path part
                path = repo.split("file:///")[-1]
                path_parts = [p for p in path.split('/') if p]
                
                if path_parts:
                    # Use the last part as the project name
                    project_name = path_parts[-1]
                    if debug:
                        logger.debug(f"Found project name '{project_name}' from git repo in workspace {workspace_id}")
                    con.close()
                    return project_name
            else:
                if debug:
                    logger.debug(f"No 'git:Git:file:///' pattern in repo: {repo}")
                    
        if debug:
            logger.debug(f"No suitable git repos found in workspace {workspace_id}")
        con.close()
    except Exception as e:
        if debug:
            logger.debug(f"Error extracting git repos from workspace {workspace_id}: {e}")
        return None
        
    return None

def format_chat_for_frontend(chat):
    """Format the chat data to match what the frontend expects."""
    try:
        # Generate a unique ID for this chat if it doesn't have one
        session_id = str(uuid.uuid4())
        if 'session' in chat and chat['session'] and isinstance(chat['session'], dict):
            session_id = chat['session'].get('composerId', session_id)
        
        # Format date from createdAt timestamp or use current date
        date = int(datetime.datetime.now().timestamp())
        if 'session' in chat and chat['session'] and isinstance(chat['session'], dict):
            created_at = chat['session'].get('createdAt')
            if created_at and isinstance(created_at, (int, float)):
                # Convert from milliseconds to seconds
                date = created_at / 1000
        
        # Ensure project has expected fields
        project = chat.get('project', {})
        if not isinstance(project, dict):
            project = {}
            
        # Get workspace_id from chat
        workspace_id = chat.get('workspace_id', 'unknown')
        
        # Get the database path information
        db_path = chat.get('db_path', 'Unknown database path')
        
        # If project name is a username or unknown, try to extract a better name from rootPath
        if project.get('rootPath'):
            current_name = project.get('name', '')
            username = os.path.basename(os.path.expanduser('~'))
            
            # Check if project name is username or unknown or very generic
            if (current_name == username or 
                current_name == '(unknown)' or 
                current_name == 'Root' or
                # Check if rootPath is directly under /Users/username with no additional path components
                (project.get('rootPath').startswith(f'/Users/{username}') and 
                 project.get('rootPath').count('/') <= 3)):
                
                # Try to extract a better name from the path
                project_name = extract_project_name_from_path(project.get('rootPath'), debug=False)
                
                # Only use the new name if it's meaningful
                if (project_name and 
                    project_name != 'Unknown Project' and 
                    project_name != username and
                    project_name not in ['Documents', 'Downloads', 'Desktop']):
                    
                    logger.debug(f"Improved project name from '{current_name}' to '{project_name}'")
                    project['name'] = project_name
                elif project.get('rootPath').startswith(f'/Users/{username}/Documents/codebase/'):
                    # Special case for /Users/saharmor/Documents/codebase/X
                    parts = project.get('rootPath').split('/')
                    if len(parts) > 5:  # /Users/username/Documents/codebase/X
                        project['name'] = parts[5]
                        logger.debug(f"Set project name to specific codebase subdirectory: {parts[5]}")
                    else:
                        project['name'] = "cursor-view"  # Current project as default
        
        # If the project doesn't have a rootPath or it's very generic, enhance it with workspace_id
        if not project.get('rootPath') or project.get('rootPath') == '/' or project.get('rootPath') == '/Users':
            if workspace_id != 'unknown':
                # Use workspace_id to create a more specific path
                if not project.get('rootPath'):
                    project['rootPath'] = f"/workspace/{workspace_id}"
                elif project.get('rootPath') == '/' or project.get('rootPath') == '/Users':
                    project['rootPath'] = f"{project['rootPath']}/workspace/{workspace_id}"
        
        # FALLBACK: If project name is still generic, try to extract it from git repositories
        if project.get('name') in ['Home Directory', '(unknown)']:
            git_project_name = extract_project_from_git_repos(workspace_id, debug=True)
            if git_project_name:
                logger.debug(f"Improved project name from '{project.get('name')}' to '{git_project_name}' using git repo")
                project['name'] = git_project_name
        
        # Add workspace_id to the project data explicitly
        project['workspace_id'] = workspace_id
            
        # Ensure messages exist and are properly formatted
        messages = chat.get('messages', [])
        if not isinstance(messages, list):
            messages = []
            
        # Preserve code blocks in the messages
        formatted_messages = []
        code_blocks_count = 0
        
        for msg in messages:
            if not isinstance(msg, dict):
                continue
            
            formatted_msg = {
                'role': msg.get('role', 'user'),
                'content': msg.get('content', '')
            }
            
            # Preserve codeBlocks if they exist
            if 'codeBlocks' in msg and isinstance(msg['codeBlocks'], list):
                # Filter out empty code blocks or invalid ones
                valid_code_blocks = []
                for block in msg['codeBlocks']:
                    if isinstance(block, dict) and 'content' in block and block['content']:
                        # Ensure language is valid or set to a default
                        if 'language' not in block or not block['language']:
                            block['language'] = 'text'
                        valid_code_blocks.append(block)
                
                if valid_code_blocks:
                    formatted_msg['codeBlocks'] = valid_code_blocks
                    code_blocks_count += len(valid_code_blocks)
            
            formatted_messages.append(formatted_msg)
        
        logger.debug(f"Formatted {len(formatted_messages)} messages with {code_blocks_count} code blocks for frontend")
        
        # Create properly formatted chat object
        return {
            'project': project,
            'messages': formatted_messages,
            'date': date,
            'session_id': session_id,
            'workspace_id': workspace_id,
            'db_path': db_path  # Include the database path in the output
        }
    except Exception as e:
        logger.error(f"Error formatting chat: {e}")
        # Return a minimal valid object if there's an error
        return {
            'project': {'name': 'Error', 'rootPath': '/'},
            'messages': [],
            'date': int(datetime.datetime.now().timestamp()),
            'session_id': str(uuid.uuid4()),
            'workspace_id': 'error',
            'db_path': 'Error retrieving database path'
        }

@app.route('/api/chats', methods=['GET'])
def get_chats():
    """Get all chat sessions."""
    try:
        logger.info(f"Received request for chats from {request.remote_addr}")
        chats = extract_chats()
        logger.info(f"Retrieved {len(chats)} chats")
        
        # Format each chat for the frontend
        formatted_chats = []
        for chat in chats:
            try:
                formatted_chat = format_chat_for_frontend(chat)
                formatted_chats.append(formatted_chat)
            except Exception as e:
                logger.error(f"Error formatting individual chat: {e}")
                # Skip this chat if it can't be formatted
                continue
        
        logger.info(f"Returning {len(formatted_chats)} formatted chats")
        return jsonify(formatted_chats)
    except Exception as e:
        logger.error(f"Error in get_chats: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/<session_id>', methods=['GET'])
def get_chat(session_id):
    """Get a specific chat session by ID."""
    try:
        logger.info(f"Received request for chat {session_id} from {request.remote_addr}")
        chats = extract_chats()
        
        for chat in chats:
            # Check for a matching composerId safely
            if 'session' in chat and chat['session'] and isinstance(chat['session'], dict):
                if chat['session'].get('composerId') == session_id:
                    formatted_chat = format_chat_for_frontend(chat)
                    return jsonify(formatted_chat)
        
        logger.warning(f"Chat with ID {session_id} not found")
        return jsonify({"error": "Chat not found"}), 404
    except Exception as e:
        logger.error(f"Error in get_chat: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/<session_id>/export', methods=['GET'])
def export_chat(session_id):
    """Export a specific chat session as standalone HTML or JSON."""
    try:
        logger.info(f"Received request to export chat {session_id} from {request.remote_addr}")
        export_format = request.args.get('format', 'html').lower()
        chats = extract_chats()
        
        for chat in chats:
            # Check for a matching composerId safely
            if 'session' in chat and chat['session'] and isinstance(chat['session'], dict):
                if chat['session'].get('composerId') == session_id:
                    formatted_chat = format_chat_for_frontend(chat)
                    
                    if export_format == 'json':
                        # Export as JSON
                        return Response(
                            json.dumps(formatted_chat, indent=2),
                            mimetype="application/json; charset=utf-8",
                            headers={
                                "Content-Disposition": f'attachment; filename="cursor-chat-{session_id[:8]}.json"',
                                "Cache-Control": "no-store",
                            },
                        )
                    else:
                        # Default to HTML export
                        html_content = generate_standalone_html(formatted_chat)
                        return Response(
                            html_content,
                            mimetype="text/html; charset=utf-8",
                            headers={
                                "Content-Disposition": f'attachment; filename="cursor-chat-{session_id[:8]}.html"',
                                "Content-Length": str(len(html_content)),
                                "Cache-Control": "no-store",
                            },
                        )
        
        logger.warning(f"Chat with ID {session_id} not found for export")
        return jsonify({"error": "Chat not found"}), 404
    except Exception as e:
        logger.error(f"Error in export_chat: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

def generate_standalone_html(chat):
    """Generate a standalone HTML representation of the chat."""
    logger.info(f"Generating HTML for session ID: {chat.get('session_id', 'N/A')}")
    try:
        # Format date for display
        date_display = "Unknown date"
        if chat.get('date'):
            try:
                date_obj = datetime.datetime.fromtimestamp(chat['date'])
                date_display = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                logger.warning(f"Error formatting date: {e}")
        
        # Get project info
        project_name = chat.get('project', {}).get('name', 'Unknown Project')
        project_path = chat.get('project', {}).get('rootPath', 'Unknown Path')
        
        # Create HTML template with modern styling
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>%s - Cursor Chat</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/atom-one-dark.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
            <script>hljs.highlightAll();</script>
        </head>
        <body>
            <div class="chat-header">
                <div class="project-info">
                    <h1>%s</h1>
                    <div class="metadata">
                        <div class="date">%s</div>
                        <div class="path">%s</div>
                    </div>
                </div>
            </div>
        """ % (
            project_name, # title
            project_name, # h1
            date_display, # date
            project_path  # project path
        )
        
        # Prepare messages with code blocks properly formatted
        formatted_messages = []
        for msg in chat.get('messages', []):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            
            # Format code blocks if they exist separately
            code_blocks_html = ""
            if 'codeBlocks' in msg and msg['codeBlocks']:
                for code_block in msg['codeBlocks']:
                    language = code_block.get('language', '') or 'text'
                    code_content = code_block.get('content', '')
                    if code_content:
                        # Escape HTML in code
                        code_content = html.escape(code_content)
                        
                        code_blocks_html += f"""
                        <div class="code-block">
                            <div class="code-header">
                                <span class="language-label">{language}</span>
                            </div>
                            <pre><code class="language-{language}">{code_content}</code></pre>
                        </div>
                        """
            
            formatted_messages.append({
                    'role': role,
                    'content': content,
                    'code_blocks_html': code_blocks_html
                })

        # Add messages template
        html_content += """
            <div class="chat-container">
        """
        
        # Add each message
        for msg in formatted_messages:
            role_display = "You" if msg['role'] == 'user' else "Cursor Assistant"
            role_class = msg['role']
            
            # Convert markdown in regular content
            content_html = ""
            if msg['content']:
                try:
                    content_html = markdown.markdown(msg['content'])
                except Exception:
                    content_html = f"<p>{html.escape(msg['content'])}</p>"
            
            html_content += f"""
                <div class="message {role_class}-message">
                    <div class="message-header">
                        <div class="avatar {role_class}-avatar">
                            {role_display}
                        </div>
                    </div>
                    <div class="message-content">
            """
            
            # Add text content if present
            if content_html:
                html_content += f"""
                        <div class="text-content">
                            {content_html}
                    </div>
                """
            
            # Add code blocks if present
            if msg['code_blocks_html']:
                html_content += f"""
                        <div class="code-blocks">
                            {msg['code_blocks_html']}
                </div>
                """

            html_content += """
    </div>
    </div>
            """
        
        html_content += """
    </div>
        """
        
        # Add CSS styling
        html_content += """
        <style>
            /* Base styles */
            :root {
                --user-color: #00bbff;
                --assistant-color: #FF6B35;
                --background-color: #151617;
                --card-background: #1E1E1E;
                --text-color: #FFFFFF;
                --secondary-text: #B3B3B3;
                --border-color: #3E3E3E;
                --code-bg: #282c34;
            }
            
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                line-height: 1.6;
                color: var(--text-color);
                background-color: var(--background-color);
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            /* Header */
            .chat-header {
                background: linear-gradient(90deg, var(--user-color) 0%, rgba(0, 187, 255, 0.7) 100%);
                color: white;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            
            .project-info h1 {
                font-size: 24px;
                font-weight: 600;
                margin-bottom: 10px;
            }
            
            .metadata {
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                font-size: 14px;
            }
            
            .date, .path {
                background-color: rgba(255,255,255,0.2);
                border-radius: 4px;
                padding: 3px 8px;
                display: inline-block;
            }
            
            /* Messages */
            .chat-container {
                display: flex;
                flex-direction: column;
                gap: 24px;
            }
            
            .message {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .message-header {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .avatar {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                font-weight: 500;
                color: white;
            }
            
            .user-avatar {
                background-color: var(--user-color);
            }
            
            .assistant-avatar {
                background-color: var(--assistant-color);
            }
            
            .message-content {
                background-color: var(--card-background);
                border-radius: 10px;
                padding: 16px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-left: 4px solid;
            }
            
            .user-message .message-content {
                border-color: var(--user-color);
                margin-right: 40px;
            }
            
            .assistant-message .message-content {
                border-color: var(--assistant-color);
                margin-left: 40px;
            }
            
            .text-content {
                margin-bottom: 16px;
            }
            
            .text-content:last-child {
                margin-bottom: 0;
            }
            
            /* Code blocks */
            .code-block {
                margin: 16px 0;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            }
            
            .code-block:first-child {
                margin-top: 0;
            }
            
            .code-block:last-child {
                margin-bottom: 0;
            }
            
            .code-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 8px 12px;
                background-color: #2d333b;
                border-bottom: 1px solid #444;
            }
            
            .language-label {
                font-family: 'JetBrains Mono', monospace;
                font-size: 12px;
                color: #d7dae0;
                border-radius: 4px;
                padding: 2px 8px;
                background-color: rgba(255,255,255,0.1);
            }
            
            pre {
                margin: 0;
                padding: 16px;
                overflow-x: auto;
                background-color: var(--code-bg);
            }
            
            code {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                line-height: 1.5;
            }
            
            /* Markdown content styling */
            .text-content h1, .text-content h2, .text-content h3, 
            .text-content h4, .text-content h5, .text-content h6 {
                margin-top: 1em;
                margin-bottom: 0.5em;
            }
            
            .text-content p {
                margin-bottom: 1em;
            }
            
            .text-content ul, .text-content ol {
                margin-bottom: 1em;
                padding-left: 1.5em;
            }
            
            .text-content a {
                color: var(--user-color);
                text-decoration: none;
            }
            
            .text-content a:hover {
                text-decoration: underline;
            }
            
            .text-content img {
                max-width: 100%;
                border-radius: 4px;
            }
            
            .text-content code {
                font-family: 'JetBrains Mono', monospace;
                background-color: rgba(255,255,255,0.1);
                padding: 2px 4px;
                border-radius: 4px;
                font-size: 0.9em;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                body {
                    padding: 12px;
                }
                
                .user-message .message-content {
                    margin-right: 10px;
                }
                
                .assistant-message .message-content {
                    margin-left: 10px;
                }
            }
        </style>
</body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        logger.error(f"Error generating HTML: {e}")
        return f"<html><body><h1>Error generating HTML</h1><p>{str(e)}</p></body></html>"

# Serve React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path and Path(app.static_folder, path).exists():
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Cursor Chat View server')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    args = parser.parse_args()
    
    logger.info(f"Starting server on port {args.port}")
    app.run(host='127.0.0.1', port=args.port, debug=args.debug)