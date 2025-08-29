"""
title: Data Visualization
author: open-webui
description: Create charts from conversation data
version: 1.0.0
"""

import json
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional

class Filter:
    def __init__(self):
        self.valves = self.Valves()
        
    class Valves:
        enabled: bool = True
        chart_height: int = 400
        chart_width: int = 600
        
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Check for visualization requests"""
        
        if not self.valves.enabled:
            return body
            
        messages = body.get("messages", [])
        if not messages:
            return body
            
        last_msg = messages[-1].get("content", "").lower()
        
        # Check for chart triggers
        if any(trigger in last_msg for trigger in ["create chart", "visualize", "plot", "graph"]):
            # Extract data from context
            chart_html = self.create_chart(messages)
            
            if chart_html:
                messages.append({
                    "role": "assistant",
                    "content": chart_html
                })
                
        return body
        
    def create_chart(self, messages) -> str:
        """Create a chart from conversation data"""
        
        # This is a simple example - would need data extraction logic
        fig = go.Figure(data=[
            go.Bar(x=['Category A', 'Category B', 'Category C'], 
                   y=[10, 15, 7])
        ])
        
        fig.update_layout(
            title="Data Visualization",
            height=self.valves.chart_height,
            width=self.valves.chart_width
        )
        
        # Convert to HTML
        chart_html = f"""
        <div style="width: 100%; padding: 20px;">
            {fig.to_html(include_plotlyjs='cdn', div_id="chart")}
        </div>
        """
        
        return chart_html
        
    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
