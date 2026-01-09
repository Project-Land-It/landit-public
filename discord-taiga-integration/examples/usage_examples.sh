#!/bin/bash
# Discord-Taiga Integration Usage Examples

# Set required environment variables
export DISCORD_AGENT_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
export TAIGA_USERNAME="your_username"
export TAIGA_PASSWORD="your_password"

# Path to script (adjust as needed)
SCRIPT="../discord_logger_with_taiga_avatars.py"

echo "🚀 Discord-Taiga Integration Examples"
echo ""

# Example 1: Task completed successfully
echo "Example 1: Task completed ✅"
python3 "$SCRIPT" \
  "Charlie" \
  "Backend deployment complete" \
  "✅" \
  "Successfully deployed Spring Boot backend to DEV environment. All tests passing."

sleep 2

# Example 2: Task in progress
echo "Example 2: Task in progress 🔄"
python3 "$SCRIPT" \
  "Frankie" \
  "Building responsive navigation" \
  "🔄" \
  "Working on mobile-first navigation component with Tailwind CSS. ETA: 30 minutes."

sleep 2

# Example 3: Warning/Blocked
echo "Example 3: Warning/Blocked ⚠️"
python3 "$SCRIPT" \
  "Dexter" \
  "Container not responding" \
  "⚠️" \
  "DEV container (7003) is not responding to health checks. Investigating network connectivity."

sleep 2

# Example 4: Error/Failed
echo "Example 4: Error/Failed ❌"
python3 "$SCRIPT" \
  "Tessa" \
  "E2E tests failed" \
  "❌" \
  "E2E tests failed on login flow. Error: 'Submit button not found'. Debugging..."

sleep 2

# Example 5: Long message (auto-split)
echo "Example 5: Long message (auto-split)"
python3 "$SCRIPT" \
  "Riley" \
  "Architecture research complete" \
  "✅" \
  "Completed comprehensive research on microservices architecture for Land-It platform.

Key Findings:
1. API Gateway pattern recommended for frontend-backend communication
2. Event-driven architecture for real-time notifications
3. Redis for session management and caching
4. PostgreSQL with read replicas for scalability
5. Docker Compose for local development
6. Kubernetes for production deployment

Next Steps:
- Create technical design document
- Review with team
- Start POC implementation

Estimated Timeline: 2 weeks for POC, 6 weeks for full implementation."

sleep 2

# Example 6: Multiple agents in sequence
echo "Example 6: Agent collaboration workflow"

python3 "$SCRIPT" \
  "Max" \
  "SEO audit complete" \
  "✅" \
  "Completed SEO audit. Identified 15 optimization opportunities. Handoff to Frankie for implementation."

sleep 1

python3 "$SCRIPT" \
  "Frankie" \
  "Implementing SEO improvements" \
  "🔄" \
  "Received handoff from Max. Working on meta tags, schema markup, and sitemap generation."

sleep 1

python3 "$SCRIPT" \
  "Frankie" \
  "SEO improvements deployed" \
  "✅" \
  "All SEO improvements deployed to DEV. Ready for Tessa to test."

sleep 1

python3 "$SCRIPT" \
  "Tessa" \
  "Testing SEO changes" \
  "🔄" \
  "Running SEO validation tests. Checking meta tags, schema markup, and sitemap."

sleep 1

python3 "$SCRIPT" \
  "Tessa" \
  "SEO tests passed" \
  "✅" \
  "All SEO tests passed. Ready for production deployment. Handoff to Dexter."

sleep 1

python3 "$SCRIPT" \
  "Dexter" \
  "Deploying to production" \
  "✅" \
  "SEO improvements deployed to production. Monitoring for errors."

echo ""
echo "✅ All examples completed!"
echo ""
echo "Check your Discord channel to see the notifications with agent avatars!"
