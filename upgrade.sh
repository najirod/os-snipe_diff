#!/bin/bash

#!/bin/sh

# Define color codes using tput
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
NC=$(tput sgr0) # No Color


# Exit immediately if any command fails
set -e

echo "Activating virtual environment..."
source /var/www/os-snipe_diff/venv/bin/activate
echo "Virtual environment activated."

echo "Fetching updates from Git..."
cd /var/www/os-snipe_diff/
git fetch
echo "Local changes are being stashed..."
git stash
echo "Local changes stashed."
echo "Pulling the latest changes from the Git repository..."
git pull
echo "Latest changes pulled."

echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "Dependencies installed."

echo "Setting permissions..."
sudo chmod -R 777 /var/www/os-snipe_diff/
echo "Permissions set."

echo "Restarting Apache2 server..."
sudo service apache2 restart
echo "Apache2 server restarted."

echo -e "${GREEN}UPDATED :)${NC}"