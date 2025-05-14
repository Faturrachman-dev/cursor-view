#!/usr/bin/env python3
"""
Script to import our fixed chat export directly into the server's cache
so it can be viewed in the web interface.
"""

import os
import json
import shutil
import pathlib
from pathlib import Path

# The fixed JSON file to import
SOURCE_FILE = "export/cursor-chat-5c439b02-9d08-4fd2-9b22-8e47cef5aa23-fixed.json"

def backup_existing_export():
    """Backup the original export file if it exists."""
    original_file = "export/cursor-chat-5c439b02.json"
    backup_file = "export/cursor-chat-5c439b02.json.backup"
    
    if os.path.exists(original_file) and not os.path.exists(backup_file):
        print(f"Backing up original export to {backup_file}")
        shutil.copy2(original_file, backup_file)

def import_fixed_chat():
    """Import the fixed chat into the original export file."""
    fixed_file = SOURCE_FILE
    target_file = "export/cursor-chat-5c439b02.json"
    
    if not os.path.exists(fixed_file):
        print(f"Error: Fixed chat file {fixed_file} not found")
        return False
    
    # Backup the original file
    backup_existing_export()
    
    # Copy the fixed file to the target location
    print(f"Importing fixed chat from {fixed_file} to {target_file}")
    shutil.copy2(fixed_file, target_file)
    
    return True

def main():
    """Import the fixed chat and provide instructions."""
    success = import_fixed_chat()
    
    if success:
        print("\nSuccessfully imported fixed chat!")
        print("\nTo view the chat with code blocks:")
        print("1. Make sure the server is running (python server.py)")
        print("2. Open http://localhost:5000 in your browser")
        print("3. Find and click on the conversation")
        print("4. You should now see the chat with properly formatted code blocks")
        print("\nYou can also export the chat as HTML to see the code blocks with syntax highlighting.")
    else:
        print("\nFailed to import fixed chat.")

if __name__ == "__main__":
    main() 