# config/logging_config.py

import logging
import sys
from config.settings import LOG_LEVEL

def setup_logging():
    """Set up application-wide logging."""
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Optional: suppress noisy loggers
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.INFO)
