#!/usr/bin/env python3
"""
Discord Logger with GitHub-hosted Avatars
Posts agent messages to Discord with custom avatars from GitHub raw URLs.

This version uses publicly accessible GitHub raw URLs instead of Taiga avatars,
ensuring avatars always display correctly without authentication issues.
"""

import os
import sys
import json
from datetime import datetime

# Try to import requests, fall back to urllib if not available
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    HAS_REQUESTS = False

# GitHub raw URL base
GITHUB_AVATAR_BASE = "https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles"

# Agent metadata with GitHub avatar URLs
AGENT_METADATA = {
    'alex': {
        'emoji': '🩵',
        'color': 0x00FFFF,
        'avatar': f'{GITHUB_AVATAR_BASE}/alex.png',
        'role': 'Community & Support Orchestrator'
    },
    'andy': {
        'emoji': '🟠',
        'color': 0xFF8C00,
        'avatar': f'{GITHUB_AVATAR_BASE}/andy.png',
        'role': 'Android/Mobile Orchestrator'
    },
    'charlie': {
        'emoji': '🔵',
        'color': 0x0000FF,
        'avatar': f'{GITHUB_AVATAR_BASE}/charlie.png',
        'role': 'Backend Orchestrator'
    },
    'dexter': {
        'emoji': '🟣',
        'color': 0x800080,
        'avatar': f'{GITHUB_AVATAR_BASE}/dexter.png',
        'role': 'DevOps & Deployment Orchestrator'
    },
    'finn': {
        'emoji': '💛',
        'color': 0xFFFF00,
        'avatar': f'{GITHUB_AVATAR_BASE}/finn.png',
        'role': 'Finance & Monetization Orchestrator'
    },
    'frankie': {
        'emoji': '🟢',
        'color': 0x00FF00,
        'avatar': f'{GITHUB_AVATAR_BASE}/frankie.png',
        'role': 'Frontend Orchestrator'
    },
    'lex': {
        'emoji': '⚪',
        'color': 0x808080,
        'avatar': f'{GITHUB_AVATAR_BASE}/lex.png',
        'role': 'Legal & Compliance Orchestrator'
    },
    'max': {
        'emoji': '🔴',
        'color': 0xFF0000,
        'avatar': f'{GITHUB_AVATAR_BASE}/max_realistic.png',
        'role': 'Marketing & Growth Orchestrator'
    },
    'riley': {
        'emoji': '🔮',
        'color': 0x4B0082,
        'avatar': f'{GITHUB_AVATAR_BASE}/riley.png',
        'role': 'Research & Architecture Orchestrator'
    },
    'sage': {
        'emoji': '🩷',
        'color': 0xFF00FF,
        'avatar': f'{GITHUB_AVATAR_BASE}/sage.png',
        'role': 'Design & Brand Orchestrator'
    },
    'sammy': {
        'emoji': '🛡️',
        'color': 0xC0C0C0,
        'avatar': f'{GITHUB_AVATAR_BASE}/sammy.png',
        'role': 'Security Orchestrator'
    },
    'scribbles': {
        'emoji': '📜',
        'color': 0x8B4513,
        'avatar': f'{GITHUB_AVATAR_BASE}/scribbles_realistic.png',
        'role': 'Documentation Orchestrator'
    },
    'tessa': {
        'emoji': '🟡',
        'color': 0xFFD700,
        'avatar': f'{GITHUB_AVATAR_BASE}/tessa.png',
        'role': 'Testing & QA Orchestrator'
    },
    'claude': {
        'emoji': '🤖',
        'color': 0x000000,
        'avatar': None,  # Use default webhook avatar
        'role': 'AI Assistant'
    },
}


def get_agent_avatar(agent_name: str) -> str:
    """Get the GitHub avatar URL for an agent."""
    agent_lower = agent_name.lower()
    metadata = AGENT_METADATA.get(agent_lower, {})
    return metadata.get('avatar')


def post_to_discord(agent_name: str, task: str, status: str, message: str) -> bool:
    """Post message to Discord webhook with GitHub-hosted avatar."""
    webhook_url = os.getenv('DISCORD_AGENT_WEBHOOK_URL')
    
    if not webhook_url:
        print("Error: DISCORD_AGENT_WEBHOOK_URL not set", file=sys.stderr)
        return False
    
    agent_lower = agent_name.lower()
    metadata = AGENT_METADATA.get(agent_lower, {
        'emoji': '?',
        'color': 0x808080,
        'avatar': None,
        'role': 'Unknown Agent'
    })
    
    emoji = metadata.get('emoji', '?')
    color = metadata.get('color', 0x808080)
    avatar_url = metadata.get('avatar')
    
    # Split long messages into multiple fields (Discord limit: 1024 chars per field)
    max_field_length = 1024
    message_parts = []
    
    remaining = message
    while remaining:
        message_parts.append(remaining[:max_field_length])
        remaining = remaining[max_field_length:]
    
    fields = []
    for i, part in enumerate(message_parts):
        field_name = "Details" if i == 0 else f"Details (continued {i})"
        fields.append({"name": field_name, "value": part, "inline": False})
    
    embed = {
        "title": f"{emoji} {agent_name.capitalize()}",
        "description": f"**Task**: {task}\n**Status**: {status}",
        "color": color,
        "fields": fields,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Build payload
    payload = {
        "embeds": [embed]
    }
    
    # Add custom username and avatar
    payload["username"] = f"{emoji} {agent_name.capitalize()}"
    if avatar_url:
        payload["avatar_url"] = avatar_url
    
    try:
        if HAS_REQUESTS:
            response = requests.post(webhook_url, json=payload, timeout=10)
            success = response.status_code in [200, 204]
            if not success:
                print(f"Discord API error: {response.status_code} - {response.text}", file=sys.stderr)
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
            print(f"Posted to Discord: {agent_name} - {task}")
            return True
        else:
            print(f"Failed to post to Discord", file=sys.stderr)
            return False
            
    except Exception as e:
        print(f"Error posting to Discord: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 5:
        print("Discord Logger with GitHub Avatars")
        print()
        print("Usage: python3 discord_logger_github_avatars.py <agent_name> <task> <status> <message>")
        print()
        print("Arguments:")
        print("  agent_name  - Name of the agent (alex, andy, charlie, dexter, etc.)")
        print("  task        - Brief task description")
        print("  status      - Status emoji (e.g., '✅' '🔄' '⚠️' '❌')")
        print("  message     - Detailed message content")
        print()
        print("Environment Variables:")
        print("  DISCORD_AGENT_WEBHOOK_URL - Discord webhook URL (required)")
        print()
        print("Example:")
        print("  python3 discord_logger_github_avatars.py Dexter 'Deploy frontend' '✅' 'Deployment complete!'")
        print()
        print("Available agents:")
        for name, meta in sorted(AGENT_METADATA.items()):
            if name != 'claude':
                print(f"  {meta['emoji']} {name.capitalize():12} - {meta['role']}")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    task = sys.argv[2]
    status = sys.argv[3]
    message = sys.argv[4]
    
    success = post_to_discord(agent_name, task, status, message)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
