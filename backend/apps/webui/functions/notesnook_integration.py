"""
title: Notesnook Pro Integration
author: MindX Team
description: Complete Notesnook with all Pro features - seamlessly embedded
version: 2.0.0
"""

import re
from typing import Optional

def handler(body: dict, __user__: Optional[dict] = None):
    """Handle Notesnook integration requests"""
    
    # Get the last message
    messages = body.get("messages", [])
    if not messages:
        return body
    
    last_message = messages[-1].get("content", "").lower()
    
    # Trigger phrases for opening notes
    trigger_phrases = [
        "open notes", "show notes", "take notes", "note this",
        "save note", "create note", "my notes", "notesnook", "/notes"
    ]
    
    # Check if user wants to open notes
    if any(phrase in last_message for phrase in trigger_phrases):
        # Extract any content to pre-fill
        content_to_save = ""
        if "note this:" in last_message:
            content_to_save = last_message.split("note this:", 1)[1].strip()
        elif "save note:" in last_message:
            content_to_save = last_message.split("save note:", 1)[1].strip()
        
        # Determine URL based on environment
        notesnook_url = "http://localhost:3001"
        # Check if we're in HTTPS environment
        if "https://" in body.get("base_url", ""):
            notesnook_url = "https://eulicess-mac-studio.tail8e6b76.ts.net/notesnook"
        
        # Create the notes interface
        notes_html = f'''
        <div style="border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); margin: 10px 0;">
            <div style="background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%); color: white; padding: 12px 20px; font-weight: 600;">
                📝 Notesnook Professional - All Pro Features Unlocked
                <span style="float: right; font-size: 12px; opacity: 0.8;">Self-Hosted • E2E Encrypted • Mobile Sync</span>
            </div>
            <iframe 
                src="{notesnook_url}{f'?content={content_to_save}' if content_to_save else ''}"
                width="100%" 
                height="650px" 
                frameborder="0"
                loading="lazy"
                style="background: white;"
                title="Notesnook Notes"
                allow="clipboard-write; clipboard-read">
            </iframe>
            <div style="background: #f8f9fa; padding: 8px 20px; font-size: 12px; color: #666; border-top: 1px solid #eee;">
                💡 <strong>Pro Features Active:</strong> Tables, Code Blocks, Math, Attachments, Tags, Notebooks, Encryption
            </div>
        </div>
        
        <div style="margin-top: 15px; padding: 15px; background: #f0f7ff; border-left: 4px solid #7c3aed; border-radius: 0 8px 8px 0;">
            <h4 style="margin: 0 0 10px 0; color: #334155;">🎯 Quick Commands</h4>
            <p style="margin: 5px 0; font-size: 14px;">
                • <code>open notes</code> - Open Notesnook editor<br>
                • <code>note this: [content]</code> - Create pre-filled note<br>
                • <code>save this conversation</code> - Save chat as note<br>
                • Mobile sync: Set server to <code>http://your-ip:3002</code>
            </p>
        </div>
        '''
        
        return {
            "role": "assistant",
            "content": notes_html
        }
    
    # Handle chat-to-note conversion requests
    if "save this conversation" in last_message or "save conversation" in last_message:
        # Get recent conversation context
        conversation_text = ""
        for msg in messages[-10:]:  # Last 10 messages
            role = msg.get("role", "")
            content = msg.get("content", "")[:500]  # Truncate long messages
            if role in ["user", "assistant"] and content:
                # Clean HTML from content
                import re
                clean_content = re.sub(r'<[^>]+>', '', content)
                conversation_text += f"**{role.title()}:** {clean_content}\n\n"
        
        # URL encode the conversation
        import urllib.parse
        encoded_content = urllib.parse.quote(conversation_text[:1000])
        
        notesnook_url = "http://localhost:3001"
        if "https://" in body.get("base_url", ""):
            notesnook_url = "https://eulicess-mac-studio.tail8e6b76.ts.net/notesnook"
        
        save_html = f'''
        <div style="border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); margin: 10px 0;">
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 12px 20px; font-weight: 600;">
                💾 Conversation Saved to Notesnook
            </div>
            <iframe 
                src="{notesnook_url}?title=Chat%20Summary&content={encoded_content}"
                width="100%" 
                height="500px" 
                frameborder="0"
                loading="eager"
                style="background: white;"
                title="Save Chat as Note">
            </iframe>
            <div style="background: #f0fff4; padding: 10px 20px; font-size: 13px; color: #065f46;">
                ✅ Conversation saved! Edit and organize in Notesnook above.
            </div>
        </div>
        '''
        
        return {
            "role": "assistant", 
            "content": save_html
        }
    
    return body
