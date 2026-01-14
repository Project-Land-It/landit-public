# GitHub Raw URLs for Agent Profile Images

Base URL pattern:
```
https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/{agent_name}.png
```

## All Agent URLs

### Standard Profiles (12 agents)

| Agent | Emoji | Color | GitHub Raw URL |
|-------|-------|-------|----------------|
| Alex | 🩵 | Cyan | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/alex.png` |
| Andy | 🟠 | Orange | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/andy.png` |
| Charlie | 🔵 | Blue | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/charlie.png` |
| Dexter | 🟣 | Purple | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/dexter.png` |
| Finn | 💛 | Yellow | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/finn.png` |
| Frankie | 🟢 | Green | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/frankie.png` |
| Lex | ⚪ | Gray | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/lex.png` |
| Riley | 🔮 | Indigo | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/riley.png` |
| Sage | 🩷 | Magenta | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/sage.png` |
| Sammy | 🛡️ | Red/White | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/sammy.png` |
| Tessa | 🟡 | Yellow | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/tessa.png` |

### Realistic Variants (3 agents)

| Agent | Emoji | Color | GitHub Raw URL |
|-------|-------|-------|----------------|
| Dexter (Realistic) | 🟣 | Purple | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/dexter_realistic.png` |
| Max (Realistic) | 🔴 | Red | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/max_realistic.png` |
| Scribbles (Realistic) | 📜 | Brown | `https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/scribbles_realistic.png` |

## Usage in Discord

For Discord webhooks, use the `avatar_url` field:

```python
import requests

webhook_url = "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

# Example: Posting as Charlie
payload = {
    "username": "🔵 Charlie",
    "avatar_url": "https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/charlie.png",
    "content": "Backend deployment complete!"
}

requests.post(webhook_url, json=payload)
```

## Python Dictionary for Integration

```python
AGENT_AVATARS = {
    'alex': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/alex.png',
    'andy': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/andy.png',
    'charlie': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/charlie.png',
    'dexter': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/dexter.png',
    'finn': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/finn.png',
    'frankie': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/frankie.png',
    'lex': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/lex.png',
    'max': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/max_realistic.png',
    'riley': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/riley.png',
    'sage': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/sage.png',
    'sammy': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/sammy.png',
    'scribbles': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/scribbles_realistic.png',
    'tessa': 'https://raw.githubusercontent.com/Project-Land-It/landit-public/main/agent-profiles/tessa.png',
}
```

## Verification

All URLs verified accessible on $(date -u +"%Y-%m-%d"):
- HTTP 200 response from raw.githubusercontent.com
- No authentication required
- Images served as image/png MIME type

---

**Last Updated**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
