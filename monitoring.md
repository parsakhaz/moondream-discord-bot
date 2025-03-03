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

### 2.1 Setup System Process to Monitor the Auto-Restart service

Set up a process to ensure the monitoring script automatically boots up on restart

```
sudo tee /etc/systemd/system/monitor-health-check.service > /dev/null << 'EOL'
[Unit]
Description=Monitor Health Check Service
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'while true; do if ! systemctl is-active --quiet bot-monitor; then curl -H "Title: CRITICAL: Monitor Down" -H "Priority: urgent" -H "Tags: error,monitor,critical" -d "The bot monitoring service itself is down! System needs immediate attention." https://ntfy.sh/dsc-bot-moondream-prod; fi; sleep 60; done'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl restart monitor-health-check
```

```
# Check if the service is active and running
sudo systemctl status bot-monitor monitor-health-check

# Check logs from the service
sudo journalctl -u bot-monitor -f
```

### 2.2 Test the bot monitoring services monitoring service

```
# Kill the bot-monitor service
sudo systemctl stop bot-monitor

# Wait a few minutes (up to 5 minutes based on the check interval)
# You should receive a notification that the monitor is down

# Verify it's actually stopped
sudo systemctl status bot-monitor
# Should show "inactive (dead)"

# Start it back up again
sudo systemctl start bot-monitor

# Verify it's running again
sudo systemctl status bot-monitor
# Should show "active (running)"
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

## Sanity Check

To test that everything is running properly, you'll need to check both the bot process and the monitoring systems. Here are the commands to run:

1. **Check that the bot is running:**
   ```bash
   pgrep -f "python bot.py"
   ```
   This should return a process ID if the bot is running.

2. **Check that the monitor script is running:**
   ```bash
   ps aux | grep monitor_bot.sh
   ```
   This should show the monitoring script process.

3. **Check that the systemd services are active:**
   ```bash
   sudo systemctl status bot-monitor monitor-health-check
   ```
   Both services should show as "active (running)" with green dots.

4. **View the logs from the monitoring services:**
   ```bash
   sudo journalctl -u bot-monitor -n 20
   sudo journalctl -u monitor-health-check -n 20
   ```

5. **Check the restart log to see if any restarts have occurred:**
   ```bash
   cat monitor_restart.log
   ```

6. **Test the bot monitoring by killing the bot:**
   ```bash
   pkill -f "python bot.py"
   ```
   Wait 15 seconds - you should get a notification that the bot was down and restarted.

7. **Test the monitor-health-check by stopping the bot-monitor service:**
   ```bash
   sudo systemctl stop bot-monitor
   ```
   Wait about a minute - you should get a notification that the monitoring service is down.

8. **Don't forget to restart the bot-monitor after testing:**
   ```bash
   sudo systemctl start bot-monitor
   ```

These commands will help you verify that all components of your monitoring setup are functioning properly.
