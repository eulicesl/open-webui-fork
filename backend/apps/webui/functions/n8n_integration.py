"""
title: N8N Workflow Integration
author: MindX Team
description: Trigger N8N workflows from chat
version: 1.0.0
"""

import requests
import json
from typing import Optional

class Filter:
    def __init__(self):
        self.valves = self.Valves()
        
    class Valves:
        n8n_webhook_url: str = "http://localhost:5678/webhook/"
        webhook_id: str = ""
        enabled: bool = True
        
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Send messages to N8N workflow"""
        
        if not self.valves.enabled or not self.valves.webhook_id:
            return body
            
        messages = body.get("messages", [])
        if not messages:
            return body
            
        last_msg = messages[-1]
        
        # Check for N8N triggers
        if "/n8n" in last_msg.get("content", "").lower():
            # Send to N8N
            webhook_url = f"{self.valves.n8n_webhook_url}{self.valves.webhook_id}"
            
            payload = {
                "message": last_msg.get("content", ""),
                "user": __user__.get("name", "unknown") if __user__ else "unknown",
                "timestamp": str(datetime.now()),
                "full_context": messages[-5:]  # Last 5 messages for context
            }
            
            try:
                response = requests.post(webhook_url, json=payload)
                if response.status_code == 200:
                    # Add N8N response to chat
                    n8n_response = response.json()
                    messages.append({
                        "role": "assistant",
                        "content": f"✅ N8N Workflow Response:\n{json.dumps(n8n_response, indent=2)}"
                    })
            except Exception as e:
                messages.append({
                    "role": "assistant",
                    "content": f"❌ N8N Error: {str(e)}"
                })
                
        return body
        
    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
