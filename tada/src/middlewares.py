import logging
import logging.config
from datetime import datetime
from pathlib import Path

from fastapi import Request

# setup loggers
LOGGING_CONFIG = Path(__file__).parent / "logging.ini"
logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)


class LogMiddleware:
    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)

    async def __call__(self, request: Request, *args, **kwargs):
        start_time = datetime.utcnow()
        response = await self.app(request, *args, **kwargs)
        end_time = datetime.utcnow()
        self.logger.info(
            f"Method: {request.get('method')}, "
            f"URL: {request.get('path')}, "
            f"Start Time: {start_time}, "
            f"End Time: {end_time}"
        )
        return response
