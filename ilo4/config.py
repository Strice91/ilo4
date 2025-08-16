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
        Validator("mqtt.url", must_exist=True),
        Validator("mqtt.port", default=1883),
        Validator("mqtt.topic", default="ilo4"),
        Validator("mqtt.keepalive", default=60),
        Validator("mqtt.user", must_exist=True),
        Validator("mqtt.password", must_exist=True),
        Validator("mqtt.delay", default=1),
        Validator("mqtt.base_topic", default=None),
        Validator("logging.file", default="config/ilo4.log"),
        Validator("logging.level", default="INFO"),
        Validator("logging.size_kb", default="1000"),
    ],
)
settings.validators.validate()
