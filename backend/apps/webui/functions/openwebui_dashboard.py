"""
title: OpenWebUI Dashboard
author: MindX Team  
description: Quick access to all tools and features
version: 1.0.0
"""

from typing import Optional

class Filter:
    def __init__(self):
        self.valves = self.Valves()
        
    class Valves:
        enabled: bool = True
        
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Show dashboard on command"""
        
        if not self.valves.enabled:
            return body
            
        messages = body.get("messages", [])
        if not messages:
            return body
            
        last_msg = messages[-1].get("content", "").lower()
        
        if any(trigger in last_msg for trigger in ["/dashboard", "/tools", "/help", "/commands"]):
            dashboard_html = """
## 🎯 OpenWebUI Command Center

### 📝 Note-Taking
- `/notes` - Open Notesnook editor
- `save this` - Save conversation to notes

### 🧠 Memory & AI
- `/omi` - Open OMI memory assistant
- `search memories: [query]` - Search OMI memories
- `/think` - Enable thinking mode

### 🔍 Search & Research
- `search: [query]` - Web search
- `youtube: [url]` - Analyze YouTube video
- `/research [topic]` - Deep research mode

### 🔧 Integrations
- `/n8n [workflow]` - Trigger N8N workflow
- `/api [service]` - API integrations
- `/chart [data]` - Create visualizations

### 🤖 AI Models
- `/claude` - Switch to Claude
- `/gpt4` - Switch to GPT-4
- `/local` - Use local models

### 💾 Data Management
- `/export` - Export conversation
- `/backup` - Backup settings
- `/sync` - Sync across devices

### ⚙️ Settings
- `/config` - Configuration panel
- `/valves` - Adjust parameters
- `/status` - System status

**Pro Tips:**
- Combine commands: `/think search: quantum computing`
- Use natural language: "Save this and create a chart"
- Chain workflows: `/n8n process then /notes save`
"""
            
            messages.append({
                "role": "assistant",
                "content": dashboard_html
            })
            
        return body
        
    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
