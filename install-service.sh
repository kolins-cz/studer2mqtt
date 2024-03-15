#!/bin/bash

# Create a systemd service file
cat <<EOF > /etc/systemd/system/studer2mqtt.service
[Unit]
Description=Studer2MQTT Service
After=network.target

[Service]
ExecStart=python $(pwd)/studer2mqtt.py
WorkingDirectory=$(pwd)
Restart=always
User=${SUDO_USER}


[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon
systemctl daemon-reload

# Enable and start the service
systemctl enable studer2mqtt.service
systemctl start studer2mqtt.service