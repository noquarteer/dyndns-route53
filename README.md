## R53 Record updater

This script was created to avoid dynamic dns configurations for a PC I was using to host an application visible for the internet.

It's supossed to be running in a crontab with some parameters:

> python3 main.py <AWS_ACCESS_KEY_ID> <AWS_SECRET_ACCESS_KEY> <A_RECORD_TO_UPDATE> <HOSTED_ZONE_ID>

To install it, just clone this repo and install the dependencies before running it:

> pip3 install -r requirements.txt

Feel free to open a pull request to improve this very basic script. 

Godspeed. 