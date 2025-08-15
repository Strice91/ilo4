from ilo4.config import settings


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


def extract_temperatures(client) -> list[Temperature]:
    response = client.get(settings.ilo.temperature.path)
    temperatures = []
    for item in response["Temperatures"]:
        t = Temperature(item)
        if t.name in settings.ilo.temperature.exclude:
            continue
        temperatures.append(t)
    return temperatures
