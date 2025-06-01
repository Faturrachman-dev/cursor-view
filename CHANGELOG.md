# Changelog

All notable changes to the Cursor View project will be documented in this file.

## [1.2.0] - 2025-05-26

### Added
- Delete chat functionality now fully working
- Comprehensive documentation suite in the `documentation/` folder
- Enhanced logging for better debugging and troubleshooting
- Detailed error reporting in server logs

### Fixed
- Fixed 404 error when deleting chat sessions from the UI
- Fixed inconsistent session ID handling across endpoints

### Updated
- README.md with latest features and documentation links
- Memory Bank with complete project history and task tracking

## [1.1.0] - 2025-05-21

### Added
- Comprehensive server.py documentation
  - Main server architecture overview
  - API endpoints reference
  - Database structure documentation
  - Code reference for all major functions
  - Implementation details for bug fixes
- Memory Bank system for project task tracking and documentation

### Fixed
- Fixed 404 error when exporting chat sessions as JSON
- Updated export_chat function to use correct session_id property
- Added detailed logging for export functionality
- Improved efficiency with target_session_id parameter

## [1.0.0] - 2025-05-14

### Added
- Support for code blocks extraction and display
  - Proper extraction from SQLite database 
  - Preserved language information for syntax highlighting
  - Separate rendering from regular markdown text
  - Support in both HTML and JSON exports
- Full documentation for code block implementation in CODEBLOCK_SUPPORT.md

### Changed
- Improved database extraction logic to handle code blocks
- Enhanced UI rendering for code blocks with syntax highlighting
- Updated data pipeline to preserve code block structure

## [0.9.0] - Initial Release

### Features
- Browse all Cursor chat sessions
- Search through chat history
- Export chats as JSON or standalone HTML
- Organize chats by project
- View timestamps of conversations 