import os
import subprocess
from pathlib import Path

from fastapi import FastAPI

from tada.src.api.v1.endpoints import router
from tada.src.middlewares import LogMiddleware

app = FastAPI()

# Include all routes
app.include_router(router=router, prefix="/v1")

# Add all middlewares
app.add_middleware(LogMiddleware)


# Running the app in standalone mode (python package)
def run():
    script_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
    os.chdir(script_dir)

    script_path = "scripts/start"
    alembic_config_path = "alembic/alembic.ini"

    subprocess.run([script_path, alembic_config_path])  # noqa
