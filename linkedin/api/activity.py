import logging

logger = logging.getLogger(__name__)

def parse_activity_response(data: dict) -> list[dict]:
    """
    Parse Voyager profileUpdatesV2 response and return last 3 posts.
    
    Args:
        data: Raw JSON from Voyager API (with "included")
        
    Returns:
        List of dicts with 'text' and 'timestamp'
    """
    posts = []
    included = data.get("included", [])
    
    for entity in included:
        # Voyager activity updates usually have a $type related to Update or UpdateV2
        # profileUpdatesV2 often uses ProfileUpdate entities.
        if entity.get("$type") == "com.linkedin.voyager.dash.identity.profile.ProfileUpdate":
            # Extract text and timestamp
            # The structure below is based on typical Voyager dash profile updates
            value_dict = entity.get("value", {})
            update_value = value_dict.get("com.linkedin.voyager.dash.identity.profile.ProfileUpdateValue", {})
            
            # Text is often nested in a 'text' object
            text_obj = update_value.get("text", {})
            text = text_obj.get("text")
            
            # Timestamp is usually a Unix epoch in milliseconds
            timestamp = entity.get("createdTime")
            
            if text:
                posts.append({
                    "text": text,
                    "timestamp": timestamp
                })
        
        # Another common pattern for shares/posts in Voyager
        elif entity.get("$type") == "com.linkedin.voyager.dash.feed.Update":
            # Similar extraction for feed-style updates if present in profileUpdates
            pass

    # Sort by timestamp descending (newest first)
    posts.sort(key=lambda x: x.get("timestamp") or 0, reverse=True)
    
    # Return top 3 unique posts
    seen_texts = set()
    unique_posts = []
    for p in posts:
        if p["text"] not in seen_texts:
            unique_posts.append(p)
            seen_texts.add(p["text"])
        if len(unique_posts) >= 3:
            break
            
    return unique_posts
