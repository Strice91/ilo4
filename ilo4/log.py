import logging
from logging.handlers import RotatingFileHandler

from ilo4.config import settings

log_size_byte = 1024 * int(settings.logging.size_kb)

logger = logging.getLogger(__name__)
file_handler = RotatingFileHandler(
    settings.logging.file,
    maxBytes=log_size_byte,
    backupCount=5,
)
formatter = logging.Formatter("%(asctime)s : %(levelname)-8s [%(filename)-13s:%(lineno)-3d] %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(getattr(logging, settings.logging.level))
