# Changelog

## 2025-05-14: Code Block Support

### Added
- Support for extracting and displaying code blocks from Cursor chats
- Language-specific syntax highlighting for code blocks
- Improved HTML export with formatted code blocks
- JSON export with structured code block data
- Language labels for code blocks in the UI
- Test scripts for verifying code block extraction and rendering

### Fixed
- Fixed indentation errors in server.py
- Fixed missing code blocks in exported conversations
- Fixed HTML generation to include proper code block styling
- Fixed language mapping for syntax highlighter

### Technical Changes
- Updated server.py to extract code blocks from the database
- Enhanced message formatting in format_chat_for_frontend()
- Improved ChatDetail.js to properly render code blocks
- Added normalizeLanguage() helper function for consistent language identification
- Created test_code_blocks.py for database diagnostics
- Created test_api_response.js for API testing
- Added support for multiple language identifiers 