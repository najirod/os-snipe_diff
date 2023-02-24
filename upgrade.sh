#!/bin/bash

# Activate virtual environment
source /var/www/os-snipe_diff/venv/bin/activate

# Pull from Git
cd /var/www/os-snipe_diff/
git fetch
git stash
git pull

# Install requirements
pip install -r requirements.txt

# Set permissions
sudo chmod -R 777 /var/www/os-snipe_diff/

# Restart Apache2 server
sudo service apache2 restart
