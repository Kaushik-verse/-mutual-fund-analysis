#!/bin/bash
# scripts/schedule_cron.sh
# Bonus B1: Schedule ETL as a cron job auto-fetching NAV from mfapi.in every weekday at 8 PM

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." >/dev/null 2>&1 && pwd)"
PYTHON_EXEC="$PROJECT_DIR/venv/bin/python"
SCRIPT_PATH="$PROJECT_DIR/scripts/live_nav_fetch.py"

# Define the cron job line:
# 0 20 * * 1-5 = 8:00 PM every Monday through Friday
CRON_CMD="0 20 * * 1-5 cd $PROJECT_DIR && $PYTHON_EXEC $SCRIPT_PATH >> $PROJECT_DIR/logs/cron.log 2>&1"

# Check if the job already exists
(crontab -l 2>/dev/null | grep -F "$SCRIPT_PATH") > /dev/null
if [ $? -eq 0 ]; then
    echo "Cron job for live_nav_fetch.py is already scheduled."
else
    # Append the new cron job
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "Successfully scheduled cron job:"
    echo "$CRON_CMD"
    echo "This will fetch NAV data every weekday at 8:00 PM."
    mkdir -p "$PROJECT_DIR/logs"
fi
