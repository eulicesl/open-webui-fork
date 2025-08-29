"""
MindX Chat Function
Add this through OpenWebUI's Function interface
Go to: Settings → Functions → Create New Function
"""

async def handler(body, __user__={}):
    """
    MindX Chat Enhancement Function
    Adds branding and smart features to responses
    """
    
    # MindX branding
    mindx_signature = "\n\n---\n*Powered by MindX Technology - Intelligence Amplified*"
    
    # Get the messages
    messages = body.get("messages", [])
    if not messages:
        return body
        
    last_message = messages[-1]
    
    # Check for MindX queries in user messages
    if last_message.get("role") == "user":
        content = last_message.get("content", "").lower()
        
        # Handle MindX info requests
        if "mindx" in content and any(word in content for word in ["info", "about", "what is", "tell me"]):
            return {
                "messages": [{
                    "role": "assistant",
                    "content": """# Welcome to MindX Chat! 🚀

**Intelligence Amplified**

I'm MindX, your advanced AI assistant designed to help with:
- 🧠 Complex analysis and problem-solving
- 💻 Code generation and debugging
- ✍️ Creative writing and content creation
- 📊 Data analysis and insights
- 🎯 Strategic planning and decision support
- 🔗 Integrated with n8n for workflow automation

Key Features:
• **Smart Context** - I remember our conversation context
• **Enhanced Analysis** - Deeper insights on complex topics  
• **Workflow Integration** - Connected to your automation tools
• **Custom Knowledge** - Access to your organization's data

Just ask me anything, and I'll apply my enhanced capabilities to help you succeed!

---
*Powered by MindX Technology - Intelligence Amplified*"""
                }]
            }
        
        # Handle capabilities request
        if "capabilities" in content or "what can you do" in content:
            return {
                "messages": [{
                    "role": "assistant",
                    "content": """## 🧠 MindX Capabilities

### Core Abilities:
- **Natural Language Understanding** - Context-aware conversations
- **Code Generation** - Multiple languages with best practices
- **Data Analysis** - Process CSV, JSON, SQL queries
- **Creative Content** - Stories, emails, documentation
- **Research Assistant** - Summarize papers, find sources

### Integrations:
- **n8n Workflows** - Trigger automations from chat
- **Document RAG** - Query your knowledge base
- **Web Search** - Real-time information retrieval
- **API Connections** - External service integration

### Smart Features:
- Context retention across conversations
- Multi-model routing for optimal responses
- Automatic prompt enhancement
- Response formatting and structuring

Ask me to help with any of these capabilities!

---
*Powered by MindX Technology*"""
                }]
            }
    
    # For assistant responses, add subtle enhancements
    if last_message.get("role") == "assistant":
        content = last_message.get("content", "")
        
        # Add signature to important/long responses
        keywords = ["recommend", "analysis", "solution", "conclusion", "summary", "steps", "guide"]
        if any(keyword in content.lower() for keyword in keywords) or len(content) > 1500:
            if mindx_signature not in content:
                content += mindx_signature
                
        # Add MindX insights for very long responses
        if len(content) > 2000 and "MindX" not in content:
            content += "\n\n💡 **MindX Insight:** This comprehensive analysis considers multiple perspectives. Focus on the key points most relevant to your needs."
            
        last_message["content"] = content
    
    return body