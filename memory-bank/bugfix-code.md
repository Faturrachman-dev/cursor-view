# JSON Export Bug Fix - Code Changes

## Current Implementation
`python
@app.route('/api/chat/<session_id>/export', methods=['GET'])
def export_chat(session_id):
    \
\\Export
a
specific
chat
session
as
standalone
HTML
or
JSON.\\\
    try:
        logger.info(f\Received
request
to
export
chat
session_id
from
request.remote_addr
\)
        export_format = request.args.get('format', 'html').lower()
        chats = extract_chats(detailed_logging=False)
        
        for chat in chats:
            # Check for a matching composerId safely
            if 'session' in chat and chat['session'] and isinstance(chat['session'], dict):
                if chat['session'].get('composerId') == session_id:
                    formatted_chat = format_chat_for_frontend(chat)
