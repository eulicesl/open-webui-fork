"""
title: Live Web Search
author: open-webui
description: Search the web in real-time
version: 1.0.0
"""

from typing import Optional
import requests
from urllib.parse import quote

class Filter:
    def __init__(self):
        self.valves = self.Valves()
        
    class Valves:
        search_engine: str = "duckduckgo"  # Options: duckduckgo, google, searxng
        max_results: int = 5
        enabled: bool = True
        
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Process incoming messages for search triggers"""
        
        if not self.valves.enabled:
            return body
            
        messages = body.get("messages", [])
        if not messages:
            return body
            
        last_msg = messages[-1].get("content", "").lower()
        
        # Check for search triggers
        if any(trigger in last_msg for trigger in ["search:", "search for", "look up", "find online"]):
            # Extract search query
            query = last_msg.split("search", 1)[-1].strip(": ")
            
            # Perform search
            results = self.search_web(query)
            
            # Add search results to context
            search_context = f"\n\n**Web Search Results for '{query}':**\n"
            for i, result in enumerate(results[:self.valves.max_results], 1):
                search_context += f"{i}. {result['title']}\n   {result['snippet']}\n   URL: {result['url']}\n\n"
                
            messages[-1]["content"] += search_context
            
        return body
        
    def search_web(self, query: str) -> list:
        """Perform web search using configured engine"""
        
        if self.valves.search_engine == "duckduckgo":
            return self.search_duckduckgo(query)
        elif self.valves.search_engine == "google":
            return self.search_google(query)
        else:
            return []
            
    def search_duckduckgo(self, query: str) -> list:
        """Search using DuckDuckGo"""
        url = f"https://html.duckduckgo.com/html?q={quote(query)}"
        
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            # Parse HTML response (simplified)
            results = []
            # This would need proper HTML parsing
            return results
        except:
            return []
            
    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
