from ilo4.config import settings
from redfish.rest.v1 import HttpClient

from ilo4.log import logger


class System:
    def __init__(self, item: dict):
        try:
            self.status = item["Status"]["Health"]
            self.name = item["HostName"]
        except KeyError as e:
            logger.error(f"Cloud not extract System Information! - KeyError: {e}")
            self.name = "UNKNOWN"
            self.status = "UNKNOWN"

    def is_healthy(self) -> bool:
        return self.status == "OK"


class Temperature:
    def __init__(self, item: dict):
        self.name = item["Name"]
        self.value = item["ReadingCelsius"]
        self.critical = item["UpperThresholdCritical"]
        self.fatal = item["UpperThresholdFatal"]

    def is_critical(self) -> bool:
        return self.critical > 0 and self.value > self.critical

    def is_fatal(self) -> bool:
        return self.fatal > 0 and self.value > self.fatal

    def __repr__(self) -> str:
        return f"Temperature '{self.name}': {self.value}°C"

    def __str__(self) -> str:
        return f"'{self.name}': {self.value}°C"


def extract_temperatures(client: HttpClient) -> list[Temperature]:
    response = client.get(settings.ilo.temperature.path)
    temperatures = []
    for item in response.get("Temperatures", []):
        t = Temperature(item)
        if t.name in settings.ilo.temperature.exclude:
            continue
        temperatures.append(t)
    if (n := len(temperatures)) > 0:
        logger.info(f"Successfully extracted {n} temperature values.")
    else:
        logger.warning("No temperatures could be extracted!")
    return temperatures


def extract_system(client: HttpClient) -> System:
    response = client.get(settings.ilo.system.path)
    return System(response)
