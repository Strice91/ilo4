import redfish
from redfish.rest.v1 import RetriesExhaustedError, SessionCreationError

from ilo4.config import settings
from ilo4.log import logger


class APIClient:
    def __init__(self, url: str | None = None, user: str | None = None, password: str | None = None):
        self.user = user or settings.ilo.user
        self.password = password or settings.ilo.password
        self.url = url or settings.ilo.url
        self._connected = False
        self._client: redfish.redfish_client.RedfishClient

        try:
            self._client = redfish.redfish_client(
                base_url=self.url,
                username=self.user,
                password=self.password,
                default_prefix="/redfish/v1",
            )
            logger.info(f"Connected to ILO {self.url}")
        except RetriesExhaustedError as e:
            logger.error(f"Failed to connect to ILO {self.url} - {e}")

    def login(self):
        if self._client is None:
            return
        try:
            self._client.login(auth="session")
            self._connected = True
            logger.info("Login to ILO successful")
        except SessionCreationError as e:
            logger.error(f"Failed to login to ILO {self.url} - {e}")

    def logout(self):
        if self._client is None:
            return
        self._client.logout()
        self._connected = False
        logger.info(f"Disconnected from ILO {self.url}")

    def get(self, path: str, **kwargs) -> dict:
        return self._client.get(path, **kwargs).dict

    def is_connected(self):
        return self._connected

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.logout()


if __name__ == "__main__":
    with APIClient() as client:
        print(client.get("/redfish/v1/"))
