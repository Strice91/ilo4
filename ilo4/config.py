import importlib.resources as res

from dynaconf import Dynaconf, Validator

PACKAGE_ROOT = res.files("ilo4")
PROJECT_ROOT = PACKAGE_ROOT.parent
CONFIG_ROOT = PROJECT_ROOT / "config"

settings = Dynaconf(
    envvar_prefix="ILO4",
    merge_enabled=True,
    load_dotenv=False,
    root_path=CONFIG_ROOT,
    settings_files=["settings.toml", ".secrets.toml"],
    validators=[
        Validator("ilo.url", must_exist=True),
        Validator("ilo.user", must_exist=True),
        Validator("ilo.password", must_exist=True),
        Validator("ilo.poll_interval", default=5),
        Validator("ilo.temperature.path", must_exist=True),
        Validator("ilo.temperature.exclude", default=[]),
        Validator("ilo.system.path", must_exist=True),
        Validator("mqtt.url", must_exist=True),
        Validator("mqtt.port", default=1883),
        Validator("mqtt.keepalive", default=60, cast=int),
        Validator("mqtt.client_id", default=None),
        Validator("mqtt.user"),
        Validator("mqtt.password"),
        Validator("mqtt.delay", default=1),
        Validator("mqtt.base_topic", default=None),
        Validator("mqtt.websocket", default=False, cast=bool),
        Validator("logging.stream", default=True, cast=bool),
        Validator("logging.file", default=False, cast=bool),
        Validator("logging.path", default="config/ilo4.log"),
        Validator("logging.level", default="INFO"),
        Validator("logging.size_kb", default=500, cast=int),
    ],
)
settings.validators.validate()
