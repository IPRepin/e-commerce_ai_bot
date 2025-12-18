import logging

from src.config.config import settings as cfg


def setup_logging() -> None:
    log_level = getattr(logging, cfg.logging.LOGGER_LEVEL, logging.INFO)

    logging.basicConfig(
        filename=f"{cfg.logging.LOGS_DIR}/chat_session.log",
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
        encoding="utf-8"
    )


setup_logging()
logger = logging.getLogger(__name__)