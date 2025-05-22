# Cursor View Documentation

This directory contains comprehensive documentation for the Cursor View application, a tool that allows users to browse, search, and export their Cursor AI chat histories.

## Documentation Files

- [**Server Documentation**](server_documentation.md): An overview of the server architecture, features, API endpoints, and deployment guidelines.
- [**Code Reference**](code_reference.md): Detailed reference for the main functions in the server.py file, including parameters, return values, and usage examples.
- [**Database Structure**](database_structure.md): Information about the SQLite database structure that Cursor View interacts with.

## Getting Started

To get started with Cursor View, refer to the [Installation & Setup](server_documentation.md#installation--setup) section in the server documentation.

## Contributing

If you'd like to contribute to Cursor View, please ensure you understand the codebase by reviewing the documentation provided here. When making changes:

1. Update the relevant documentation files to reflect your changes
2. Follow the code style and patterns established in the existing codebase
3. Add appropriate error handling and logging
4. Test your changes with different versions of Cursor

## Bug Fixes for JSON Export

The recent bug fix for JSON export addressed an issue where the `/api/chat/<session_id>/export?format=json` endpoint was returning a 404 error. The fix involved updating the export_chat function to use consistent session ID lookups.

### Bug Details

The bug occurred in the `export_chat` function when checking for a matching session ID. The function was looking for `chat['session']['composerId']` while the correct structure was `chat.get('session_id')`.

### Fix Implementation

The fix changed the session lookup logic to match the pattern used in the `get_chat` function, which was already working correctly.

```python
# Old code with bug:
if 'session' in chat and chat['session'] and isinstance(chat['session'], dict):
    if chat['session'].get('composerId') == session_id:

# Fixed code:
if chat.get('session_id') == session_id:
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 