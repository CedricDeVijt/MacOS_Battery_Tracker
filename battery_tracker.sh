#!/bin/zsh

# This script is used to set up and run the battery_tracker.py script in a virtual environment.
# It first navigates to the directory of the script, sets up a Python virtual environment, installs the necessary dependencies, and then runs the script.

# Get the directory of the path of the current script relative to the home directory
DIR_FROM_HOME=$(dirname "$0")

# Change to the directory of the script
cd "$HOME/$DIR_FROM_HOME" || exit

# Change to the src directory
cd src || exit

# Set up a Python virtual environment
python3 -m venv venv

# Activate the Python virtual environment
source venv/bin/activate

# Install the necessary dependencies
pip install -r requirements.txt > /dev/null

# Run the battery_tracker.py script
python battery_tracker.py

# Deactivate the Python virtual environment
deactivate