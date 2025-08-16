from time import sleep
from socket import gaierror

from paho.mqtt.client import Client, WebsocketConnectionError

from ilo4.config import settings
from ilo4.log import logger


class MQTTClient:
    def __init__(self, url: str | None = None, port: int | None = None, keepalive: int | None = None, **kwargs):
        self.broker = url or settings.mqtt.url
        self.port = port or settings.mqtt.port
        self.keepalive = keepalive or settings.mqtt.keepalive
        self.delay = settings.mqtt.delay
        if settings.mqtt.websocket:
            self._client = Client(transport="websockets")
            self._client.ws_set_options(path="/")
            self._client.tls_set()
        else:
            self._client = Client()
        self._client.username_pw_set(settings.mqtt.user, settings.mqtt.password)
        self._connected = False

    def connect(self):
        try:
            self._client.connect(self.broker, self.port, self.keepalive)
            self._connected = True
            logger.info(f"Connected to MQTT broker {self.broker}:{self.port}")
        except (ConnectionRefusedError, OSError) as e:
            logger.error(f"Failed to connect to MQTT broker {self.broker}:{self.port} - {e}")
        except (WebsocketConnectionError, gaierror) as e:
            logger.error(f"Websocket Connection Error to MQTT broker {self.broker}:{self.port} - {e}")

    def publish(self, topic: str, payload: str):
        sleep(self.delay)
        full_topic = topic if settings.mqtt.base_topic is None else f"{settings.mqtt.base_topic}/{topic}"
        self._client.publish(full_topic, payload)
        logger.info(f"Publishing '{full_topic}': '{payload}'")

    def disconnect(self):
        self._connected = False
        self._client.disconnect()
        logger.info(f"Disconnected from MQTT broker {self.broker}:{self.port}")

    def is_connected(self):
        return self._connected

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()


if __name__ == "__main__":
    with MQTTClient() as mqtt_client:
        mqtt_client.publish("test", "hello world")
