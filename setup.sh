#!/bin/bash

set -e

echo "Updating package list"
sudo apt-get update && sudo apt-get install upgrade -y

echo "Installing dependencies..."
sudo apt-get install -y git python3 python3-pip nodejs npm sqlite3

if [ -f "requirements.txt" ]; then
  echo "Installing Python dependencies..."
  pip3 install -r requirements.txt
fi

cd server

if [ -f "package.json" ]; then
  echo "Installing Node.js dependencies..."
  npm install
fi

cd ..

if [ ! -f "vehicles.db" ]; then
    echo "Creating vehicles.db database..."
    touch vehicles.db
fi

echo "Setup complete."

echo "Enter the camera's info"

read -p "Username: " username
read -p "IP Address: " ipaddress
read -sp "Password: " password
echo

CSV_FILE="camera.csv"

if [ ! -f "$CSV_FILE" ]; then
    echo "Creating $CSV_FILE..."
    echo "" > "$CSV_FILE"
fi

echo "username,ipaddress,password" > "$CSV_FILE"
echo "$username,$ipaddress,$password" >> "$CSV_FILE"

echo "Saved changes to $CSV_FILE."

chmod +x run.sh

echo "To run the software execute run.sh"
