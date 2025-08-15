#!/usr/local/bin/python3
from ilo4.api import APIClient
from ilo4.mqtt import MQTTClient
from ilo4.data import extract_temperatures

from ilo4.log import logger


def main():
    with APIClient() as api_client:
        if not api_client.is_connected():
            logger.error("API client is not connected. Aborting... ")
            return
        temperatures = extract_temperatures(api_client)

    with MQTTClient() as mqtt_client:
        if not mqtt_client.is_connected():
            logger.error("MQTT client is not connected. Aborting... ")
            return
        for temp in temperatures:
            mqtt_client.publish(temp.name, str(temp.value))

        if any([temp.is_fatal() for temp in temperatures]):
            mqtt_client.publish("temperature", "FATAL")
        elif any([temp.is_critical() for temp in temperatures]):
            mqtt_client.publish("temperature", "CRITICAL")
        else:
            mqtt_client.publish("temperature", "OK")


if __name__ == "__main__":
    main()
