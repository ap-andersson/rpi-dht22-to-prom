# rpi-dht22-to-prom

Simple python script to get temperature and humidity from a DHT22 sensor and publish as a prometheus metrics endpoint.

## Python pre-reqs
Following needs to be run for the script to work:

```
sudo apt install python3 python3-pip libsystemd-dev
sudo pip3 install Adafruit_DHT
sudo pip3 install systemd-python
sudo pip3 install gpiozero

# Testrun with:
python3 collect-temp.py
```


## Creating service to autostart script on boot
sudo nano /etc/systemd/system/collect-temperature.service 

You need to set the correct WorkingDirectory, otherwise its good to go with the following content:

```
[Unit]
Description=A script for collecting temperature and publish for prometheus scraper
After=syslog.target network.target

[Service]
WorkingDirectory=/home/<username>
ExecStart=/bin/python3 collect-temp.py

Restart=always
RestartSec=120

[Install]
WantedBy=multi-user.target
```

sudo systemctl daemon-reload 

sudo service collect-temperature start 

Enable at boot:
sudo systemctl enable collect-temperature

Should start at boot.