# Discord-Taiga Avatar Integration

Display Taiga user profile pictures as custom avatars in Discord webhook notifications.

## ✨ Features

- 🎨 **Custom Avatars** - Fetches user profile pictures from Taiga API
- 🔄 **URL Conversion** - Automatically converts internal URLs to external
- 💾 **Smart Caching** - Caches avatar URLs to minimize API calls
- 🛡️ **Graceful Fallback** - Uses default webhook avatar if not found
- ⚡ **Fast & Reliable** - 5-second timeout, non-blocking execution
- 🔒 **Secure** - Credentials only used internally, never exposed

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip3 install requests
# Optional for database integration
pip3 install asyncpg
```

### 2. Configure Environment

```bash
# Run setup script
./setup.sh

# Or manually edit .env:
export DISCORD_AGENT_WEBHOOK_URL="your_webhook_url"
export TAIGA_USERNAME="your_username"
export TAIGA_PASSWORD="your_password"
export TAIGA_API_URL="http://192.168.1.13:8080/api/v1"
export TAIGA_EXTERNAL_URL="https://taiga.landit4.fun"
```

### 3. Usage

```bash
python3 discord_logger_with_taiga_avatars.py \
  "Charlie" \
  "Deployed backend to DEV" \
  "✅" \
  "Successfully deployed Spring Boot backend to DEV environment."
```

## 📖 Documentation

- **[Integration Guide](docs/INTEGRATION_GUIDE.md)** - Complete setup and usage guide
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[API Reference](docs/API_REFERENCE.md)** - Function documentation

## 🎯 How It Works

```
Agent Task Completion
     ↓
discord_logger_with_taiga_avatars.py
     ↓
1. Authenticate with Taiga API
2. Search for user matching agent name
3. Extract photo URL from user object
4. Convert: http://internal:8080/media/... → https://external.com/media/...
5. Post to Discord with avatar_url parameter
     ↓
Discord displays custom avatar! 🎉
```

## 🔧 Configuration

### Required Environment Variables

```bash
DISCORD_AGENT_WEBHOOK_URL  # Discord webhook URL
```

### Optional (for avatar integration)

```bash
TAIGA_USERNAME             # Taiga username
TAIGA_PASSWORD             # Taiga password
TAIGA_API_URL              # Taiga API endpoint (default: http://192.168.1.13:8080/api/v1)
TAIGA_EXTERNAL_URL         # External Taiga URL (default: https://taiga.landit4.fun)
TAIGA_INTERNAL_HOST        # Internal host to replace (default: 192.168.1.13:8080)
```

### Optional (for database integration)

```bash
DB_HOST                    # PostgreSQL host
DB_PORT                    # PostgreSQL port
DB_NAME                    # Database name
DB_USER                    # Database user
DB_PASSWORD                # Database password
```

## 📋 Examples

### Basic Usage

```bash
# Post with status icon
python3 discord_logger_with_taiga_avatars.py \
  "Riley" \
  "Research complete" \
  "✅" \
  "Completed architecture research for new feature."

# Post with warning
python3 discord_logger_with_taiga_avatars.py \
  "Dexter" \
  "Deployment blocked" \
  "⚠️" \
  "Container 7003 is not responding. Investigating..."

# Post in progress
python3 discord_logger_with_taiga_avatars.py \
  "Frankie" \
  "Building UI components" \
  "🔄" \
  "Working on responsive navigation component."
```

### Status Icons

- ✅ **Complete** - Task finished successfully
- 🔄 **In Progress** - Currently working on task
- ⚠️ **Warning/Blocked** - Issue encountered, needs attention
- ❌ **Error/Failed** - Task failed

## 🌐 Public URL Requirement

Discord webhooks require **publicly accessible** avatar URLs. The script automatically converts internal Taiga URLs to your external domain.

**Example Conversion:**
```
Internal:  http://192.168.1.13:8080/media/user/1/avatar.png
           ↓
External:  https://taiga.landit4.fun/media/user/1/avatar.png
           ↓
Discord:   ✅ Can access!
```

Make sure your external Taiga URL serves `/media/*` paths publicly (via reverse proxy or Tailscale Funnel).

## 🧪 Testing

```bash
# Set credentials
export TAIGA_USERNAME="charlie"
export TAIGA_PASSWORD="your_password"
export DISCORD_AGENT_WEBHOOK_URL="your_webhook_url"

# Test avatar fetch
python3 -c "
from discord_logger_with_taiga_avatars import get_taiga_user_avatar
print(get_taiga_user_avatar('Charlie'))
"

# Test full integration
python3 discord_logger_with_taiga_avatars.py \
  "Charlie" \
  "Avatar Test" \
  "🔄" \
  "Testing Taiga avatar integration!"
```

## 📊 Agent Metadata

The script includes pre-configured metadata for all Land-It agents:

- Riley (🔮 Indigo)
- Charlie (🔵 Blue)
- Frankie (🟢 Green)
- Andy (🟠 Orange)
- Tessa (🟡 Dark Yellow)
- Dexter (🟣 Purple)
- Sammy (🛡️ Red/White)
- Max (🔴 Red)
- Alex (🩵 Cyan)
- Sage (🩷 Magenta)
- Finn (💛 Yellow)
- Lex (⚪ Gray)
- Scribbles (📜 Brown)

## 🔐 Security

- Taiga credentials only used internally
- HTTPS for external URLs
- 5-second timeout prevents blocking
- Silent failure on errors (doesn't break logging)
- No secrets logged to console

## 🤝 Contributing

This tool was built for the Land-It project but can be adapted for any Taiga + Discord integration.

**Ideas for contributions:**
- Support for other project management tools (Jira, Linear)
- Webhook signature verification
- Retry logic with exponential backoff
- Avatar image optimization
- Multi-language support

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details.

## 🔗 Related

- **[Agent Profiles](../agent-profiles/)** - Profile pictures for all agents
- **[Land-It Main Repo](https://github.com/Project-Land-It)** - The Land-It platform

---

**Created**: January 9, 2026  
**Status**: Production Ready ✅  
**Tested With**: Charlie agent on Land-It project
