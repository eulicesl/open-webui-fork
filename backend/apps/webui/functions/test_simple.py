"""
title: Test Function
author: MindX
version: 1.0.0
"""

class Filter:
    def __init__(self):
        pass

    async def inlet(self, body: dict, __user__ = None) -> dict:
        messages = body.get("messages", [])
        if messages and "test" in messages[-1].get("content", "").lower():
            messages.append({
                "role": "assistant",
                "content": "✅ Test function is working!"
            })
        return body

    async def outlet(self, body: dict, __user__ = None) -> dict:
        return body