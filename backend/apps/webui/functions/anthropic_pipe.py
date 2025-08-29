"""
title: Anthropic Claude Pipe
author: open-webui
description: Use Anthropic Claude models in Open WebUI
version: 2.0.0
"""

from typing import List, Dict, Optional
import requests
import json

class Pipeline:
    def __init__(self):
        self.name = "Anthropic Claude"
        self.api_key = None  # Set via valves
        
    class Valves:
        ANTHROPIC_API_KEY: str = ""
        MODEL: str = "claude-3-5-sonnet-20241022"
        
    async def pipe(
        self, 
        user_message: str, 
        model_id: str, 
        messages: List[Dict], 
        body: Dict
    ) -> str:
        """Process messages through Anthropic API"""
        
        if not self.valves.ANTHROPIC_API_KEY:
            return "Please set your Anthropic API key in settings"
            
        headers = {
            "x-api-key": self.valves.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        # Convert messages to Anthropic format
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": "user" if msg["role"] == "user" else "assistant",
                "content": msg["content"]
            })
            
        payload = {
            "model": self.valves.MODEL,
            "messages": anthropic_messages,
            "max_tokens": 4096,
            "temperature": body.get("temperature", 0.7)
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()["content"][0]["text"]
        else:
            return f"Error: {response.status_code} - {response.text}"
