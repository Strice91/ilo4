#!/usr/local/bin/python3
from ilo4.api import APIClient
from ilo4.mqtt import MQTTClient
from ilo4.data import extract_temperatures

from ilo4.log import logger
from ilo4.config import settings

import signal
import threading
import sys
import time

# Global reference to the timer
timer = None
shutdown_event = threading.Event()


def task():
    logger.info("Polling API and Pushing to MQTT ...")
    with APIClient() as api_client:
        if not api_client.is_connected():
            logger.error("API client is not connected. Aborting!")
            return
        temperatures = extract_temperatures(api_client)

    with MQTTClient() as mqtt_client:
        if not mqtt_client.is_connected():
            logger.error("MQTT client is not connected. Aborting!")
            return
        for temp in temperatures:
            mqtt_client.publish(temp.name, str(temp.value))

        if any([temp.is_fatal() for temp in temperatures]):
            mqtt_client.publish("temperature", "FATAL")
        elif any([temp.is_critical() for temp in temperatures]):
            mqtt_client.publish("temperature", "CRITICAL")
        else:
            mqtt_client.publish("temperature", "OK")

    # Reschedule the timer only if not shutting down
    global timer
    timer = threading.Timer(settings.ilo.poll_interval * 60, task)
    timer.start()


def handle_shutdown(signum, frame):
    logger.info("Shutdown signal received. Cleaning up...")
    shutdown_event.set()

    global timer
    if timer:
        timer.cancel()
        logger.info("Timer cancelled.")

    sys.exit(0)


def main():
    signal.signal(signal.SIGTERM, handle_shutdown)  # Docker
    signal.signal(signal.SIGINT, handle_shutdown)  # Ctrl+C

    # Start the main task and timer
    logger.info("Starting iLO4 Event Loop")
    logger.info("Poll Interval: %smin", settings.ilo.poll_interval)
    task()

    # Keep the process alive, but responsive to shutdown_event
    try:
        while not shutdown_event.is_set():
            time.sleep(5)
    except KeyboardInterrupt:
        handle_shutdown(None, None)


if __name__ == "__main__":
    main()
