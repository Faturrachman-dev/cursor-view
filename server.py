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

# Configure logging to write to a file
log_directory = Path("logs")
log_directory.mkdir(exist_ok=True)
log_file = log_directory / "cursor_view.log"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # Keep console logging but at INFO level
    ]
)
# Set console handler to INFO level, while file handler remains at DEBUG
logging.getLogger().handlers[1].setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.info(f"Logging to file: {log_file}")

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

def iter_bubbles_from_disk_kv(db: pathlib.Path, detailed_logging=False, target_session_id=None) -> Iterable[tuple[str,str,str,str,list,bool,dict,dict,int]]:
    """Yield (composerId, role, text, db_path, code_blocks, is_thought, thinking, tool_former_data, capability_type) from cursorDiskKV table."""
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
                
            # Only debug this session if it matches the target_session_id or if no target specified
            should_log_details = detailed_logging and (target_session_id is None or composer_id == target_session_id)
        
            # Log the raw bubble data for diagnostics only when detailed logging is enabled for this session
            if should_log_details:
                logger.debug(f"Raw bubble data for composer {composer_id}: {json.dumps(bubble, indent=2)}")
            
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
            
            # Extract additional fields
            is_thought = bubble.get("isThought", False)
            thinking = bubble.get("thinking", {})
            tool_former_data = bubble.get("toolFormerData", {})
            capability_type = bubble.get("capabilityType", None)
                            
            # Skip bubbles with no content - but allow thought or tool data bubbles even without text
            if not text and not code_blocks and not is_thought and not tool_former_data:
                continue

            role = "user" if bubble.get("type") == 1 else "assistant"
            yield composer_id, role, text, db_path_str, code_blocks, is_thought, thinking, tool_former_data, capability_type
            
        except Exception as e:
            logger.debug(f"Error processing bubble: {e}")

def iter_chat_from_item_table(db: pathlib.Path, detailed_logging=False, target_session_id=None) -> Iterable[tuple[str,str,str,str,list,bool,dict,dict,int]]:
    """Yield (composerId, role, text, db_path, code_blocks, is_thought, thinking, tool_former_data, capability_type) from ItemTable."""
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        cur = con.cursor()
        
        # Try to get chat data from workbench.panel.aichat.view.aichat.chatdata
        chat_data = j(cur, "ItemTable", "workbench.panel.aichat.view.aichat.chatdata")
        if chat_data and "tabs" in chat_data:
            for tab in chat_data.get("tabs", []):
                tab_id = tab.get("tabId", "unknown")
                
                # Only debug this tab if it matches the target_session_id or if no target specified
                should_log_details = detailed_logging and (target_session_id is None or tab_id == target_session_id)
                
                for bubble in tab.get("bubbles", []):
                    bubble_type = bubble.get("type")
                    if not bubble_type:
                        continue
                    
                    # Log the raw bubble data for diagnostics only when detailed logging is enabled for this session
                    if should_log_details:
                        logger.debug(f"Raw bubble data from ItemTable for tab {tab_id}: {json.dumps(bubble, indent=2)}")
                    
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
                    
                    # Extract additional fields
                    is_thought = bubble.get("isThought", False)
                    thinking = bubble.get("thinking", {})
                    tool_former_data = bubble.get("toolFormerData", {})
                    capability_type = bubble.get("capabilityType", None)
                    
                    # Skip bubbles with no content - but allow thought or tool data bubbles even without text
                    if not text and not code_blocks and not is_thought and not tool_former_data:
                        continue
    
                    role = "user" if bubble_type == 1 else "assistant"
                    yield tab_id, role, text, str(db), code_blocks, is_thought, thinking, tool_former_data, capability_type

    except Exception as e:
        logger.debug(f"Error in iter_chat_from_item_table: {e}")

def iter_composer_data(db: pathlib.Path, detailed_logging=False, target_session_id=None) -> Iterable[tuple[str,dict,str]]:
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
            
            # Only debug this composer if it matches the target_session_id or if no target specified
            should_log_details = detailed_logging and (target_session_id is None or composer_id == target_session_id)
            
            # Log the raw composer data for diagnostics only when detailed logging is enabled for this session
            if should_log_details:
                logger.debug(f"Raw composer data for composer {composer_id}: {json.dumps(composer_data, indent=2)}")
            
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
def extract_chats(detailed_logging=False, target_session_id=None) -> list[Dict[str,Any]]:
    """Extract all chat sessions from disk."""
    # Set up root directory and create sessions dictionary
    root = cursor_root()
    if not root:
        logger.error(f"Could not find Cursor Data directory")
        return []
    
    sessions = defaultdict(lambda: {"messages": []})
    ws_proj = {}
    comp_meta = {}
    comp2ws = {}
    
    logger.info(f"Extracting chats from {root}")

    # 1. Process workspace DBs first
    logger.debug("Processing workspace databases...")
    ws_count = 0
    for ws_id, db in workspaces(root):
        ws_count += 1
        if detailed_logging:
            logger.debug(f"Processing workspace {ws_id} - {db}")
        proj, meta = workspace_info(db)
        ws_proj[ws_id] = proj
        for cid, m in meta.items():
            comp_meta[cid] = m
            comp2ws[cid] = ws_id
        
        # Extract chat data from workspace's state.vscdb
        msg_count = 0
        for cid, role, text, db_path, code_blocks, is_thought, thinking, tool_former_data, capability_type in iter_chat_from_item_table(db, detailed_logging, target_session_id):
            # Add the message
            sessions[cid]["messages"].append({
                "role": role, 
                "content": text,
                "codeBlocks": code_blocks,
                "is_thought": is_thought,
                "thinking": thinking,
                "tool_former_data": tool_former_data,
                "capability_type": capability_type
            })
            sessions[cid]["db_path"] = db_path
            sessions[cid]["workspace_id"] = ws_id
            sessions[cid]["session_id"] = cid
            msg_count += 1
        
        if detailed_logging and msg_count > 0:
            logger.debug(f"  - Found {msg_count} chat messages")

    logger.info(f"Processed {ws_count} workspaces")
    
    # 2. Process global storage DB
    gs_path = global_storage_path(root)
    if not gs_path:
        logger.warning(f"Could not find global storage path")
    else:
        if detailed_logging:
            logger.debug(f"Processing global storage DB: {gs_path}")
        
        # Extract chat data from global state.vscdb
        msg_count_global = 0
        
        # First try DiskKV bubbles
        for cid, role, text, db_path, code_blocks, is_thought, thinking, tool_former_data, capability_type in iter_bubbles_from_disk_kv(gs_path, detailed_logging, target_session_id):
            # Add the message
            sessions[cid]["messages"].append({
                "role": role, 
                "content": text,
                "codeBlocks": code_blocks,
                "is_thought": is_thought,
                "thinking": thinking,
                "tool_former_data": tool_former_data,
                "capability_type": capability_type
            })
            sessions[cid]["db_path"] = db_path
            sessions[cid]["session_id"] = cid
            msg_count_global += 1
        
        # Then try ItemTable
        for cid, role, text, db_path, code_blocks, is_thought, thinking, tool_former_data, capability_type in iter_chat_from_item_table(gs_path, detailed_logging, target_session_id):
            # Add the message
            sessions[cid]["messages"].append({
                "role": role, 
                "content": text,
                "codeBlocks": code_blocks,
                "is_thought": is_thought,
                "thinking": thinking,
                "tool_former_data": tool_former_data,
                "capability_type": capability_type
            })
            sessions[cid]["db_path"] = db_path
            sessions[cid]["session_id"] = cid
            msg_count_global += 1
        
        if detailed_logging and msg_count_global > 0:
            logger.debug(f"  - Found {msg_count_global} chat messages in global storage")
        
        # Get composer data metadata from global storage DB
        comp_count = 0
        for cid, data, db_path in iter_composer_data(gs_path, detailed_logging, target_session_id):
            if cid in sessions:
                comp_meta[cid] = data
                sessions[cid]["composer_data"] = data
                sessions[cid]["db_path"] = db_path
                comp_count += 1
            
        if detailed_logging and comp_count > 0:
            logger.debug(f"  - Found {comp_count} composer metadata records")
    
    # 3. Add workspace project info to sessions
    for cid, session in sessions.items():
        if "workspace_id" in session and session["workspace_id"] in ws_proj:
            session["project"] = ws_proj[session["workspace_id"]]
        elif cid in comp2ws and comp2ws[cid] in ws_proj:
            session["project"] = ws_proj[comp2ws[cid]]
            session["workspace_id"] = comp2ws[cid]
        else:
            # Try to extract from git info
            session["project"] = extract_project_from_git_repos(None, detailed_logging)
    
    # 4. Add metadata to sessions and sort messages
    results = []
    session_count = 0
    for cid, session in sessions.items():
        if target_session_id and cid != target_session_id:
            continue
            
        # Skip sessions with no messages
        if not session["messages"]:
            continue
        
        # Sort messages by date if available
        session["messages"].sort(key=lambda m: m.get("date", 0) if isinstance(m.get("date"), (int, float)) else 0)
        
        # Add metadata
        if cid in comp_meta:
            metadata = comp_meta[cid]
            
            if "createdAt" in metadata:
                try:
                    created_at = metadata["createdAt"]
                    if isinstance(created_at, str):
                        session["date"] = int(datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00')).timestamp())
                    else:
                        session["date"] = int(created_at / 1000)  # Convert ms to seconds
                except Exception as e:
                    if detailed_logging:
                        logger.warning(f"Error parsing date: {e}")
            
            if "title" in metadata:
                session["title"] = metadata["title"]
        
        # Format the result
        result = {
            "session_id": cid,
            "messages": session["messages"],
            "date": session.get("date", 0),
            "title": session.get("title", "Untitled Chat"),
            "project": session.get("project", {"name": "Unknown Project"}),
            "workspace_id": session.get("workspace_id"),
            "db_path": session.get("db_path"),
        }
        
        results.append(result)
        session_count += 1
    
    # Sort by date descending (newest first)
    results.sort(key=lambda x: x.get("date", 0), reverse=True)
    
    logger.info(f"Extracted {session_count} chat sessions with messages")
    
    return results

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
    """Format chat for frontend display, processing special elements like code blocks."""
    try:
        formatted_messages = []
        code_blocks_count = 0
        
        if not chat or "messages" not in chat:
            logger.warning("Invalid chat data for formatting")
            return {"messages": []}
        
        for msg in chat.get("messages", []):
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
            
            # Add thinking and tool_former data for advanced UI features
            if msg.get('is_thought'):
                formatted_msg['is_thought'] = True
            
            if 'thinking' in msg and msg['thinking']:
                formatted_msg['thinking'] = msg['thinking']
                # Format the thinking HTML for display in the UI
                if isinstance(msg['thinking'], dict) and 'text' in msg['thinking'] and msg['thinking']['text']:
                    thinking_text = html.escape(msg['thinking']['text'])
                    formatted_msg['thinking_html'] = f"""
                    <div class="thinking-block">
                        <div class="thinking-header">
                            <span class="thinking-label">AI Thought Process</span>
                        </div>
                        <div class="thinking-content">
                            {thinking_text}
                        </div>
                    </div>
                    """

            if 'tool_former_data' in msg and msg['tool_former_data']:
                formatted_msg['tool_former_data'] = msg['tool_former_data']
                # Format the tool call HTML for display in the UI
                tool_former_data = msg['tool_former_data']
                if isinstance(tool_former_data, dict):
                    tool_name = tool_former_data.get('name', 'Unknown Tool')
                    tool_status = tool_former_data.get('status', 'unknown')
                    tool_params = tool_former_data.get('params') or tool_former_data.get('rawArgs', {})
                    tool_result = tool_former_data.get('result', '')
                    
                    # Format parameters for HTML display
                    params_html = ""
                    if tool_params:
                        try:
                            if isinstance(tool_params, str):
                                params_json = json.loads(tool_params)
                            else:
                                params_json = tool_params
                            params_str = json.dumps(params_json, indent=2)
                            params_html = f"""
                            <div class="tool-params">
                                <div class="tool-section-header">Parameters:</div>
                                <pre><code class="language-json">{html.escape(params_str)}</code></pre>
                            </div>
                            """
                        except:
                            params_html = f"""
                            <div class="tool-params">
                                <div class="tool-section-header">Parameters:</div>
                                <pre>{html.escape(str(tool_params))}</pre>
                            </div>
                            """
                    
                    # Format result for HTML display
                    result_html = ""
                    if tool_result:
                        try:
                            if isinstance(tool_result, str):
                                # Try to parse as JSON
                                result_json = json.loads(tool_result)
                                result_str = json.dumps(result_json, indent=2)
                            else:
                                result_str = json.dumps(tool_result, indent=2)
                            result_html = f"""
                            <div class="tool-result">
                                <div class="tool-section-header">Result:</div>
                                <pre><code class="language-json">{html.escape(result_str)}</code></pre>
                            </div>
                            """
                        except:
                            result_html = f"""
                            <div class="tool-result">
                                <div class="tool-section-header">Result:</div>
                                <pre>{html.escape(str(tool_result))}</pre>
                            </div>
                            """
                    
                    status_class = "success" if tool_status == "completed" else "error" if tool_status == "error" else "pending"
                    status_icon = "✅" if tool_status == "completed" else "❌" if tool_status == "error" else "⏳"
                    
                    formatted_msg['tool_call_html'] = f"""
                    <div class="tool-call-block">
                        <div class="tool-call-header status-{status_class}">
                            <span class="tool-name">Called Tool: {tool_name}</span>
                            <span class="tool-status">{status_icon}</span>
                        </div>
                        {params_html}
                        {result_html}
                    </div>
                    """
            
            formatted_messages.append(formatted_msg)
        
        logger.debug(f"Formatted {len(formatted_messages)} messages with {code_blocks_count} code blocks for frontend")
        
        return {
            "messages": formatted_messages,
            "title": chat.get("title", "Untitled Chat"),
            "project": chat.get("project", {}),
            "date": chat.get("date", 0),
            "session_id": chat.get("session_id", "")
        }
    except Exception as e:
        logger.error(f"Error formatting chat for frontend: {e}")
        return {"messages": []}

@app.route('/api/chats', methods=['GET'])
def get_chats():
    """Get all chat sessions."""
    try:
        logger.info(f"Received request for chats from {request.remote_addr}")
        # Don't use detailed logging for the chat list view
        chats = extract_chats(detailed_logging=False)
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
        # Use detailed logging ONLY for the specific session being viewed
        chats = extract_chats(detailed_logging=True, target_session_id=session_id)
        
        for chat in chats:
            # Check for direct session_id match in the chat object
            if chat.get('session_id') == session_id:
                formatted_chat = format_chat_for_frontend(chat)
                return jsonify(formatted_chat)
        
        logger.warning(f"Chat with ID {session_id} not found")
        return jsonify({"error": "Chat not found"}), 404
    except Exception as e:
        logger.error(f"Error in get_chat: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/<session_id>', methods=['DELETE'])
def delete_chat(session_id):
    """Delete a specific chat session by ID."""
    try:
        logger.info(f"Received request to delete chat {session_id} from {request.remote_addr}")
        
        # Extract all chats to find the one we want to delete
        chats = extract_chats(detailed_logging=False)
        chat_to_delete = None
        
        for chat in chats:
            # Check for a matching composerId safely
            if 'session' in chat and chat['session'] and isinstance(chat['session'], dict):
                if chat['session'].get('composerId') == session_id:
                    chat_to_delete = chat
                    break
        
        if not chat_to_delete:
            logger.warning(f"Chat with ID {session_id} not found for deletion")
            return jsonify({"error": "Chat not found"}), 404
        
        # Get db_path from the chat
        db_path = chat_to_delete.get('db_path')
        if not db_path:
            return jsonify({"error": "Database path not found for this chat"}), 400
        
        # Get composer ID
        composer_id = None
        if 'session' in chat_to_delete and chat_to_delete['session'] and isinstance(chat_to_delete['session'], dict):
            composer_id = chat_to_delete['session'].get('composerId')
        
        if not composer_id:
            return jsonify({"error": "Composer ID not found for this chat"}), 400
        
        # Delete chat from database
        success = delete_chat_from_db(db_path, composer_id)
        
        if success:
            logger.info(f"Successfully deleted chat {session_id}")
            return jsonify({"success": True, "message": "Chat deleted successfully"})
        else:
            logger.error(f"Failed to delete chat {session_id}")
            return jsonify({"error": "Failed to delete chat"}), 500
        
    except Exception as e:
        logger.error(f"Error in delete_chat: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

def delete_chat_from_db(db_path, composer_id):
    """Delete a chat from the database.
    
    Args:
        db_path (str): Path to the database file
        composer_id (str): Composer ID of the chat to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        logger.info(f"Attempting to delete chat with composer ID {composer_id} from {db_path}")
        
        # Verify the database file exists
        if not os.path.exists(db_path):
            logger.error(f"Database file {db_path} does not exist")
            return False
        
        # Connect to the database
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
        # Check if it's in cursorDiskKV table (global storage)
        try:
            # First check if the table exists
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cursorDiskKV'")
            if cur.fetchone():
                # Delete bubble data
                cur.execute("DELETE FROM cursorDiskKV WHERE key LIKE ?", (f'bubbleId:{composer_id}%',))
                # Delete composer data
                cur.execute("DELETE FROM cursorDiskKV WHERE key = ?", (f'composerData:{composer_id}',))
                logger.info(f"Deleted chat data from cursorDiskKV table, rows affected: {cur.rowcount}")
        except sqlite3.Error as e:
            logger.error(f"Error deleting from cursorDiskKV: {e}")
        
        # Check if it's in ItemTable (workspace or global)
        try:
            # First check if the table exists
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ItemTable'")
            if cur.fetchone():
                # For ItemTable, we need to modify the JSON data
                cur.execute("SELECT key, value FROM ItemTable WHERE key = 'workbench.panel.aichat.view.aichat.chatdata'")
                row = cur.fetchone()
                
                if row:
                    key, value = row
                    try:
                        chat_data = json.loads(value)
                        if "tabs" in chat_data:
                            # Filter out the tab with matching ID
                            original_tabs_length = len(chat_data["tabs"])
                            chat_data["tabs"] = [tab for tab in chat_data["tabs"] if tab.get("tabId") != composer_id]
                            
                            if len(chat_data["tabs"]) < original_tabs_length:
                                # Update the record with the modified JSON
                                cur.execute(
                                    "UPDATE ItemTable SET value = ? WHERE key = 'workbench.panel.aichat.view.aichat.chatdata'",
                                    (json.dumps(chat_data),)
                                )
                                logger.info(f"Updated chat data in ItemTable, removed tab with ID {composer_id}")
                    except json.JSONDecodeError as e:
                        logger.error(f"Error parsing JSON from ItemTable: {e}")
        except sqlite3.Error as e:
            logger.error(f"Error updating ItemTable: {e}")
        
        # Commit changes and close connection
        con.commit()
        con.close()
        
        logger.info(f"Successfully deleted chat with composer ID {composer_id} from {db_path}")
        return True
    
    except Exception as e:
        logger.error(f"Error in delete_chat_from_db: {e}", exc_info=True)
        return False

@app.route('/api/chat/<session_id>/export', methods=['GET'])
def export_chat(session_id):
    """Export a specific chat session as standalone HTML or JSON."""
    try:
        logger.info(f"Received request to export chat {session_id} from {request.remote_addr}")
        export_format = request.args.get('format', 'html').lower()
        # Use detailed_logging for easier debugging, but only for the specific session
        chats = extract_chats(detailed_logging=True, target_session_id=session_id)
        
        for chat in chats:
            # Use the same pattern as get_chat which works correctly
            if chat.get('session_id') == session_id:
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
            is_thought = msg.get('is_thought', False)
            thinking = msg.get('thinking', {})
            tool_former_data = msg.get('tool_former_data', {})
            
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
            
            # Add thinking and tool_former data for advanced UI features
            if msg.get('is_thought'):
                formatted_msg['is_thought'] = True
            
            if 'thinking' in msg and msg['thinking']:
                formatted_msg['thinking'] = msg['thinking']
                # Format the thinking HTML for display in the UI
                if isinstance(msg['thinking'], dict) and 'text' in msg['thinking'] and msg['thinking']['text']:
                    thinking_text = html.escape(msg['thinking']['text'])
                    formatted_msg['thinking_html'] = f"""
                    <div class="thinking-block">
                        <div class="thinking-header">
                            <span class="thinking-label">AI Thought Process</span>
                        </div>
                        <div class="thinking-content">
                            {thinking_text}
                        </div>
                    </div>
                    """

            if 'tool_former_data' in msg and msg['tool_former_data']:
                formatted_msg['tool_former_data'] = msg['tool_former_data']
                # Format the tool call HTML for display in the UI
                tool_former_data = msg['tool_former_data']
                if isinstance(tool_former_data, dict):
                    tool_name = tool_former_data.get('name', 'Unknown Tool')
                    tool_status = tool_former_data.get('status', 'unknown')
                    tool_params = tool_former_data.get('params') or tool_former_data.get('rawArgs', {})
                    tool_result = tool_former_data.get('result', '')
                    
                    # Format parameters for HTML display
                    params_html = ""
                    if tool_params:
                        try:
                            if isinstance(tool_params, str):
                                params_json = json.loads(tool_params)
                            else:
                                params_json = tool_params
                            params_str = json.dumps(params_json, indent=2)
                            params_html = f"""
                            <div class="tool-params">
                                <div class="tool-section-header">Parameters:</div>
                                <pre><code class="language-json">{html.escape(params_str)}</code></pre>
                            </div>
                            """
                        except:
                            params_html = f"""
                            <div class="tool-params">
                                <div class="tool-section-header">Parameters:</div>
                                <pre>{html.escape(str(tool_params))}</pre>
                            </div>
                            """
                    
                    # Format result for HTML display
                    result_html = ""
                    if tool_result:
                        try:
                            if isinstance(tool_result, str):
                                # Try to parse as JSON
                                result_json = json.loads(tool_result)
                                result_str = json.dumps(result_json, indent=2)
                            else:
                                result_str = json.dumps(tool_result, indent=2)
                            result_html = f"""
                            <div class="tool-result">
                                <div class="tool-section-header">Result:</div>
                                <pre><code class="language-json">{html.escape(result_str)}</code></pre>
                            </div>
                            """
                        except:
                            result_html = f"""
                            <div class="tool-result">
                                <div class="tool-section-header">Result:</div>
                                <pre>{html.escape(str(tool_result))}</pre>
                            </div>
                            """
                    
                    status_class = "success" if tool_status == "completed" else "error" if tool_status == "error" else "pending"
                    status_icon = "✅" if tool_status == "completed" else "❌" if tool_status == "error" else "⏳"
                    
                    formatted_msg['tool_call_html'] = f"""
                    <div class="tool-call-block">
                        <div class="tool-call-header status-{status_class}">
                            <span class="tool-name">Called Tool: {tool_name}</span>
                            <span class="tool-status">{status_icon}</span>
                        </div>
                        {params_html}
                        {result_html}
                    </div>
                    """
            
            formatted_messages.append(formatted_msg)

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
                            {role_display[0]}
                        </div>
                        <div class="header-text">{role_display}</div>
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
            if 'codeBlocks' in msg and isinstance(msg['codeBlocks'], list) and msg['codeBlocks']:
                code_blocks_html = ""
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
                
                if code_blocks_html:
                    html_content += f"""
                            <div class="code-blocks">
                                {code_blocks_html}
                            </div>
                    """
            
            # Add thinking content if present
            if msg['thinking_html']:
                html_content += f"""
                        <div class="thinking-blocks">
                            {msg['thinking_html']}
                        </div>
                """
            
            # Add tool call content if present
            if msg['tool_call_html']:
                html_content += f"""
                        <div class="tool-call-blocks">
                            {msg['tool_call_html']}
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
                --thinking-bg: #2d3748;
                --thinking-border: #4a5568;
                --tool-header-bg: #2b4562;
                --tool-success-color: #48BB78;
                --tool-error-color: #F56565;
                --tool-pending-color: #ECC94B;
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
            
            .header-text {
                font-weight: 500;
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
            .code-blocks {
                margin-top: 16px;
            }
            
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
            
            /* Thinking blocks */
            .thinking-blocks {
                margin-top: 16px;
            }
            
            .thinking-block {
                background-color: var(--thinking-bg);
                border: 1px solid var(--thinking-border);
                border-radius: 8px;
                margin-bottom: 16px;
                overflow: hidden;
            }
            
            .thinking-header {
                background-color: rgba(0,0,0,0.2);
                padding: 8px 12px;
                border-bottom: 1px solid var(--thinking-border);
            }
            
            .thinking-label {
                font-family: 'JetBrains Mono', monospace;
                font-size: 12px;
                color: #a0aec0;
                display: flex;
                align-items: center;
            }
            
            .thinking-content {
                padding: 12px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                white-space: pre-wrap;
                color: #e2e8f0;
            }
            
            /* Tool call blocks */
            .tool-call-blocks {
                margin-top: 16px;
            }
            
            .tool-call-block {
                border-radius: 8px;
                overflow: hidden;
                border: 1px solid rgba(102, 179, 255, 0.3);
                margin-bottom: 16px;
                background-color: rgba(30, 41, 59, 0.8);
            }
            
            .tool-call-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 8px 12px;
                border-bottom: 1px solid rgba(102, 179, 255, 0.2);
                border-left: 4px solid;
            }
            
            .status-success {
                background-color: rgba(43, 69, 98, 0.7);
                border-left-color: var(--tool-success-color);
            }
            
            .status-error {
                background-color: rgba(43, 69, 98, 0.7);
                border-left-color: var(--tool-error-color);
            }
            
            .status-pending {
                background-color: rgba(43, 69, 98, 0.7);
                border-left-color: var(--tool-pending-color);
            }
            
            .tool-name {
                font-family: 'JetBrains Mono', monospace;
                font-weight: 500;
                font-size: 14px;
            }
            
            .tool-status {
                font-size: 16px;
            }
            
            .tool-params, .tool-result {
                padding: 12px;
                border-bottom: 1px solid rgba(102, 179, 255, 0.2);
            }
            
            .tool-result {
                border-bottom: none;
            }
            
            .tool-section-header {
                color: rgba(156, 220, 254, 0.7);
                font-weight: 500;
                font-size: 12px;
                margin-bottom: 8px;
                display: block;
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
        logger.error(f"Error generating HTML: {e}")
        return f"<html><body><h1>Error generating HTML</h1><p>{str(e)}</p></body></html>"

@app.route('/api/chat/<session_id>/raw', methods=['GET'])
def get_raw_chat(session_id):
    """Get raw chat data for diagnostic purposes."""
    try:
        logger.info(f"Received request for raw chat data {session_id} from {request.remote_addr}")
        # Enable detailed logging ONLY for the specific session being viewed
        chats = extract_chats(detailed_logging=True, target_session_id=session_id)
        
        # Find the chat with the matching session_id
        target_chat = None
        for chat in chats:
            if 'session' in chat and chat['session'] and isinstance(chat['session'], dict):
                if chat['session'].get('composerId') == session_id:
                    target_chat = chat
                    break
        
        if not target_chat:
            logger.warning(f"Chat with ID {session_id} not found for raw data view")
            return jsonify({"error": "Chat not found"}), 404
        
        # Check if we need to extract raw bubble data from the database
        db_path = target_chat.get('db_path')
        if not db_path:
            return jsonify({"error": "Database path not found for this chat"}), 400
        
        # Connect to the database and get raw data
        raw_bubbles = []
        try:
            con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            cur = con.cursor()
            
            # Check for cursorDiskKV table
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cursorDiskKV'")
            if cur.fetchone():
                # Get raw bubble data
                cur.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE ?", (f'bubbleId:{session_id}%',))
                for k, v in cur.fetchall():
                    if v is not None:
                        try:
                            bubble_data = json.loads(v)
                            raw_bubbles.append({
                                "key": k,
                                "data": bubble_data
                            })
                        except Exception as e:
                            logger.error(f"Error parsing JSON for bubble {k}: {e}")
                
                # Get composer data
                cur.execute("SELECT value FROM cursorDiskKV WHERE key = ?", (f'composerData:{session_id}',))
                row = cur.fetchone()
                composer_data = None
                if row and row[0]:
                    try:
                        composer_data = json.loads(row[0])
                    except Exception as e:
                        logger.error(f"Error parsing JSON for composer data: {e}")
            
            # Check ItemTable for this chat
            item_table_data = None
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ItemTable'")
            if cur.fetchone():
                cur.execute("SELECT value FROM ItemTable WHERE key = 'workbench.panel.aichat.view.aichat.chatdata'")
                row = cur.fetchone()
                if row and row[0]:
                    try:
                        chat_data = json.loads(row[0])
                        # Find the tab with this session ID
                        if 'tabs' in chat_data:
                            for tab in chat_data['tabs']:
                                if tab.get('tabId') == session_id:
                                    item_table_data = tab
                                    break
                    except Exception as e:
                        logger.error(f"Error parsing JSON from ItemTable: {e}")
            
            con.close()
            
            return jsonify({
                "session_id": session_id,
                "raw_bubbles": raw_bubbles,
                "composer_data": composer_data,
                "item_table_data": item_table_data,
                "formatted_messages": target_chat.get("messages", [])
            })
            
        except Exception as e:
            logger.error(f"Error getting raw data: {e}", exc_info=True)
            return jsonify({"error": f"Error getting raw data: {str(e)}"}), 500
        
    except Exception as e:
        logger.error(f"Error in get_raw_chat: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

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