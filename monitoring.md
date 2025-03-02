# Bot Monitoring Setup Guide

This guide outlines how to set up a lightweight monitoring system for `bot.py` with notifications via ntfy.sh.

## Overview

The monitoring script:
- Checks every 15 seconds if `bot.py` is running
- Automatically restarts the bot if it crashes
- Sends notifications via ntfy.sh when issues occur
- Logs restart events to a file
- Uses minimal system resources

## Setup Instructions

### 1. Create the Monitoring Script

Run the following command to create the monitoring script:

```bash
cat > monitor_bot.sh << 'EOL'
#!/bin/bash

# Simple script to monitor bot.py and restart if not running
# Sends notifications via ntfy.sh when bot is down
# Created $(date)

# Set your ntfy.sh topic
NTFY_TOPIC="dsc-bot-moondream-prod"

# Initialize counter for consecutive failures
failures=0

while true; do
  if ! pgrep -f "python bot.py" > /dev/null; then
    # Increment failure counter
    ((failures++))
    
    # Log restart attempt
    echo "[$(date)] Bot not running (failure #$failures). Attempting restart..." >> monitor_restart.log
    
    # Restart the bot
    cd "$(dirname "$0")" # Change to script directory
    python bot.py &      # Start bot in background
    
    # Send notification via ntfy.sh
    curl -H "Title: Bot Down Alert" \
         -H "Priority: high" \
         -H "Tags: warning,bot,restart" \
         -d "Python bot.py is down! Attempting restart #$failures at $(date). Check server." \
         https://ntfy.sh/$NTFY_TOPIC
    
    sleep 5  # Wait to ensure bot started properly
    
    # Check if restart was successful
    if ! pgrep -f "python bot.py" > /dev/null; then
      # Send critical notification if restart failed
      curl -H "Title: CRITICAL: Bot Restart Failed" \
           -H "Priority: urgent" \
           -H "Tags: error,bot,critical" \
           -d "Failed to restart bot.py after attempt #$failures. Immediate attention required!" \
           https://ntfy.sh/$NTFY_TOPIC
    else
      # Send recovery notification
      curl -H "Title: Bot Recovered" \
           -H "Priority: default" \
           -H "Tags: success,bot,recovery" \
           -d "Bot successfully restarted after being down (attempt #$failures)." \
           https://ntfy.sh/$NTFY_TOPIC
      
      # Reset failure counter on successful restart
      failures=0
    fi
  fi
  sleep 15  # Check every 15 seconds
done
EOL
```

### 2. Make the Script Executable

```bash
chmod +x monitor_bot.sh
```

### 3. Set Up Notifications

1. Install the ntfy app on your device:
   - Android: [Google Play](https://play.google.com/store/apps/details?id=io.heckel.ntfy)
   - iOS: [App Store](https://apps.apple.com/us/app/ntfy/id1625396347)
   - Or use the web interface at [ntfy.sh](https://ntfy.sh/)

2. Subscribe to the topic `dsc-bot-moondream-prod` in the app

### 4. Start the Monitoring Script

To run the script in the background and keep it running after you disconnect:

```bash
nohup ./monitor_bot.sh > /dev/null 2>&1 &
```

### 5. Check That Monitoring Is Active

```bash
ps aux | grep monitor_bot.sh
```

You should see the script running.

### 6. Verify Notification Setup

Test that notifications are working by temporarily stopping the bot:

```bash
pkill -f "python bot.py"
```

You should receive a notification within 15 seconds, and another notification when the bot restarts.

### 7. Monitor Logs

View restart logs with:

```bash
cat monitor_restart.log
```

## Troubleshooting

- If the script isn't detecting the bot, check that the bot process name matches exactly "python bot.py"
- Make sure curl is installed: `apt-get install curl` (on Ubuntu/Debian)
- Ensure the VM has internet access to reach ntfy.sh
- Check that the monitor script and bot.py are in the same directory

## Additional Notes

- The script logs only when restarts happen, to conserve disk space
- Notifications include failure count to help identify recurring issues
- To stop monitoring: `pkill -f "monitor_bot.sh"`