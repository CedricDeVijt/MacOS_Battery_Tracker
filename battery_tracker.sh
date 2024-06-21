#!/bin/zsh
cd src || exit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt > /dev/null
python battery_tracker.py
deactivate
