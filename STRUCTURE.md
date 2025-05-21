# Project Structure

```
└── 📁cursor-view                          # Root project directory
    └── 📁export                           # Directory containing exported chat files
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
        └── package-lock.json              # NPM package lock file
        └── package.json                   # NPM package configuration
        └── 📁public                       # Public assets for the React app
            └── favicon.ico                # Favicon source
            └── index.html                 # HTML template
            └── manifest.json              # Web app manifest source
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
    └── extract_cursor_chat.py             # Core module for extracting chat data from databases
    └── LICENSE                            # Project license
    └── package-lock.json                  # NPM package lock file
    └── package.json                       # NPM package configuration
    └── README.md                          # Project documentation and setup instructions
    └── requirements.txt                   # Python dependencies
    └── server.py                          # Main Python backend server (Flask)
```
