"""
title: Adaptive Memory System
author: open-webui
description: Dynamic memory that learns from conversations
version: 1.0.0
"""

import json
import hashlib
from datetime import datetime
from typing import Optional

class Filter:
    def __init__(self):
        self.valves = self.Valves()
        self.memory = {}
        self.load_memory()
        
    class Valves:
        enabled: bool = True
        max_memories: int = 100
        memory_file: str = "adaptive_memory.json"
        
    def load_memory(self):
        """Load memory from storage"""
        try:
            with open(self.valves.memory_file, 'r') as f:
                self.memory = json.load(f)
        except:
            self.memory = {}
            
    def save_memory(self):
        """Save memory to storage"""
        try:
            with open(self.valves.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except:
            pass
            
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Add relevant memories to context"""
        
        if not self.valves.enabled:
            return body
            
        messages = body.get("messages", [])
        if not messages:
            return body
            
        user_id = __user__.get("id", "default") if __user__ else "default"
        user_memory = self.memory.get(user_id, {})
        
        # Add relevant memories to context
        if user_memory:
            memory_context = "\n**Your memories:**\n"
            for key, value in list(user_memory.items())[:5]:  # Last 5 memories
                memory_context += f"- {key}: {value}\n"
                
            # Add as system message
            messages.insert(0, {
                "role": "system",
                "content": memory_context
            })
            
        return body
        
    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Extract and store new memories"""
        
        if not self.valves.enabled:
            return body
            
        messages = body.get("messages", [])
        if not messages:
            return body
            
        user_id = __user__.get("id", "default") if __user__ else "default"
        
        # Extract information from conversation
        for msg in messages[-5:]:  # Last 5 messages
            if msg.get("role") == "user":
                content = msg.get("content", "")
                
                # Simple memory extraction (would be more sophisticated)
                if "my name is" in content.lower():
                    name = content.split("my name is", 1)[-1].split()[0]
                    if user_id not in self.memory:
                        self.memory[user_id] = {}
                    self.memory[user_id]["name"] = name
                    self.save_memory()
                    
        return body
