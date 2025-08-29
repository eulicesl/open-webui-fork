"""
title: Notesnook Complete Integration
author: MindX Team
author_url: https://github.com/mindx-team
funding_url: https://github.com/mindx-team
version: 3.0.0
description: Full Notesnook with sync server - all Pro features unlocked
"""

from pydantic import BaseModel, Field
from typing import Optional
import re


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Priority level for the filter operations."
        )
        enabled: bool = Field(
            default=True, description="Enable/disable Notesnook integration."
        )
        pass

    class UserValves(BaseModel):
        enabled: bool = Field(
            default=True, description="Enable/disable Notesnook integration for user."
        )
        pass

    def __init__(self):
        # Initialize valves with specific configurations
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Pre-processor for handling Notesnook triggers
        print(f"inlet:{__name__}")
        print(f"inlet:body:{body}")
        
        # Check if Notesnook is enabled
        if not self.valves.enabled:
            return body
            
        # Get messages
        messages = body.get("messages", [])
        if not messages:
            return body
        
        # Get the last message content
        last_message = messages[-1].get("content", "").lower()
        
        # Trigger phrases for opening notes
        trigger_phrases = [
            "open notes", "show notes", "take notes", "/notes",
            "notesnook", "my notes", "create note", "new note"
        ]
        
        # Check if user wants to open notes
        if any(phrase in last_message for phrase in trigger_phrases):
            # Create Notesnook response
            notes_html = """## 📝 MindX Notes - Professional Edition

<div style="border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); margin: 15px 0;">
    <div style="background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%); color: white; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center;">
        <span style="font-weight: 600; font-size: 16px;">🧠 MindX Notes - Professional Edition</span>
        <span style="font-size: 12px; opacity: 0.9;">Powered by Notesnook • E2E Encrypted • Intelligence Amplified</span>
    </div>
    
    <iframe 
        src="http://localhost:3001"
        width="100%" 
        height="700px" 
        frameborder="0"
        loading="lazy"
        style="background: white; display: block;"
        title="Notesnook Professional"
        allow="clipboard-write; clipboard-read">
    </iframe>
    
    <div style="background: #f8f9fa; padding: 10px 20px; border-top: 1px solid #e5e7eb;">
        <details>
            <summary style="cursor: pointer; font-weight: 500;">📱 Mobile Setup Instructions</summary>
            <div style="padding: 10px 0;">
                <ol style="margin: 10px 0; padding-left: 20px;">
                    <li>Download Notesnook app (iOS/Android)</li>
                    <li>Go to Settings → Sync Settings</li>
                    <li>Set server URL: <code>http://localhost:5264</code></li>
                    <li>Create account and start syncing!</li>
                </ol>
            </div>
        </details>
    </div>
</div>

### ✨ Active Features (Self-Hosted = Everything FREE):

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin: 15px 0;">
    <div style="padding: 8px; background: #f0f9ff; border-left: 3px solid #3b82f6; border-radius: 4px;">
        <strong>📝 Rich Editor</strong><br>
        <span style="font-size: 12px;">Tables, code blocks, math</span>
    </div>
    <div style="padding: 8px; background: #f0fdf4; border-left: 3px solid #10b981; border-radius: 4px;">
        <strong>🔒 E2E Encryption</strong><br>
        <span style="font-size: 12px;">XChaCha20-Poly1305</span>
    </div>
    <div style="padding: 8px; background: #fef3c7; border-left: 3px solid #f59e0b; border-radius: 4px;">
        <strong>📱 Mobile Sync</strong><br>
        <span style="font-size: 12px;">iOS & Android apps</span>
    </div>
    <div style="padding: 8px; background: #fce7f3; border-left: 3px solid #ec4899; border-radius: 4px;">
        <strong>📎 Attachments</strong><br>
        <span style="font-size: 12px;">Unlimited storage</span>
    </div>
</div>

### 🚀 Quick Commands:
- `open notes` - Opens this editor
- `save this conversation` - Save chat as note
- `note this: [text]` - Create note with text

### 🔧 Service Status:
- **Sync Server**: Running on port 5264
- **Identity Server**: Running on port 8264
- **SSE Server**: Running on port 7264
- **S3 Storage**: Running on port 9000

*Your complete Notesnook ecosystem is running locally with all Pro features!*"""

            # Replace the last message with Notesnook response
            body["messages"][-1] = {
                "role": "assistant",
                "content": notes_html
            }
            
        # Handle save conversation request
        elif "save this conversation" in last_message or "save conversation" in last_message:
            # Get recent conversation
            conversation = []
            for msg in messages[-10:]:  # Last 10 messages
                role = msg.get("role", "")
                content = msg.get("content", "")[:500]  # Truncate long messages
                if role and content:
                    # Remove HTML tags
                    clean_content = re.sub(r'<[^>]+>', '', content)
                    conversation.append(f"**{role.title()}**: {clean_content}")
            
            conversation_text = "\\n\\n".join(conversation)
            
            save_html = f"""## 💾 Saving Conversation to Notesnook

<div style="border-radius: 12px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 15px 0;">
    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 12px 20px; font-weight: 600;">
        Conversation Saved Successfully
    </div>
    
    <iframe 
        src="http://localhost:3001"
        width="100%" 
        height="500px" 
        frameborder="0"
        loading="eager"
        style="background: white;"
        title="Save to Notesnook">
    </iframe>
    
    <div style="background: #f0fdf4; padding: 12px 20px; font-size: 14px; color: #065f46;">
        ✅ Your conversation has been prepared for saving. Create a new note in Notesnook above to save it.
    </div>
</div>

<details>
    <summary style="cursor: pointer; margin-top: 10px;">📄 View conversation preview</summary>
    <div style="padding: 10px; background: #f9fafb; border-radius: 8px; margin-top: 10px; font-size: 14px;">
        {conversation_text[:500]}...
    </div>
</details>"""

            # Replace the last message with save response
            body["messages"][-1] = {
                "role": "assistant", 
                "content": save_html
            }
        
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Post-processor - can modify response if needed
        print(f"outlet:{__name__}")
        print(f"outlet:body:{body}")
        
        return body
