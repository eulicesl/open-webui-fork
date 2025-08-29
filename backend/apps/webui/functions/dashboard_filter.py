"""
title: MindX Dashboard
author: MindX Team
author_url: https://github.com/mindx-team
funding_url: https://github.com/mindx-team
version: 1.0.0
description: Central command dashboard for all OpenWebUI features
required_open_webui_version: 0.3.0
"""

from pydantic import BaseModel, Field
from typing import Optional
import json


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Priority level for filter operations"
        )
        enabled: bool = Field(
            default=True, description="Enable or disable the dashboard"
        )

    class UserValves(BaseModel):
        show_commands: bool = Field(
            default=True, description="Show command list in dashboard"
        )

    def __init__(self):
        self.valves = self.Valves()

    async def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Process incoming messages for dashboard commands"""
        print(f"Dashboard inlet - checking for commands")
        
        if not self.valves.enabled:
            return body
            
        messages = body.get("messages", [])
        if not messages:
            return body
            
        last_msg = messages[-1].get("content", "").lower()
        
        # Dashboard triggers
        triggers = ["/dashboard", "/help", "/commands", "/tools", "show commands"]
        
        if any(trigger in last_msg for trigger in triggers):
            dashboard_content = """# 🎯 MindX Command Center

## 📝 Note-Taking & Memory
- **`/notes`** - Open Notesnook professional editor
- **`/omi`** or **`/memory`** - Open MindX Memory (powered by OMI)
- **`save this`** - Save conversation to notes
- **`search memories: [query]`** - Search your memories

## 🔍 Search & Research
- **`search: [query]`** - Real-time web search
- **`research: [topic]`** - Deep research mode
- **`youtube: [url]`** - Analyze YouTube videos
- **`analyze: [url]`** - Analyze any webpage

## 📊 Data & Visualization
- **`create chart`** - Generate visualization from data
- **`visualize: [data]`** - Create interactive charts
- **`export data`** - Export conversation data

## 🤖 AI Enhancements
- **`/think`** - Enable step-by-step reasoning
- **`/claude`** - Use Claude model
- **`/gpt4`** - Use GPT-4 model
- **`/models`** - List available models

## 🔧 Automation & Integration
- **`/n8n`** - Trigger N8N workflows
- **`/api [service]`** - API integrations
- **`/webhook`** - Webhook triggers

## ⚙️ System & Settings
- **`/status`** - System status check
- **`/config`** - Configuration settings
- **`/valves`** - Adjust parameters
- **`/functions`** - List active functions

## 💡 Pro Tips
- Combine commands: `search: AI news then save this`
- Use natural language: "Take a note about this"
- Chain workflows: `/n8n process then /notes`

---
*MindX Dashboard v1.0 - Type any command to get started!*"""

            # Replace the last message with dashboard
            messages[-1] = {
                "role": "assistant",
                "content": dashboard_content
            }
            
        return body

    async def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Process outgoing messages"""
        return body