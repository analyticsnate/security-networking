# security-networking
This repository contains python and shell scripts that I wrote while exploring streaming data from my raspberry pi to my laptop.

# pi_hdd_check.py
This script checks the microSD card from the pi to see if a flag in custom_config is set to True. If so, this means the SD card has new data and log files ready to be transferred from to the laptop. The script then transfers all the files into the Interfaces directory and sets the flag to False.
In normal operation, this script is run every minute with a cron job.
>crontab -e to modify

# pi_load_sql.py
This script loads the data from the Interfaces folder to a mysql database
In normal operation, this script is run every 30 mins with a cron job.
