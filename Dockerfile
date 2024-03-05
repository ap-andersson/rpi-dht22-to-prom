FROM python:3.8-slim-buster

WORKDIR /app

RUN apt update
RUN apt install -y python3 python3-pip rpi.gpio-common
RUN pip3 install Adafruit_DHT
RUN pip3 install gpiozero
RUN pip3 install prometheus_client requests
RUN pip3 install rpi.gpio

RUN usermod -a -G dialout root

COPY collect-temp-dock.py .

EXPOSE 8000

CMD ["python3", "-u", "collect-temp-dock.py", "80"]