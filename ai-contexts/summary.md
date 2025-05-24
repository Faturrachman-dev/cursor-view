Okay, here's a wiki-entry style summary of our development session for the Cursor View project.

---

## Wiki Entry: Cursor View - Code Block Display Enhancement

**Project:** Cursor View
**Date of Session:** 2025-05-14 (Simulated)
**Goal:** To enable the correct extraction, display, and export of code blocks within chat conversations from Cursor's local database.

### 1. Overview

The Cursor View application aims to provide a user-friendly interface to browse, search, and export chat histories from the Cursor AI-assisted code editor. This session focused on addressing a critical bug where code snippets shared during conversations were not being rendered in the web UI or included correctly in exports.

### 2. Initial Problem Statement

Users reported that code blocks, a vital part of AI-assisted coding conversations, were missing from the `cursor-view` web application's display and its JSON/HTML export functionalities. The application was only showing plain text messages.

### 3. Investigation and Discovery

The debugging process involved several stages:

1.  **Codebase Examination:** Initial review of `server.py` (Flask backend) and `extract_cursor_chat.py` (Python extraction logic) to understand how chat messages were processed.
2.  **Hypothesis Testing (Data Fields):** Explored various potential fields within the Cursor SQLite database (`state.vscdb`, `*.sqlite`) that might contain code, such as `text`, `richText`, `code`, `codeSnippet`, `markdown`, and nested `parts`.
3.  **Diagnostic Scripting:**
    *   `explore_cursor_db.py`: Created to inspect table schemas and sample data directly from Cursor's SQLite databases.
    *   `test_code_blocks.py`: Developed and iteratively enhanced to specifically trace how messages from a target chat session (identified by `TARGET_SESSION_ID` and `TARGET_WORKSPACE_ID`) were being processed by the extraction logic. This script simulated parts of the `server.py` pipeline.
4.  **Key Discovery:** The diagnostic scripts revealed that Cursor stores code snippets in a dedicated structured array field named `codeBlocks` within each message object. This field was separate from the main `text` content and contained objects, each with `content` (the code itself) and `languageId`.

### 4. Solution Implementation

The solution involved modifications to the backend, frontend, and HTML export functionality.

#### 4.1. Backend (Python)

*   **`server.py` & `extract_cursor_chat.py`:**
    *   Modified data extraction functions (`iter_bubbles_from_disk_kv`, `iter_chat_from_item_table`, `_iter_bubble_messages`) to explicitly look for and parse the `codeBlocks` array.
    *   Ensured that each extracted message object now includes a `codeBlocks` field, structured as an array of objects: `[{ "content": "...", "language": "..." }, ...]`.
    *   Updated the `format_chat_for_frontend` function to preserve the `codeBlocks` array in the data sent to the frontend.
    *   Corrected several indentation errors and logical flaws in message processing loops that were preventing `codeBlocks` from being consistently included.

#### 4.2. Frontend (React)

*   **`frontend/src/components/ChatDetail.js`:**
    *   Modified the component to check for the `message.codeBlocks` array.
    *   When present, iterate over `message.codeBlocks` and render each block using the `react-syntax-highlighter` library (with the Prism engine and `atomDark` style).
    *   Implemented a `normalizeLanguage` helper function to map language identifiers from Cursor (e.g., "golang", "py") to identifiers recognized by Prism (e.g., "go", "python").
    *   Added styling to display a language label (chip) for each code block and ensure proper visual presentation.
*   **`frontend/package.json`:** Added `react-syntax-highlighter` as a dependency.
*   **`frontend/public/index.html`:** Included CSS for Prism syntax highlighting themes.
*   **Build Process:** Addressed issues where frontend changes were not reflecting by instructing the user to run `npm install` and `npm run build` within the `frontend` directory to generate an updated production build.

#### 4.3. HTML Export

*   **`server.py` (within `generate_standalone_html` function):**
    *   Modified the HTML generation logic to iterate through `message.codeBlocks`.
    *   For each code block, generate `<pre><code class="language-...">...</code></pre>` tags.
    *   Included `highlight.js` CDN links and initialization script in the exported HTML for client-side syntax highlighting.
    *   Improved CSS for better visual presentation of code blocks in the exported HTML.

### 5. Key Challenges Encountered

*   **Undocumented Database Schema:** Cursor's SQLite database structure is not publicly documented, requiring manual exploration.
*   **Data Structure Mismatch:** Initial assumptions about code storage (e.g., as markdown within text) were incorrect.
*   **Python Indentation Errors:** Several subtle indentation errors in `server.py` complicated debugging.
*   **Frontend Build & Caching:** Changes to React components were not immediately visible in the browser until the frontend application was rebuilt and browser cache potentially cleared.
*   **Syntax Highlighter Integration:** Ensuring the `react-syntax-highlighter` library correctly received content and language props, and that its necessary CSS was loaded.

### 6. Testing and Diagnostics

*   **Python Scripts:** `test_code_blocks.py` was instrumental in verifying backend extraction.
*   **JavaScript Script:** `test_api_response.js` (using Axios) was created to check the structure of data served by the Flask API.
*   **Browser Developer Tools:** Used extensively to inspect console logs, network requests, and React component states.
*   **Manual JSON/HTML Export Inspection:** Regularly checked exported files to validate content.
*   **Static HTML Test Files:** Created `test-code-blocks.html` and `test-react-syntax-highlighter.html` to isolate and test syntax highlighting library behavior.

### 7. Documentation Updates

As a final step, the following documentation files were created/updated:

*   `README.md`: Updated with new features, including code block support.
*   `STRUCTURE.md`: Provided concise explanations for each file and component.
*   `CODEBLOCK_SUPPORT.md`: Detailed technical documentation about the code block implementation.
*   `CHANGELOG.md`: Documented the changes related to code block support.

### 8. Outcome

The Cursor View application now successfully extracts, displays (with syntax highlighting and language labels), and exports chat conversations that include code blocks. This significantly enhances the tool's usability for developers reviewing their AI-assisted coding sessions.

---