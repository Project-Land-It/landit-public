#!/usr/bin/env python3
"""
Enhanced Discord Logger - With Taiga Avatar Integration
Posts agent messages to Discord with custom avatars from Taiga user profiles
"""

import os
import sys
import json
from datetime import datetime

# Optional asyncpg for database updates
try:
    import asyncio
    import asyncpg
    HAS_ASYNCPG = True
except ImportError:
    HAS_ASYNCPG = False

# Try to import requests, fall back to urllib if not available
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    HAS_REQUESTS = False

# Agent metadata (emoji and color codes)
AGENT_METADATA = {
    'riley': {'emoji': '🔮', 'color': 0x4B0082},
    'charlie': {'emoji': '🔵', 'color': 0x0000FF},
    'frankie': {'emoji': '🟢', 'color': 0x00FF00},
    'andy': {'emoji': '🟠', 'color': 0xFF8C00},
    'tessa': {'emoji': '🟡', 'color': 0xFFD700},
    'dexter': {'emoji': '🟣', 'color': 0x800080},
    'sammy': {'emoji': '🛡️', 'color': 0xC0C0C0},
    'max': {'emoji': '🔴', 'color': 0xFF0000},
    'alex': {'emoji': '🩵', 'color': 0x00FFFF},
    'sage': {'emoji': '🩷', 'color': 0xFF00FF},
    'finn': {'emoji': '💛', 'color': 0xFFFF00},
    'lex': {'emoji': '⚪', 'color': 0x808080},
    'scribbles': {'emoji': '📜', 'color': 0x8B4513},
    'claude': {'emoji': '🤖', 'color': 0x000000},
}

# Taiga configuration
TAIGA_URL = os.getenv('TAIGA_API_URL', 'http://192.168.1.13:8080/api/v1')
TAIGA_EXTERNAL_URL = os.getenv('TAIGA_EXTERNAL_URL', 'https://taiga.landit4.fun')
TAIGA_INTERNAL_HOST = os.getenv('TAIGA_INTERNAL_HOST', '192.168.1.13:8080')
TAIGA_USERNAME = os.getenv('TAIGA_USERNAME', '')
TAIGA_PASSWORD = os.getenv('TAIGA_PASSWORD', '')

# Database configuration
DB_HOST = os.getenv('DB_HOST', '192.168.1.11')
DB_PORT = int(os.getenv('DB_PORT', '5432'))
DB_NAME = os.getenv('DB_NAME', 'landit_sit_db')
DB_USER = os.getenv('DB_USER', 'landit')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

# Avatar cache (to avoid repeated API calls)
_avatar_cache = {}


def get_taiga_auth_token():
    """Authenticate with Taiga and return auth token."""
    if not TAIGA_USERNAME or not TAIGA_PASSWORD:
        return None
    
    try:
        if not HAS_REQUESTS:
            return None
        
        response = requests.post(
            f"{TAIGA_URL}/auth",
            json={
                "username": TAIGA_USERNAME,
                "password": TAIGA_PASSWORD,
                "type": "normal"
            },
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json().get('auth_token')
    except Exception:
        pass
    
    return None


def get_taiga_user_avatar(agent_name):
    """
    Fetch user avatar from Taiga API by searching for username matching agent name.
    Returns the avatar URL or None if not found.
    """
    # Check cache first
    if agent_name.lower() in _avatar_cache:
        return _avatar_cache[agent_name.lower()]
    
    if not HAS_REQUESTS:
        return None
    
    # Get auth token
    token = get_taiga_auth_token()
    if not token:
        return None
    
    try:
        # Search for user by username (case-insensitive match)
        response = requests.get(
            f"{TAIGA_URL}/users",
            headers={"Authorization": f"Bearer {token}"},
            params={"project": 1},  # land-it project ID
            timeout=5
        )
        
        if response.status_code != 200:
            return None
        
        users = response.json()
        
        # Find user matching agent name
        for user in users:
            username = user.get('username', '').lower()
            full_name = user.get('full_name', '').lower()
            agent_name_lower = agent_name.lower()
            
            # Match by username or full name
            if username == agent_name_lower or full_name == agent_name_lower:
                avatar_url = user.get('photo') or user.get('big_photo')
                
                if avatar_url:
                    # Convert internal URLs to external
                    avatar_url = convert_to_external_url(avatar_url)
                    
                    # Cache the result
                    _avatar_cache[agent_name.lower()] = avatar_url
                    return avatar_url
    
    except Exception as e:
        print(f"⚠️  Warning: Failed to fetch Taiga avatar for {agent_name}: {e}", file=sys.stderr)
    
    # Cache negative result to avoid repeated failures
    _avatar_cache[agent_name.lower()] = None
    return None


def convert_to_external_url(url):
    """
    Convert internal Taiga URLs to external ones.
    Examples:
      - http://192.168.1.13:8080/media/... -> https://taiga.landit4.fun/media/...
      - //192.168.1.13:8080/media/... -> https://taiga.landit4.fun/media/...
      - /media/... -> https://taiga.landit4.fun/media/...
    """
    if not url:
        return None
    
    # Handle protocol-relative URLs
    if url.startswith('//'):
        url = 'https:' + url
    
    # Handle absolute paths
    if url.startswith('/'):
        return f"{TAIGA_EXTERNAL_URL}{url}"
    
    # Replace internal host with external URL
    if TAIGA_INTERNAL_HOST in url:
        # Remove protocol if present
        if url.startswith('http://') or url.startswith('https://'):
            url = url.split('://', 1)[1]
        
        # Replace internal host with external URL
        url = url.replace(TAIGA_INTERNAL_HOST, TAIGA_EXTERNAL_URL.replace('https://', '').replace('http://', ''))
        
        # Ensure https protocol
        if not url.startswith('http'):
            url = 'https://' + url
    
    return url


async def update_agent_state_db(agent_name: str, status: str, task_description: str = None):
    """Update agent state in PostgreSQL database (optional)"""
    if not HAS_ASYNCPG or not DB_PASSWORD:
        return  # Skip if asyncpg not available or no DB password
    
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            timeout=5
        )
        
        # Map status emoji to database status
        status_map = {
            '✅': 'IDLE',
            '🔄': 'WORKING',
            '⚠️': 'BLOCKED',
            '❌': 'IDLE',
        }
        db_status = status_map.get(status, 'WORKING')
        
        await conn.execute("""
            UPDATE discord_agent_state
            SET current_status = $1,
                current_task_description = $2,
                last_activity_at = NOW()
            WHERE agent_name = $3
        """, db_status, task_description, agent_name.lower())
        
        await conn.close()
        
    except Exception:
        pass  # Silently fail


def post_to_discord(agent_name, task, status, message):
    """Post message to Discord webhook with Taiga avatar"""
    webhook_url = os.getenv('DISCORD_AGENT_WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ Error: DISCORD_AGENT_WEBHOOK_URL not set", file=sys.stderr)
        return False
    
    agent_name_lower = agent_name.lower()
    metadata = AGENT_METADATA.get(agent_name_lower, {'emoji': '❓', 'color': 0x808080})
    
    emoji = metadata['emoji']
    color = metadata['color']
    
    # Try to get Taiga avatar
    avatar_url = get_taiga_user_avatar(agent_name)
    
    # Split long messages into multiple fields
    max_field_length = 1024
    message_parts = []
    
    if len(message) <= max_field_length:
        message_parts = [message]
    else:
        while message:
            message_parts.append(message[:max_field_length])
            message = message[max_field_length:]
    
    fields = []
    for i, part in enumerate(message_parts):
        field_name = "Message" if i == 0 else f"Message (continued {i})"
        fields.append({"name": field_name, "value": part, "inline": False})
    
    embed = {
        "title": f"{emoji} {agent_name}",
        "description": f"**Task**: {task}\n**Status**: {status}",
        "color": color,
        "fields": fields,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Build payload with optional avatar and username override
    payload = {
        "embeds": [embed]
    }
    
    # Add custom username and avatar if Taiga avatar found
    if avatar_url:
        payload["username"] = f"{emoji} {agent_name}"
        payload["avatar_url"] = avatar_url
        print(f"ℹ️  Using Taiga avatar: {avatar_url}", file=sys.stderr)
    else:
        print(f"ℹ️  No Taiga avatar found for {agent_name}, using default webhook avatar", file=sys.stderr)
    
    try:
        if HAS_REQUESTS:
            response = requests.post(webhook_url, json=payload, timeout=10)
            success = response.status_code in [200, 204]
        else:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                success = response.status in [200, 204]
        
        if success:
            print(f"✅ Posted to Discord: {agent_name} - {task}")
            return True
        else:
            print(f"❌ Failed to post to Discord", file=sys.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error posting to Discord: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 5:
        print("Usage: python3 discord_logger_with_taiga_avatars.py <agent_name> <task> <status> <message>")
        print("Example: python3 discord_logger_with_taiga_avatars.py Charlie 'Build API' '🔄' 'Working on it...'")
        print()
        print("Required environment variables:")
        print("  DISCORD_AGENT_WEBHOOK_URL - Discord webhook URL")
        print()
        print("Optional environment variables for Taiga avatars:")
        print("  TAIGA_USERNAME - Taiga username for authentication")
        print("  TAIGA_PASSWORD - Taiga password for authentication")
        print("  TAIGA_API_URL - Taiga API URL (default: http://192.168.1.13:8080/api/v1)")
        print("  TAIGA_EXTERNAL_URL - External Taiga URL (default: https://taiga.landit4.fun)")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    task = sys.argv[2]
    status = sys.argv[3]
    message = sys.argv[4]
    
    # Update database state (if asyncpg available)
    if HAS_ASYNCPG:
        asyncio.run(update_agent_state_db(agent_name, status, task))
    
    # Post to Discord
    success = post_to_discord(agent_name, task, status, message)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
