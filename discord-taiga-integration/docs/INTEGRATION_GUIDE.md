# Taiga Avatar Integration for Discord Notifications

## Overview

The enhanced Discord logger (`discord_logger_with_taiga_avatars.py`) fetches agent profile pictures from Taiga and uses them as custom avatars in Discord webhook notifications.

## How It Works

1. **Fetches Taiga User Data**: Queries the Taiga API for users in the land-it project
2. **Matches Agent Names**: Finds the Taiga user matching the agent name (case-insensitive)
3. **Extracts Avatar URL**: Gets the `photo` or `big_photo` field from the user object
4. **Converts to External URL**: Replaces internal URLs (`192.168.1.13:8080`) with external ones (`taiga.landit4.fun`)
5. **Posts to Discord**: Uses the avatar URL in the Discord webhook `avatar_url` parameter

## Public URL Requirement

**Important**: Discord webhooks require **publicly accessible** avatar URLs. The avatar images must be reachable by Discord's servers.

Your current setup:
- ✅ **Internal**: `http://192.168.1.13:8080` (private network)
- ✅ **External**: `https://taiga.landit4.fun` (public via reverse proxy/Tailscale Funnel)

The script automatically converts internal Taiga media URLs to use your external domain, so Discord can access them.

## Setup

### 1. Environment Variables

```bash
# Required
export DISCORD_AGENT_WEBHOOK_URL="your_discord_webhook_url"

# For Taiga avatar integration (optional)
export TAIGA_USERNAME="your_taiga_username"
export TAIGA_PASSWORD="your_taiga_password"

# Optional (use defaults if not set)
export TAIGA_API_URL="http://192.168.1.13:8080/api/v1"
export TAIGA_EXTERNAL_URL="https://taiga.landit4.fun"
export TAIGA_INTERNAL_HOST="192.168.1.13:8080"
```

### 2. Ensure Taiga Users Match Agent Names

For avatar matching to work, your Taiga users should have usernames or full names matching agent names:

| Agent Name | Taiga Username | Taiga Full Name |
|------------|----------------|-----------------|
| Riley | `riley` | Riley |
| Charlie | `charlie` | Charlie |
| Frankie | `frankie` | Frankie |
| Andy | `andy` | Andy |
| Tessa | `tessa` | Tessa |
| Dexter | `dexter` | Dexter |
| Max | `max` | Max |
| Alex | `alex` | Alex |
| Sage | `sage` | Sage |
| Finn | `finn` | Finn |
| Lex | `lex` | Lex |
| Sammy | `sammy` | Sammy |
| Scribbles | `scribbles` | Scribbles |

### 3. Upload Agent Avatars to Taiga

You can upload profile pictures to Taiga either:

**Via Web UI:**
1. Log in to https://taiga.landit4.fun
2. Click on user profile (top right)
3. Edit profile
4. Upload avatar image

**Via API** (using the images from `.claude/agent-profiles/`):
```bash
# Example script to upload avatar
curl -X POST "http://192.168.1.13:8080/api/v1/users/change-avatar" \
  -H "Authorization: Bearer $TOKEN" \
  -F "avatar=@.claude/agent-profiles/riley.png"
```

## Usage

### Basic Usage

```bash
cd /home/devuser/project_landit
python3 .claude/discord_logger_with_taiga_avatars.py \
  "Riley" \
  "Complete research task" \
  "✅" \
  "Successfully analyzed codebase structure and identified key components."
```

### From Agent Skill (log-to-chat)

Update `.claude/commands/log-to-chat-discord.md` to use the new script:

```bash
python3 .claude/discord_logger_with_taiga_avatars.py "{agent_name}" "{task_description}" "{status_emoji}" "{detailed_message}"
```

## Behavior

### When Taiga Credentials Are Set
- ✅ Fetches avatar from Taiga API
- ✅ Converts internal URLs to external
- ✅ Uses custom avatar in Discord
- ✅ Caches avatars to avoid repeated API calls

### When Taiga Credentials Are NOT Set
- ⚠️ Falls back to default webhook avatar
- ⚠️ Still posts to Discord normally
- ⚠️ Logs warning message

### When Agent Not Found in Taiga
- ⚠️ Falls back to default webhook avatar
- ⚠️ Still posts to Discord normally
- ⚠️ Caches negative result to avoid repeated lookups

## Avatar URL Format

Taiga provides avatar URLs in several formats:
- `photo` - Standard size (e.g., 80x80)
- `big_photo` - Larger size (e.g., 400x400)

The script prefers `photo` but falls back to `big_photo` if available.

Example URLs:
```
Internal:  http://192.168.1.13:8080/media/user/1/avatar_80x80.png
External:  https://taiga.landit4.fun/media/user/1/avatar_80x80.png
```

## Testing

Test the integration:

```bash
# Set credentials (replace with real values)
export TAIGA_USERNAME="your_username"
export TAIGA_PASSWORD="your_password"
export DISCORD_AGENT_WEBHOOK_URL="your_webhook_url"

# Test with a real agent
python3 .claude/discord_logger_with_taiga_avatars.py \
  "Charlie" \
  "Test Taiga avatar integration" \
  "🔄" \
  "Testing if Charlie's Taiga profile picture appears in Discord!"
```

Check Discord to see if the avatar appears!

## Troubleshooting

### Avatar Not Showing in Discord

1. **Check Taiga user exists**:
   ```bash
   curl -X POST "http://192.168.1.13:8080/api/v1/auth" \
     -H "Content-Type: application/json" \
     -d '{"username":"YOUR_USER","password":"YOUR_PASS","type":"normal"}' \
     | jq .auth_token
   
   # Use token to check users
   curl "http://192.168.1.13:8080/api/v1/users?project=1" \
     -H "Authorization: Bearer YOUR_TOKEN" | jq '.[] | {username, full_name, photo}'
   ```

2. **Verify external URL is accessible**:
   ```bash
   # Test if Taiga media is publicly accessible
   curl -I https://taiga.landit4.fun/media/user/1/avatar.png
   ```

3. **Check script logs**:
   The script outputs:
   - `ℹ️  Using Taiga avatar: <url>` - Avatar found and used
   - `ℹ️  No Taiga avatar found for <agent>, using default` - Fallback to default
   - `⚠️  Warning: Failed to fetch Taiga avatar` - API error

4. **Discord may cache avatars**: Wait a few minutes or use a different webhook to see changes

### External URL Not Working

If `taiga.landit4.fun` media URLs aren't accessible:

1. **Check reverse proxy/Tailscale Funnel configuration**
2. **Ensure media files are served correctly**
3. **Test with curl**: `curl -I https://taiga.landit4.fun/media/test.png`

### Fallback Option: Use Local Images

If you can't get Taiga media URLs working publicly, you could:
1. Upload agent profile images to a CDN or public server
2. Modify the script to use those URLs instead

## Performance

- **Caching**: Avatar URLs are cached in memory to avoid repeated API calls
- **Timeout**: API calls timeout after 5 seconds to prevent blocking
- **Graceful Degradation**: Falls back to default avatar if anything fails

## Security

- **Credentials**: Taiga credentials are only used internally, never sent to Discord
- **HTTPS**: External URLs use HTTPS for security
- **No Secrets in Logs**: Avatar URLs are logged but contain no sensitive data

---

**Created**: January 9, 2026  
**Status**: Ready for testing ✅
