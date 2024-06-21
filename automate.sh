#!/bin/zsh

# This script automates the process of setting up a cron job for the battery_tracker.sh script.

# Get the directory of the current script relative to the home directory
DIR_FROM_HOME="${PWD#$HOME/}"

# Path to the battery_tracker.sh script
SCRIPT_PATH="$DIR_FROM_HOME/battery_tracker.sh"

# Make the script executable
DIR="$(dirname "$0")"
# Change the permission of the battery_tracker.sh script to make it executable
if [ -f ./"$DIR"/battery_tracker.sh ]; then
    # If the file exists, change its permissions to make it executable
    chmod +x ./"$DIR"/battery_tracker.sh
else
    # If the file does not exist, print an error message and exit the script
    echo "Error: File ./$DIR/battery_tracker.sh does cannot be found."
    exit 1
fi

# Check if the cron job already exists
CRON_JOB="0 12 * * 1 ./$SCRIPT_PATH"
# Check if the cron job already exists in the crontab
if crontab -l | grep -q "0 12 \* \* 1.*battery_tracker\.sh"; then
    echo "Cron job already exists."
else
    # If the cron job does not exist, add it to the crontab
    echo "Cron job does not exist. Adding it..."
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
fi

# If the cron job was added successfully, print a success message. Otherwise, print a failure message.
if crontab -l | grep -q "0 12 \* \* 1.*battery_tracker\.sh"; then
    echo "Cron job added successfully."
else
    echo "Failed to add cron job."
fi