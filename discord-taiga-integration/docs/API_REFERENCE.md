# API Reference

## Functions

### `get_taiga_auth_token()`

Authenticate with Taiga and return auth token.

**Returns:** `str | None` - Auth token or None if authentication fails

**Environment Variables:**
- `TAIGA_USERNAME` - Taiga username
- `TAIGA_PASSWORD` - Taiga password
- `TAIGA_URL` - Taiga API URL

### `get_taiga_user_avatar(agent_name: str)`

Fetch user avatar from Taiga API by searching for username matching agent name.

**Parameters:**
- `agent_name` (str) - Name of the agent (case-insensitive)

**Returns:** `str | None` - External avatar URL or None if not found

**Behavior:**
- Checks cache first
- Searches Taiga users by username or full name
- Converts internal URLs to external
- Caches result (positive or negative)

**Example:**
```python
avatar_url = get_taiga_user_avatar("Charlie")
# Returns: "https://taiga.landit4.fun/media/user/.../charlie.png"
```

### `convert_to_external_url(url: str)`

Convert internal Taiga URLs to external ones.

**Parameters:**
- `url` (str) - Internal or relative URL

**Returns:** `str | None` - External URL or None if conversion fails

**Examples:**
```python
# Protocol-relative
convert_to_external_url("//192.168.1.13:8080/media/avatar.png")
# → "https://taiga.landit4.fun/media/avatar.png"

# Absolute path
convert_to_external_url("/media/avatar.png")
# → "https://taiga.landit4.fun/media/avatar.png"

# Full internal URL
convert_to_external_url("http://192.168.1.13:8080/media/avatar.png")
# → "https://taiga.landit4.fun/media/avatar.png"
```

### `update_agent_state_db(agent_name: str, status: str, task_description: str = None)`

Update agent state in PostgreSQL database (optional, async).

**Parameters:**
- `agent_name` (str) - Agent name
- `status` (str) - Status emoji (✅, 🔄, ⚠️, ❌)
- `task_description` (str, optional) - Task description

**Returns:** `None`

**Database Mapping:**
- ✅ → `IDLE`
- 🔄 → `WORKING`
- ⚠️ → `BLOCKED`
- ❌ → `IDLE`

**Requirements:**
- `asyncpg` package installed
- `DB_PASSWORD` environment variable set

### `post_to_discord(agent_name: str, task: str, status: str, message: str)`

Post message to Discord webhook with Taiga avatar.

**Parameters:**
- `agent_name` (str) - Agent name
- `task` (str) - Task description (concise)
- `status` (str) - Status emoji
- `message` (str) - Detailed message

**Returns:** `bool` - True if successful, False otherwise

**Behavior:**
- Fetches Taiga avatar
- Splits long messages into multiple fields (max 1024 chars each)
- Builds Discord embed with agent color
- Posts with custom username and avatar if found
- Falls back to default webhook avatar

**Example:**
```python
success = post_to_discord(
    "Charlie",
    "Deploy backend",
    "✅",
    "Successfully deployed to DEV"
)
```

## Constants

### `AGENT_METADATA`

Dictionary mapping agent names to emoji and color codes.

**Structure:**
```python
{
    'agent_name_lower': {
        'emoji': 'emoji_character',
        'color': 0xHEXCOLOR
    }
}
```

**Example:**
```python
AGENT_METADATA['charlie']
# → {'emoji': '🔵', 'color': 0x0000FF}
```

### Agent Colors

| Agent | Emoji | Hex Color |
|-------|-------|-----------|
| Riley | 🔮 | 0x4B0082 (Indigo) |
| Charlie | 🔵 | 0x0000FF (Blue) |
| Frankie | 🟢 | 0x00FF00 (Green) |
| Andy | 🟠 | 0xFF8C00 (Orange) |
| Tessa | 🟡 | 0xFFD700 (Gold) |
| Dexter | 🟣 | 0x800080 (Purple) |
| Sammy | 🛡️ | 0xC0C0C0 (Silver) |
| Max | 🔴 | 0xFF0000 (Red) |
| Alex | 🩵 | 0x00FFFF (Cyan) |
| Sage | 🩷 | 0xFF00FF (Magenta) |
| Finn | 💛 | 0xFFFF00 (Yellow) |
| Lex | ⚪ | 0x808080 (Gray) |
| Scribbles | 📜 | 0x8B4513 (Brown) |
| Claude | 🤖 | 0x000000 (Black) |

## Environment Variables

### Required

```bash
DISCORD_AGENT_WEBHOOK_URL  # Discord webhook URL
```

### Taiga Integration (Optional)

```bash
TAIGA_USERNAME="username"                              # Taiga username
TAIGA_PASSWORD="password"                              # Taiga password
TAIGA_API_URL="http://192.168.1.13:8080/api/v1"      # API endpoint
TAIGA_EXTERNAL_URL="https://taiga.landit4.fun"       # External URL
TAIGA_INTERNAL_HOST="192.168.1.13:8080"              # Internal host
```

### Database Integration (Optional)

```bash
DB_HOST="192.168.1.11"      # PostgreSQL host
DB_PORT="5432"              # PostgreSQL port
DB_NAME="landit_sit_db"     # Database name
DB_USER="landit"            # Database user
DB_PASSWORD="password"      # Database password
```

## Error Handling

### Taiga API Errors
- Authentication failure → Returns None, logs warning
- Network timeout (5s) → Returns None, logs warning
- User not found → Caches negative result, returns None

### Discord API Errors
- Webhook URL not set → Prints error, exits 1
- Network error → Prints error, returns False
- Invalid status code → Prints error, returns False

### Database Errors
- asyncpg not installed → Silently skips DB updates
- Connection timeout (5s) → Silently fails
- Query error → Silently fails

## Performance

### Caching
- Avatar URLs cached in memory (`_avatar_cache`)
- Cache persists for script lifetime
- Both positive and negative results cached

### Timeouts
- Taiga API: 5 seconds
- Discord API: 10 seconds
- Database: 5 seconds

### Message Size Limits
- Total message: No limit (auto-split)
- Field size: 1024 characters max
- Fields created as needed for long messages

## CLI Usage

```bash
python3 discord_logger_with_taiga_avatars.py <agent_name> <task> <status> <message>
```

**Arguments:**
1. `agent_name` - Agent name (e.g., "Charlie")
2. `task` - Brief task description
3. `status` - Status emoji (✅, 🔄, ⚠️, ❌)
4. `message` - Detailed message

**Exit Codes:**
- `0` - Success
- `1` - Failure (missing args, Discord error)

**Example:**
```bash
python3 discord_logger_with_taiga_avatars.py \
  "Charlie" \
  "Backend deployment" \
  "✅" \
  "Deployed Spring Boot backend to DEV environment successfully."
```
