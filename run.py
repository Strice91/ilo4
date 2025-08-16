#!/usr/local/bin/python3
from ilo4.api import APIClient
from ilo4.mqtt import MQTTClient
from ilo4.data import extract_temperatures

from ilo4.log import logger
from ilo4.config import settings

import signal
import threading
import sys
from time import sleep
from datetime import datetime, timedelta

shutdown_event = threading.Event()


def task():
    logger.info("Polling API and Pushing to MQTT ...")
    with APIClient() as api_client:
        if not api_client.is_connected():
            logger.error("API client is not connected.")
        temperatures = extract_temperatures(api_client)

    with MQTTClient() as mqtt_client:
        if not mqtt_client.is_connected():
            logger.error("MQTT client is not connected. Retrying")
            schedule_task()
            return

        for temp in temperatures:
            mqtt_client.publish(temp.name, str(temp.value))

        if not temperatures:
            mqtt_client.publish("temperature", "UNKONWN")
        elif any([temp.is_fatal() for temp in temperatures]):
            mqtt_client.publish("temperature", "FATAL")
        elif any([temp.is_critical() for temp in temperatures]):
            mqtt_client.publish("temperature", "CRITICAL")
        else:
            mqtt_client.publish("temperature", "OK")

    schedule_task()


def schedule_task():
    if not shutdown_event.is_set():
        interval = settings.ilo.poll_interval * 60
        # Reschedule the timer only if not shutting down
        logger.info(f"Next try at {datetime.now() + timedelta(seconds=interval)}")
        timer = threading.Timer(interval, task)
        timer.daemon = True
        timer.start()


def handle_shutdown(signum, frame):
    logger.info(f"Shutdown signal {signum} received. Cleaning up...")
    shutdown_event.set()
    # sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_shutdown)  # Docker
    signal.signal(signal.SIGINT, handle_shutdown)  # Ctrl+C

    # Start the main task and timer
    logger.info("Starting iLO4 Event Loop")
    logger.info("Poll Interval: %smin", settings.ilo.poll_interval)
    schedule_task()

    # Keep the process alive, but responsive to shutdown_event
    try:
        while not shutdown_event.is_set():
            sleep(5)
    except KeyboardInterrupt:
        handle_shutdown(signal.SIGINT, None)
