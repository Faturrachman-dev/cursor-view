# Project Structure

```
└── 📁cursor-view                          # Root project directory
    └── 📁cursor_chat_viewer               # Legacy viewer files
        └── index.html                     # Original HTML viewer (legacy)
    └── 📁export                           # Directory containing exported chat files
        └── cursor-chat-66277016 (2).json  # Example of JSON chat export
        └── cursor-chat-66277016 (3).json  # Another JSON export
        └── cursor-chat-66277016 (4).json  # Latest JSON export with code blocks
    └── 📁frontend                         # React frontend application
        └── 📁build                        # Compiled production build of the React app
            └── asset-manifest.json        # Asset mapping for the build
            └── favicon.ico                # Favicon
            └── index.html                 # Main HTML entry point
            └── manifest.json              # Web app manifest
            └── 📁static                   # Static assets
                └── 📁css                  # Compiled CSS files
                    └── main.35335c5e.css  # Main CSS file
                    └── main.35335c5e.css.map # Source map for CSS
                └── 📁js                   # Compiled JavaScript files
                    └── main.ce2d036f.js   # Main JavaScript bundle
                    └── main.ce2d036f.js.LICENSE.txt # License notices
                    └── main.ce2d036f.js.map # Source map for JS
            └── test-code-blocks.html      # Test page for code block rendering
            └── test-react-syntax-highlighter.html # Test for syntax highlighter
        └── package-lock.json              # NPM package lock file
        └── package.json                   # NPM package configuration
        └── 📁public                       # Public assets for the React app
            └── favicon.ico                # Favicon source
            └── index.html                 # HTML template
            └── manifest.json              # Web app manifest source
            └── test-code-blocks.html      # Test HTML for code blocks
            └── test-react-syntax-highlighter.html # Test for syntax highlighter
        └── 📁src                          # React source code
            └── App.js                     # Main App component
            └── 📁components               # React components
                └── ChatDetail.js          # Chat detail view component (displays conversations w/ code blocks)
                └── ChatList.js            # Chat list component (displays all chats)
                └── Header.js              # Header component
            └── index.css                  # Global CSS
            └── index.js                   # React entry point
    └── .gitignore                         # Git ignore file
    └── cursor_chat_finder.py              # Utility to find Cursor chat files
    └── diagnostic_extraction_result.json  # Diagnostic output from extraction process
    └── diagnostic_formatted_result.json   # Diagnostic output after formatting
    └── explore_cursor_db.py               # Tool to explore Cursor's SQLite databases
    └── extract_cursor_chat.py             # Core module for extracting chat data from databases
    └── extract_single_chat.py             # Utility to extract a single chat by ID
    └── import_fixed_chat.py               # Utility to import fixed chat data
    └── LICENSE                            # Project license
    └── package-lock.json                  # NPM package lock file
    └── package.json                       # NPM package configuration
    └── problems.txt                       # Documentation of known issues
    └── README.md                          # Project documentation and setup instructions
    └── requirements.txt                   # Python dependencies
    └── server.py                          # Main Python backend server (Flask)
    └── test_api_response.js               # JavaScript test for API responses
    └── test_code_blocks.py                # Test script for code block extraction
    └── vscdb_to_sqlite.py                 # Utility to convert VSCode database to SQLite
```