"""
title: Thinking Claude
author: open-webui
description: Enhanced reasoning with thinking process
version: 1.0.0
"""

from typing import Optional

class Filter:
    def __init__(self):
        self.valves = self.Valves()
        
    class Valves:
        show_thinking: bool = True
        thinking_label: str = "🤔 Thinking..."
        enabled: bool = True
        
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Add thinking instructions to prompts"""
        
        if not self.valves.enabled:
            return body
            
        messages = body.get("messages", [])
        if not messages:
            return body
            
        # Add thinking instructions to system prompt
        thinking_prompt = """
        Before answering, think step-by-step about the problem.
        Show your reasoning process in a <thinking> section.
        Then provide your final answer in an <answer> section.
        """
        
        # Check if system message exists
        has_system = False
        for msg in messages:
            if msg.get("role") == "system":
                msg["content"] += "\n\n" + thinking_prompt
                has_system = True
                break
                
        if not has_system:
            messages.insert(0, {
                "role": "system",
                "content": thinking_prompt
            })
            
        return body
        
    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Format thinking output"""
        
        if not self.valves.enabled:
            return body
            
        messages = body.get("messages", [])
        if not messages:
            return body
            
        # Process last assistant message
        last_msg = messages[-1]
        if last_msg.get("role") == "assistant":
            content = last_msg.get("content", "")
            
            # Format thinking sections
            if "<thinking>" in content and "</thinking>" in content:
                thinking_start = content.index("<thinking>")
                thinking_end = content.index("</thinking>") + len("</thinking>")
                thinking_content = content[thinking_start:thinking_end]
                
                # Replace with formatted version
                formatted_thinking = f"""
<details>
<summary>{self.valves.thinking_label}</summary>
<div style="padding: 10px; background: #f0f0f0; border-radius: 5px; margin: 10px 0;">
{thinking_content.replace("<thinking>", "").replace("</thinking>", "")}
</div>
</details>
"""
                
                content = content[:thinking_start] + formatted_thinking + content[thinking_end:]
                last_msg["content"] = content
                
        return body
