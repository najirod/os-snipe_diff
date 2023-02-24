#!/bin/bash

# Activate virtual environment
source /var/www/os-snipe_diff/venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create database tables
python db_create.py
