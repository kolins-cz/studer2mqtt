#!/bin/bash

# Restart studer2mqtt service
sudo systemctl restart studer2mqtt

# Show output of studer2mqtt service
sudo journalctl -u studer2mqtt -f