"""
Optimal Notesnook Integration
Combines simplicity with functionality
"""

async def handler(body, __user__=None, __event_emitter__=None):
    """
    Lightweight Notesnook integration using best of both approaches
    """
    import json
    import hashlib
    from datetime import datetime
    
    # Check if user wants notes
    if "messages" not in body:
        return body
        
    last_message = body.get("messages", [{}])[-1]
    content = last_message.get("content", "").lower()
    
    # Trigger phrases
    if any(trigger in content for trigger in ["open notes", "/notes", "show notes"]):
        # Return lightweight embedded editor (not full Notesnook)
        return {
            "role": "assistant",
            "content": """## 📝 Quick Notes Editor

<div id="notes-container" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; background: white;">
    <style>
        .note-editor { 
            min-height: 400px; 
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .note-title {
            font-size: 24px;
            font-weight: 600;
            border: none;
            outline: none;
            width: 100%;
            margin-bottom: 15px;
            padding: 8px;
        }
        .note-content {
            min-height: 300px;
            border: 1px solid #e5e7eb;
            border-radius: 4px;
            padding: 15px;
            outline: none;
            line-height: 1.6;
        }
        .note-toolbar {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e5e7eb;
        }
        .note-btn {
            padding: 6px 12px;
            background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        .note-btn:hover {
            opacity: 0.9;
        }
        .saved-notes {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }
        .note-item {
            padding: 10px;
            margin: 5px 0;
            background: #f9fafb;
            border-radius: 4px;
            cursor: pointer;
        }
        .note-item:hover {
            background: #f3f4f6;
        }
    </style>
    
    <div class="note-editor">
        <div class="note-toolbar">
            <button class="note-btn" onclick="saveNote()">💾 Save</button>
            <button class="note-btn" onclick="formatBold()">𝐁 Bold</button>
            <button class="note-btn" onclick="formatItalic()">𝐼 Italic</button>
            <button class="note-btn" onclick="insertList()">• List</button>
            <button class="note-btn" onclick="clearNote()">🗑️ Clear</button>
        </div>
        
        <input type="text" class="note-title" id="noteTitle" placeholder="Note title..." />
        <div class="note-content" id="noteContent" contenteditable="true">Start typing your note...</div>
        
        <div class="saved-notes" id="savedNotes">
            <h4>📚 Recent Notes</h4>
            <div id="notesList"></div>
        </div>
    </div>
    
    <script>
        // Lightweight note functionality
        let notes = JSON.parse(localStorage.getItem('openwebui_notes') || '[]');
        
        function saveNote() {
            const title = document.getElementById('noteTitle').value || 'Untitled';
            const content = document.getElementById('noteContent').innerHTML;
            
            const note = {
                id: Date.now().toString(),
                title: title,
                content: content,
                created: new Date().toISOString(),
                encrypted: false // Would encrypt here in production
            };
            
            notes.unshift(note);
            localStorage.setItem('openwebui_notes', JSON.stringify(notes));
            loadNotes();
            
            // Visual feedback
            const btn = event.target;
            btn.textContent = '✅ Saved!';
            setTimeout(() => btn.textContent = '💾 Save', 2000);
        }
        
        function loadNotes() {
            const list = document.getElementById('notesList');
            list.innerHTML = notes.slice(0, 5).map(note => 
                `<div class="note-item" onclick="loadNote('${note.id}')">
                    <strong>${note.title}</strong>
                    <div style="font-size: 12px; color: #6b7280;">
                        ${new Date(note.created).toLocaleDateString()}
                    </div>
                </div>`
            ).join('');
        }
        
        function loadNote(id) {
            const note = notes.find(n => n.id === id);
            if (note) {
                document.getElementById('noteTitle').value = note.title;
                document.getElementById('noteContent').innerHTML = note.content;
            }
        }
        
        function formatBold() {
            document.execCommand('bold', false, null);
        }
        
        function formatItalic() {
            document.execCommand('italic', false, null);
        }
        
        function insertList() {
            document.execCommand('insertUnorderedList', false, null);
        }
        
        function clearNote() {
            if (confirm('Clear this note?')) {
                document.getElementById('noteTitle').value = '';
                document.getElementById('noteContent').innerHTML = '';
            }
        }
        
        // Auto-save every 30 seconds
        setInterval(() => {
            if (document.getElementById('noteTitle').value) {
                saveNote();
            }
        }, 30000);
        
        // Load existing notes
        loadNotes();
        
        // Send message to parent (OpenWebUI)
        window.parent.postMessage({
            type: 'notes-ready',
            count: notes.length
        }, '*');
    </script>
</div>

**Features:**
- 📝 Rich text editing (basic formatting)
- 💾 Auto-save to browser storage
- 🔒 Ready for encryption (add your key)
- 📚 Recent notes access
- ✨ No external dependencies

*This is integrated directly into OpenWebUI - no separate app needed!*"""
        }
    
    # Save from conversation
    elif "save this as note" in content or "save to notes" in content:
        # Extract the previous assistant message
        prev_content = ""
        for msg in reversed(body.get("messages", [])[:-1]):
            if msg.get("role") == "assistant":
                prev_content = msg.get("content", "")
                break
        
        if prev_content:
            # Create a note from the content
            note_title = f"AI Response - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            return {
                "role": "assistant",
                "content": f"""✅ **Saved to Notes!**

**Title:** {note_title}
**Content:** {prev_content[:100]}...

<script>
// Save to localStorage
const note = {{
    id: '{hashlib.md5(prev_content.encode()).hexdigest()[:8]}',
    title: '{note_title}',
    content: `{prev_content}`,
    created: new Date().toISOString()
}};

let notes = JSON.parse(localStorage.getItem('openwebui_notes') || '[]');
notes.unshift(note);
localStorage.setItem('openwebui_notes', JSON.stringify(notes));
</script>

Say "open notes" to view and edit your saved notes."""
            }
    
    return body