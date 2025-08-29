"""
Notesnook Action Functions
Interactive buttons for note operations in OpenWebUI
"""

async def handler(body, __user__=None, __event_emitter__=None, __event_call__=None):
    """
    Action function that adds note-taking buttons to messages
    """
    import json
    import hashlib
    from datetime import datetime
    from pathlib import Path
    import sqlite3
    
    # This function creates action buttons for note operations
    if not __event_call__:
        # Return action button configuration
        return {
            "actions": [
                {
                    "id": "save_note",
                    "label": "💾 Save as Note",
                    "icon": "save",
                    "description": "Save this message as a secure note"
                },
                {
                    "id": "create_task",
                    "label": "✅ Create Task",
                    "icon": "check-square",
                    "description": "Convert to action items"
                },
                {
                    "id": "add_tags",
                    "label": "🏷️ Add Tags",
                    "icon": "tag",
                    "description": "Categorize this content"
                },
                {
                    "id": "export_note",
                    "label": "📤 Export",
                    "icon": "upload",
                    "description": "Export to Markdown/JSON"
                }
            ]
        }
    
    # Handle action callbacks
    action = body.get("action")
    message_content = body.get("content", "")
    user_id = __user__.get("id", "default") if __user__ else "default"
    
    if action == "save_note":
        # Interactive save note flow
        if __event_call__:
            # Ask for note title
            response = await __event_call__({
                "type": "input",
                "data": {
                    "title": "Save as Note",
                    "message": "Enter a title for this note:",
                    "placeholder": "e.g., Meeting Notes, Project Ideas, etc."
                }
            })
            
            if response and response.get("input"):
                title = response["input"]
                
                # Ask for notebook selection
                notebook_response = await __event_call__({
                    "type": "select",
                    "data": {
                        "title": "Select Notebook",
                        "message": "Choose a notebook:",
                        "options": [
                            {"label": "📝 General", "value": "general"},
                            {"label": "💼 Work", "value": "work"},
                            {"label": "💡 Ideas", "value": "ideas"},
                            {"label": "📚 Learning", "value": "learning"},
                            {"label": "🎯 Projects", "value": "projects"},
                            {"label": "➕ Create New", "value": "new"}
                        ]
                    }
                })
                
                notebook = notebook_response.get("selection", "general") if notebook_response else "general"
                
                # If creating new notebook
                if notebook == "new":
                    new_notebook = await __event_call__({
                        "type": "input",
                        "data": {
                            "title": "New Notebook",
                            "message": "Enter notebook name:",
                            "placeholder": "e.g., Personal, Research, etc."
                        }
                    })
                    notebook = new_notebook.get("input", "general") if new_notebook else "general"
                
                # Save the note
                note_id = save_note_to_db(title, message_content, user_id, notebook)
                
                # Confirm save
                await __event_call__({
                    "type": "notification",
                    "data": {
                        "type": "success",
                        "title": "Note Saved",
                        "message": f"Note '{title}' saved to {notebook} (ID: {note_id})"
                    }
                })
                
                return f"✅ Note saved: **{title}** in 📚 {notebook}"
                
    elif action == "create_task":
        # Extract tasks from content
        tasks = extract_tasks(message_content)
        
        if __event_call__ and tasks:
            # Show extracted tasks for confirmation
            task_list = "\n".join([f"☐ {task}" for task in tasks])
            
            response = await __event_call__({
                "type": "confirm",
                "data": {
                    "title": "Create Tasks",
                    "message": f"Found {len(tasks)} tasks:\n\n{task_list}\n\nCreate these tasks?",
                    "confirm_label": "Create Tasks",
                    "cancel_label": "Cancel"
                }
            })
            
            if response and response.get("confirmed"):
                # Save tasks
                for task in tasks:
                    save_task_to_db(task, user_id)
                    
                await __event_call__({
                    "type": "notification",
                    "data": {
                        "type": "success",
                        "title": "Tasks Created",
                        "message": f"Created {len(tasks)} tasks successfully"
                    }
                })
                
                return f"✅ Created {len(tasks)} tasks"
        else:
            return "No tasks found in this message"
            
    elif action == "add_tags":
        if __event_call__:
            # Ask for tags
            response = await __event_call__({
                "type": "input",
                "data": {
                    "title": "Add Tags",
                    "message": "Enter tags (comma-separated):",
                    "placeholder": "e.g., important, project-x, review"
                }
            })
            
            if response and response.get("input"):
                tags = [tag.strip() for tag in response["input"].split(",")]
                
                # Save tags association
                save_tags(message_content, tags, user_id)
                
                tag_badges = " ".join([f"🏷️ {tag}" for tag in tags])
                return f"Added tags: {tag_badges}"
                
    elif action == "export_note":
        if __event_call__:
            # Ask for export format
            response = await __event_call__({
                "type": "select",
                "data": {
                    "title": "Export Format",
                    "message": "Choose export format:",
                    "options": [
                        {"label": "📝 Markdown (.md)", "value": "markdown"},
                        {"label": "📄 Plain Text (.txt)", "value": "text"},
                        {"label": "🔗 JSON (.json)", "value": "json"},
                        {"label": "📊 CSV (for tables)", "value": "csv"}
                    ]
                }
            })
            
            if response:
                format_type = response.get("selection", "markdown")
                exported_content = export_content(message_content, format_type)
                
                # Show export preview
                await __event_call__({
                    "type": "code",
                    "data": {
                        "title": f"Exported as {format_type.upper()}",
                        "code": exported_content,
                        "language": format_type
                    }
                })
                
                return f"📤 Exported as {format_type}"
    
    return body


def save_note_to_db(title, content, user_id, notebook):
    """Save note to database"""
    from pathlib import Path
    import sqlite3
    import hashlib
    
    db_path = Path.home() / ".openwebui" / "notesnook" / "notes.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Ensure tables exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            notebook TEXT,
            user_id TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    ''')
    
    note_id = hashlib.md5(f"{title}{datetime.now()}".encode()).hexdigest()[:8]
    
    cursor.execute('''
        INSERT INTO notes (id, title, content, notebook, user_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (note_id, title, content, notebook, user_id, datetime.now(), datetime.now()))
    
    conn.commit()
    conn.close()
    
    return note_id


def save_task_to_db(task, user_id):
    """Save task to database"""
    from pathlib import Path
    import sqlite3
    
    db_path = Path.home() / ".openwebui" / "notesnook" / "notes.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            user_id TEXT,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        INSERT INTO tasks (task, user_id, created_at)
        VALUES (?, ?, ?)
    ''', (task, user_id, datetime.now()))
    
    conn.commit()
    conn.close()


def save_tags(content, tags, user_id):
    """Save tags association"""
    from pathlib import Path
    import sqlite3
    
    db_path = Path.home() / ".openwebui" / "notesnook" / "notes.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT,
            content_hash TEXT,
            user_id TEXT,
            created_at TIMESTAMP
        )
    ''')
    
    content_hash = hashlib.md5(content.encode()).hexdigest()
    
    for tag in tags:
        cursor.execute('''
            INSERT INTO tags (tag, content_hash, user_id, created_at)
            VALUES (?, ?, ?, ?)
        ''', (tag, content_hash, user_id, datetime.now()))
    
    conn.commit()
    conn.close()


def extract_tasks(content):
    """Extract potential tasks from content"""
    import re
    
    tasks = []
    
    # Look for bullet points or numbered lists
    patterns = [
        r'[-*•]\s+(.+)',
        r'\d+\.\s+(.+)',
        r'TODO:\s*(.+)',
        r'Task:\s*(.+)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.MULTILINE)
        tasks.extend(matches)
    
    # Clean up tasks
    cleaned_tasks = []
    for task in tasks:
        task = task.strip()
        if len(task) > 5 and len(task) < 200:
            cleaned_tasks.append(task)
    
    return cleaned_tasks[:10]  # Limit to 10 tasks


def export_content(content, format_type):
    """Export content in different formats"""
    import json
    
    if format_type == "markdown":
        return f"""# Exported Note

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

{content}

---
*Exported from MindX Chat with Notesnook Integration*
"""
    
    elif format_type == "text":
        return f"""EXPORTED NOTE
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

{content}

--
Exported from MindX Chat with Notesnook Integration
"""
    
    elif format_type == "json":
        return json.dumps({
            "title": "Exported Note",
            "content": content,
            "date": datetime.now().isoformat(),
            "source": "MindX Chat",
            "integration": "Notesnook"
        }, indent=2)
    
    else:  # CSV for tables
        lines = content.split('\n')
        csv_content = "Line Number,Content\n"
        for i, line in enumerate(lines, 1):
            csv_content += f"{i},\"{line.replace('\"', '\"\"')}\"\n"
        return csv_content