# Code Block Support in Cursor View

This document describes the implementation of code block support in Cursor View, including the challenges encountered and solutions applied.

## Background

Cursor AI (the VS Code-based code editor) allows users to interact with an AI assistant that can generate and discuss code. When code is shared in conversations, it is stored in a specialized way in Cursor's database.

Initially, Cursor View only extracted the text content from messages, missing the code blocks that were stored separately in a specialized `codeBlocks` field. This led to code snippets being missing from exported chats.

## Implementation

### 1. Database Extraction

The first step was modifying the database extraction functions to properly identify and extract code blocks:

- In `server.py`, we updated `iter_bubbles_from_disk_kv()` and `iter_chat_from_item_table()` to recognize the `codeBlocks` array in the message object
- Each code block is extracted with both its content and language identifier (when available)
- Code blocks are stored in a separate array alongside the regular message text

```python
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
```

### 2. Message Formatting

We updated `format_chat_for_frontend()` to include code blocks when formatting messages for the frontend:

```python
# Preserve code blocks in the messages
formatted_messages = []
for msg in messages:
    if not isinstance(msg, dict):
        continue
    
    formatted_msg = {
        'role': msg.get('role', 'user'),
        'content': msg.get('content', '')
    }
    
    # Preserve codeBlocks if they exist
    if 'codeBlocks' in msg and isinstance(msg['codeBlocks'], list):
        formatted_msg['codeBlocks'] = msg['codeBlocks']
    
    formatted_messages.append(formatted_msg)
```

### 3. Frontend Rendering

The most complex part was updating the React frontend to properly render code blocks with syntax highlighting:

1. We enhanced `ChatDetail.js` to handle separate code blocks:
   - Added a language normalization function to map language identifiers to ones supported by the syntax highlighter
   - Implemented proper styling for code blocks
   - Added language labels to show what language each block uses

2. We integrated `react-syntax-highlighter` with Prism for code highlighting:
   ```jsx
   <SyntaxHighlighter
     language={normalizeLanguage(codeBlock.language || 'text')}
     style={atomDark}
     showLineNumbers={true}
     customStyle={{
       margin: 0,
       borderRadius: 0,
       background: message.role === 'user' 
         ? alpha(colors.primary.main, 0.07) 
         : alpha(colors.highlightColor, 0.15),
       padding: '32px 16px 16px 16px',
     }}
   >
     {codeBlock.content || ''}
   </SyntaxHighlighter>
   ```

### 4. HTML Export

We updated the HTML export functionality to include formatted code blocks:

```python
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
```

## Challenges Encountered

1. **Database Structure**: Cursor's database structure is complex and not well-documented, requiring exploration to understand how code blocks are stored.

2. **Indentation Errors**: Several indentation errors in the original code needed to be fixed.

3. **UI Rendering**: Getting the code blocks to display correctly in the UI with proper syntax highlighting required careful configuration of the React components.

4. **Edge Cases**: Handling missing language identifiers, empty code blocks, and other edge cases was necessary for robust implementation.

## Testing

We created two test scripts to verify the code block extraction and rendering:

1. `test_code_blocks.py`: Directly examines the database to confirm code blocks are correctly extracted
2. `test_api_response.js`: Tests the API responses to ensure code blocks are included in the JSON output

## Future Improvements

Possible future enhancements to the code block functionality:

1. Support for copying code blocks with a single click
2. Better handling of very long code blocks (horizontal scrolling)
3. Collapsible code blocks for large conversations
4. Theme selection for syntax highlighting 