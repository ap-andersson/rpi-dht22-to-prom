#!/usr/bin/env python3

import Adafruit_DHT
import time

from prometheus_client import Gauge, start_http_server
from gpiozero import CPUTemperature

# Create Prometheus gauges for humidity and temperature in
# Celsius and Fahrenheit
gh = Gauge('dht22_humidity_percent', 'Humidity percentage measured by the DHT22 Sensor')
gt = Gauge('dht22_temperature', 'Temperature measured by the DHT22 Sensor')
ct = Gauge('cpu_temp', 'RPI CPU Temp')

READ_INTERVAL = 10 #seconds
SENSOR = Adafruit_DHT.DHT22
PIN = 4

def main():

    # Expose metrics
    metrics_port = 8000
    start_http_server(metrics_port)
    print("Serving sensor metrics on :{}".format(metrics_port))

    while True:

        try:
            humidity, temperature = Adafruit_DHT.read_retry(SENSOR,PIN)
            cpu_temp = CPUTemperature().temperature

            if humidity is not None and temperature is not None:
                # Update the gauge with the sensor data
                print("Temp:{0:0.1f}*C, Humidity: {1:0.1f}%, CPU Temp: {2:0.1f}*C".format(temperature, humidity, cpu_temp))
                gh.set(humidity)
                gt.set(temperature)
                ct.set(cpu_temp)
            else:
                print("None values, skipping")

        except RuntimeError as e:
            print("RuntimeError: {}".format(e))

        time.sleep(READ_INTERVAL)

if __name__ == "__main__":
    main()
