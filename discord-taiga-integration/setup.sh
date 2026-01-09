#!/bin/bash
# Setup Taiga Avatar Integration for Discord Logging
# Adds Taiga credentials to .env file for avatar fetching

ENV_FILE="/home/devuser/project_landit/.claude/.env"

echo "🔧 Setting up Taiga Avatar Integration..."
echo ""

# Check if .env exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Creating .env file..."
    touch "$ENV_FILE"
fi

# Add Taiga credentials if not already present
if ! grep -q "TAIGA_USERNAME" "$ENV_FILE"; then
    echo "Adding TAIGA_USERNAME to .env..."
    echo "" >> "$ENV_FILE"
    echo "# Taiga Avatar Integration" >> "$ENV_FILE"
    echo "TAIGA_USERNAME=charlie" >> "$ENV_FILE"
else
    echo "✅ TAIGA_USERNAME already set in .env"
fi

if ! grep -q "TAIGA_PASSWORD" "$ENV_FILE"; then
    echo "Adding TAIGA_PASSWORD to .env..."
    echo "TAIGA_PASSWORD=agent2026" >> "$ENV_FILE"
else
    echo "✅ TAIGA_PASSWORD already set in .env"
fi

if ! grep -q "TAIGA_API_URL" "$ENV_FILE"; then
    echo "Adding TAIGA_API_URL to .env..."
    echo "TAIGA_API_URL=http://192.168.1.13:8080/api/v1" >> "$ENV_FILE"
else
    echo "✅ TAIGA_API_URL already set in .env"
fi

if ! grep -q "TAIGA_EXTERNAL_URL" "$ENV_FILE"; then
    echo "Adding TAIGA_EXTERNAL_URL to .env..."
    echo "TAIGA_EXTERNAL_URL=https://taiga.landit4.fun" >> "$ENV_FILE"
else
    echo "✅ TAIGA_EXTERNAL_URL already set in .env"
fi

echo ""
echo "✅ Taiga avatar integration configured!"
echo ""
echo "The discord_logger_with_taiga_avatars.py script will now:"
echo "  1. Fetch agent profile pictures from Taiga"
echo "  2. Convert internal URLs to external (taiga.landit4.fun)"
echo "  3. Use custom avatars in Discord notifications"
echo ""
echo "To test:"
echo "  python3 .claude/discord_logger_with_taiga_avatars.py 'Charlie' 'Test' '✅' 'Testing avatars!'"
echo ""
