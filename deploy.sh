#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Update and upgrade the system
sudo apt update && sudo apt upgrade -y

# Install necessary packages
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create necessary directories for certbot
mkdir -p certbot/conf certbot/www

# Make the init-letsencrypt.sh script executable
chmod +x init-letsencrypt.sh

# Start the initial SSL certificate setup
./init-letsencrypt.sh

# Start the Docker containers
docker compose up -d

echo "Setup complete! Your application should now be running at https://smu.bchwy.com" 