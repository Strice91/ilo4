from time import sleep
from socket import gaierror
from enum import Enum
from paho.mqtt.client import Client, WebsocketConnectionError

from ilo4.config import settings
from ilo4.log import logger


class MQTTStatusCode(Enum):
    SUCCESS = 0
    UNACCEPTABLE_PROTOCOL_VERSION = 1
    IDENTIFIER_REJECTED = 2
    SERVER_UNAVAILABLE = 3
    BAD_USERNAME_OR_PASSWORD = 4
    NOT_AUTHORIZED = 5
    UNKNOWN = -1

    def describe(self):
        """Return a human-readable explanation of the status code."""
        descriptions = {
            self.SUCCESS: "Connection accepted.",
            self.UNACCEPTABLE_PROTOCOL_VERSION: "Connection refused: unacceptable protocol version.",
            self.IDENTIFIER_REJECTED: "Connection refused: client identifier not valid.",
            self.SERVER_UNAVAILABLE: "Connection refused: server unavailable.",
            self.BAD_USERNAME_OR_PASSWORD: "Connection refused: bad username or password.",
            self.NOT_AUTHORIZED: "Connection refused: not authorized.",
            self.UNKNOWN: "Unknown return code.",
        }
        return descriptions.get(self, "Unknown return code.")
    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

    

class MQTTClient:
    def __init__(self, url: str | None = None, port: int | None = None, keepalive: int | None = None, **kwargs):
        self.broker = url or settings.mqtt.url
        self.port = port or settings.mqtt.port
        self.keepalive = keepalive or settings.mqtt.keepalive
        self.delay = settings.mqtt.delay
        self.client_id = settings.mqtt.client_id

        if settings.mqtt.websocket:
            self._client = Client(client_id=self.client_id, transport="websockets")
            self._client.ws_set_options(path="/")
            self._client.tls_set()
        else:
            self._client = Client(client_id=self.client_id)

        if settings.mqtt.get("user") is not None and settings.mqtt.get("password") is not None:
            self._client.username_pw_set(settings.mqtt.user, settings.mqtt.password)

        self._client.on_connect = self._on_connect

    def connect(self):
        try:
            self._client.connect(self.broker, self.port, self.keepalive)
            self._client.loop_start()
            i = 0
            while not self._client.is_connected() and i < 10: 
                sleep(1)
                i += 1
            self._client.loop_stop()

            logger.info(f"Connected to MQTT broker {self.broker}:{self.port}")
            if self.client_id is not None:
                logger.info(f"Client ID: {self.client_id}")
        except (ConnectionRefusedError, OSError) as e:
            logger.error(f"Failed to connect to MQTT broker {self.broker}:{self.port} - {e}")
        except (WebsocketConnectionError, gaierror) as e:
            logger.error(f"Websocket Connection Error to MQTT broker {self.broker}:{self.port} - {e}")

    def _on_connect(self, client, userdata, flags, rc):
        status = MQTTStatusCode(rc)
        if status == MQTTStatusCode.SUCCESS:
            logger.info(f"Connected with result code {rc}: {status.describe()}")
        else:
            logger.error(f"Failed to connect with result code {rc}: {status.describe()}")
            

    def publish(self, topic: str, payload: str):
        sleep(self.delay)
        full_topic = topic if settings.mqtt.base_topic is None else f"{settings.mqtt.base_topic}/{topic}"
        self._client.publish(full_topic, payload)
        logger.info(f"Publishing '{full_topic}': '{payload}'")

    def disconnect(self):
        self._client.disconnect()
        logger.info(f"Disconnected from MQTT broker {self.broker}:{self.port}")

    def is_connected(self):
        return self._client.is_connected()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()


if __name__ == "__main__":
    with MQTTClient() as mqtt_client:
        mqtt_client.publish("test", "hello world")
