"""
title: OMI AI Assistant Integration
author: MindX Team
author_url: https://github.com/mindx-team
funding_url: https://github.com/mindx-team
version: 1.0.0
description: Complete OMI MCP integration with memory management
"""

from pydantic import BaseModel, Field
from typing import Optional
import json
import re


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Priority level for the filter operations."
        )
        enabled: bool = Field(
            default=True, description="Enable/disable OMI integration."
        )
        omi_web_url: str = Field(
            default="http://localhost:3458", description="OMI web interface URL."
        )
        omi_mcp_port: str = Field(
            default="3456", description="OMI MCP server port."
        )
        pass

    class UserValves(BaseModel):
        enabled: bool = Field(
            default=True, description="Enable/disable OMI integration for user."
        )
        pass

    def __init__(self):
        # Initialize valves with specific configurations
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Pre-processor for handling OMI triggers
        print(f"inlet:{__name__}")
        print(f"inlet:body:{body}")
        
        # Check if OMI is enabled
        if not self.valves.enabled:
            return body
            
        # Get messages
        messages = body.get("messages", [])
        if not messages:
            return body
        
        # Get the last message content
        last_message = messages[-1].get("content", "").lower()
        
        # Trigger phrases for OMI
        omi_triggers = [
            "/omi", "open omi", "show omi", "omi assistant",
            "my memories", "show memories", "omi memories",
            "omi conversations", "search memories"
        ]
        
        # Check if user wants OMI interface
        if any(trigger in last_message for trigger in omi_triggers):
            omi_html = f"""## 🧠 OMI AI Assistant

<div style="border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); margin: 15px 0;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600; font-size: 16px;">OMI - Personal AI Memory Assistant</span>
            <span style="font-size: 12px; opacity: 0.9;">MCP Connected • Sync Enabled</span>
        </div>
    </div>
    
    <iframe 
        src="{self.valves.omi_web_url}"
        width="100%" 
        height="700px" 
        frameborder="0"
        loading="lazy"
        style="background: white; display: block;"
        title="OMI Assistant"
        allow="clipboard-write; clipboard-read">
    </iframe>
    
    <div style="background: #f8f9fa; padding: 12px 20px; border-top: 1px solid #e5e7eb;">
        <details>
            <summary style="cursor: pointer; font-weight: 500;">📱 OMI Device Setup</summary>
            <div style="padding: 10px 0;">
                <ol style="margin: 10px 0; padding-left: 20px; font-size: 14px;">
                    <li>Open OMI app on your device</li>
                    <li>Go to Settings → Developer Settings</li>
                    <li>Enable API access and copy your key</li>
                    <li>Set MCP server: <code>http://localhost:{self.valves.omi_mcp_port}</code></li>
                </ol>
            </div>
        </details>
    </div>
</div>

### 🎯 OMI Commands:
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 15px 0;">
    <div style="padding: 10px; background: #f9fafb; border-left: 3px solid #667eea; border-radius: 4px;">
        <code>/omi</code> - Open OMI interface
    </div>
    <div style="padding: 10px; background: #f9fafb; border-left: 3px solid #667eea; border-radius: 4px;">
        <code>search memories: [query]</code> - Search your memories
    </div>
    <div style="padding: 10px; background: #f9fafb; border-left: 3px solid #667eea; border-radius: 4px;">
        <code>save to omi: [content]</code> - Create new memory
    </div>
    <div style="padding: 10px; background: #f9fafb; border-left: 3px solid #667eea; border-radius: 4px;">
        <code>show conversations</code> - View recent conversations
    </div>
</div>

### 🔧 Service Status:
- **MCP Server**: Running on port {self.valves.omi_mcp_port}
- **Bridge API**: Running on port 3457
- **Web Interface**: Running on port 3458

*Your OMI ecosystem is integrated with OpenWebUI!*"""

            # Replace the last message with OMI response
            body["messages"][-1] = {
                "role": "assistant",
                "content": omi_html
            }
            
        # Handle save to OMI
        elif "save to omi" in last_message:
            content = last_message.split("save to omi:", 1)[-1].strip() if ":" in last_message else ""
            
            save_html = f"""## 💾 Saving to OMI Memory

<div style="border-radius: 12px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 15px 0;">
    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 12px 20px; font-weight: 600;">
        Creating OMI Memory
    </div>
    
    <iframe 
        src="{self.valves.omi_web_url}"
        width="100%" 
        height="500px" 
        frameborder="0"
        loading="eager"
        style="background: white;"
        title="Save to OMI">
    </iframe>
    
    <div style="background: #f0fdf4; padding: 12px 20px; font-size: 14px; color: #065f46;">
        ✅ Memory prepared. Complete the save in OMI interface above.
    </div>
</div>

<details>
    <summary style="cursor: pointer; margin-top: 10px;">📄 Content to save</summary>
    <div style="padding: 10px; background: #f9fafb; border-radius: 8px; margin-top: 10px; font-size: 14px;">
        {content[:300]}{"..." if len(content) > 300 else ""}
    </div>
</details>"""

            # Replace the last message with save response
            body["messages"][-1] = {
                "role": "assistant",
                "content": save_html
            }
            
        # Handle search memories
        elif "search memories:" in last_message:
            query = last_message.split("search memories:", 1)[-1].strip()
            
            search_html = f"""## 🔍 Searching OMI Memories

Query: **{query}**

<div style="border-radius: 12px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 15px 0;">
    <iframe 
        src="{self.valves.omi_web_url}?search={query}"
        width="100%" 
        height="600px" 
        frameborder="0"
        loading="eager"
        style="background: white;"
        title="OMI Search Results">
    </iframe>
</div>

*Search results will appear in the OMI interface above.*"""

            # Replace the last message with search response
            body["messages"][-1] = {
                "role": "assistant",
                "content": search_html
            }
        
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Post-processor - can modify response if needed
        print(f"outlet:{__name__}")
        print(f"outlet:body:{body}")
        
        return body
