# Avatar Troubleshooting Guide

## Status: Avatar URL Being Sent ✅, Display Issue ⚠️

### What's Working
- ✅ Script successfully fetches avatar from Taiga API
- ✅ URL conversion to external domain (taiga.landit4.fun)
- ✅ Discord webhook accepts the payload (204 response)
- ✅ Avatar URL: `https://taiga.landit4.fun/media/user/.../charlie.png`

### The Issue
Discord's servers may not be able to access the avatar URL because:

1. **External Access to Media Files**
   - Your Taiga domain: `taiga.landit4.fun` → 24.163.6.159
   - Main Taiga page loads fine (HTTP 200)
   - But `/media/` path may need special routing configuration

2. **Token-Based URLs**
   - Taiga avatar URLs include authentication tokens
   - Format: `?token=aWFu9w%3AYBQtCdrBHi...`
   - These tokens may expire or not work externally

3. **Nginx Proxy Manager Configuration**
   - The reverse proxy may not be configured to serve `/media/*` paths
   - Or it may require authentication that blocks Discord's bots

## Next Steps to Fix

### Option 1: Verify External Media Access (Recommended)
```bash
# From an external machine (not on your local network), test:
curl -I https://taiga.landit4.fun/media/user/.../charlie.png
```

If this returns 404 or 403, the media path isn't publicly accessible.

### Option 2: Configure Nginx to Serve Media Publicly
On the proxy-gateway VM (192.168.1.101), ensure Nginx routes `/media/*` correctly:

```nginx
location /media/ {
    proxy_pass http://192.168.1.13:8080/media/;
    # Remove authentication for media files
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### Option 3: Use Direct Image Upload (Alternative)
Instead of using Taiga avatars, upload the agent profile images directly to Discord or a CDN:

```bash
# Upload images from .claude/agent-profiles/ to:
# - Discord CDN (via attachment)
# - AWS S3 / CloudFlare R2
# - Your web server's public directory
```

### Option 4: Test Without Auth Tokens
Taiga may require the token for internal access but not external. Test if we can use the URL without the token parameter.

## Quick Test

Run this from an external network (not your local network):
```bash
curl -I "https://taiga.landit4.fun/media/user/0/6/9/b/07613e48c4fd95af398c2fff9a36c81ae03247974fd3f9f936d17b0dd846/charlie.png.80x80_q85_crop.jpg"
```

Expected:
- ✅ 200 OK with image/jpeg or image/png
- ❌ 403 Forbidden (authentication issue)
- ❌ 404 Not Found (routing issue)
- ❌ 502 Bad Gateway (proxy issue)

## Current Workaround

Until external media access is fixed, you can:
1. Keep using the new script (it won't break anything)
2. Avatars will use the default webhook avatar
3. Once media is accessible externally, avatars will automatically appear

## Verification Script

```bash
# Test avatar URL from Discord's perspective
python3 << 'PYEOF'
import requests

url = "https://taiga.landit4.fun/media/user/0/6/9/b/07613e48c4fd95af398c2fff9a36c81ae03247974fd3f9f936d17b0dd846/charlie.png.80x80_q85_crop.jpg?token=aWFu9w%3AYBQtCdrBHi7lR-kUVt_8ByWGcUORT8P0kc5c2SCfF4P12uPsUds_IKN4E9ee2eTNkOxGEa5ogH8Gb1XmOGhMvQ"

try:
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"Content-Length: {response.headers.get('Content-Length')}")
    
    if response.status_code == 200:
        print("✅ Avatar URL is publicly accessible!")
    else:
        print(f"❌ Avatar URL returned: {response.status_code}")
except Exception as e:
    print(f"❌ Error accessing avatar: {e}")
PYEOF
```

---

**Status**: Integration complete, awaiting external media configuration
**Next Action**: Configure Nginx Proxy Manager to serve /media/ publicly
