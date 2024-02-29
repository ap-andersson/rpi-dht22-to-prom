#!/usr/bin/env python3

import Adafruit_DHT
import time
import logging

from prometheus_client import Gauge, start_http_server
from systemd.journal import JournalHandler

# Setup logging to the Systemd Journal
log = logging.getLogger('dht22_sensor')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

# Create Prometheus gauges for humidity and temperature in
# Celsius and Fahrenheit
gh = Gauge('dht22_humidity_percent', 'Humidity percentage measured by the DHT22 Sensor')
gt = Gauge('dht22_temperature', 'Temperature measured by the DHT22 Sensor')

READ_INTERVAL = 10 #seconds
SENSOR = Adafruit_DHT.DHT22
PIN = 4

def main():

    # Expose metrics
    metrics_port = 8000
    start_http_server(metrics_port)
    print("Serving sensor metrics on :{}".format(metrics_port))
    log.info("Serving sensor metrics on :{}".format(metrics_port))

    while True:

        try:
            humidity, temperature = Adafruit_DHT.read_retry(SENSOR,PIN)

            if humidity is not None and temperature is not None:
                # Update the gauge with the sensor data
                print("Temp:{0:0.1f}*C, Humidity: {1:0.1f}%".format(temperature, humidity))
                log.info("Temp:{0:0.1f}*C, Humidity: {1:0.1f}%".format(temperature, humidity))
                gh.set(humidity)
                gt.set(temperature)
            else:
                log.info("None values, skipping")
                print("None values, skipping")

        except RuntimeError as e:
            print("RuntimeError: {}".format(e))
            log.error("RuntimeError: {}".format(e))

        time.sleep(READ_INTERVAL)

if __name__ == "__main__":
    main()