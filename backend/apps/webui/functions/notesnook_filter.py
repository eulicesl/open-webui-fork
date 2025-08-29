"""
Notesnook Smart Note Detection Filter
Automatically detects and extracts notes from conversations
"""

async def handler(body, __user__=None, __event_emitter__=None):
    """
    Filter function that detects note-worthy content and adds note-taking capabilities
    """
    import json
    import re
    from datetime import datetime
    
    # Configuration
    NOTE_INDICATORS = [
        "important", "remember", "note", "save this", "keep in mind",
        "don't forget", "for reference", "key point", "action item",
        "todo", "task", "remind me", "meeting notes", "summary"
    ]
    
    # Check if we have messages
    if "messages" not in body:
        return body
        
    messages = body.get("messages", [])
    if not messages:
        return body
        
    # Process the conversation for note-worthy content
    last_message = messages[-1]
    
    # For user messages - detect note intent
    if last_message.get("role") == "user":
        content = last_message.get("content", "").lower()
        
        # Check for explicit note commands
        if content.startswith("!note") or content.startswith("/note"):
            # This is a note command, add context
            body["__note_command"] = True
            
        # Check for implicit note indicators
        note_score = 0
        detected_indicators = []
        
        for indicator in NOTE_INDICATORS:
            if indicator in content:
                note_score += 1
                detected_indicators.append(indicator)
                
        if note_score >= 2 or any(strong in content for strong in ["save this", "remember", "important note"]):
            # High probability this should be saved as a note
            body["__auto_note"] = {
                "confidence": min(note_score * 0.3, 1.0),
                "indicators": detected_indicators,
                "timestamp": datetime.now().isoformat()
            }
            
    # For assistant responses - enhance with note-taking features
    elif last_message.get("role") == "assistant":
        content = last_message.get("content", "")
        
        # Check if previous message requested note-taking
        if body.get("__auto_note") and body["__auto_note"]["confidence"] > 0.6:
            # Add note-saving UI elements
            note_ui = """

---
📝 **Note Detection:** This seems important. Would you like to:
- 💾 Save as a note
- 📌 Pin to favorites
- 🏷️ Add tags
- 📚 Add to notebook

*Use `/note save` to save this conversation*"""
            
            last_message["content"] = content + note_ui
            
        # Extract action items automatically
        action_items = extract_action_items(content)
        if action_items:
            action_summary = "\n\n✅ **Detected Action Items:**\n"
            for item in action_items:
                action_summary += f"- {item}\n"
            action_summary += "\n*Use `/note todo` to save these as tasks*"
            
            last_message["content"] = content + action_summary
            
        # Extract key points for automatic summarization
        if len(content) > 1000:
            key_points = extract_key_points(content)
            if key_points:
                body["__note_summary"] = {
                    "key_points": key_points,
                    "word_count": len(content.split()),
                    "suggested_title": generate_title(content)
                }
                
    return body


def extract_action_items(text):
    """Extract potential action items from text"""
    action_patterns = [
        r"(?:you should|you need to|you must|please|make sure to|don't forget to)\s+([^.!?]+)",
        r"(?:TODO|Action|Task):\s*([^.!?\n]+)",
        r"(?:\d+\.|\-|\*)\s*(?:You should|Need to|Must)\s+([^.!?\n]+)"
    ]
    
    action_items = []
    for pattern in action_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        action_items.extend(matches)
        
    # Clean and deduplicate
    cleaned_items = []
    for item in action_items:
        cleaned = item.strip().capitalize()
        if cleaned and cleaned not in cleaned_items and len(cleaned) > 10:
            cleaned_items.append(cleaned)
            
    return cleaned_items[:5]  # Return top 5 action items


def extract_key_points(text):
    """Extract key points from long text"""
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    
    # Keywords that indicate important points
    importance_keywords = [
        "important", "key", "critical", "essential", "must", "significant",
        "main", "primary", "fundamental", "crucial", "remember", "note"
    ]
    
    key_points = []
    for sentence in sentences:
        sentence = sentence.strip()
        if any(keyword in sentence.lower() for keyword in importance_keywords):
            if len(sentence) > 20 and len(sentence) < 200:
                key_points.append(sentence)
                
    return key_points[:5]  # Return top 5 key points


def generate_title(text):
    """Generate a title from text content"""
    # Try to find a heading
    lines = text.split('\n')
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        if line and not line.startswith('-') and len(line) < 100:
            # Remove markdown formatting
            title = re.sub(r'[#*`]', '', line).strip()
            if title:
                return title
                
    # Fallback: use first sentence
    first_sentence = re.split(r'[.!?]', text)[0].strip()
    if first_sentence and len(first_sentence) < 100:
        return first_sentence
        
    # Final fallback
    return f"Note from {datetime.now().strftime('%B %d, %Y')}"