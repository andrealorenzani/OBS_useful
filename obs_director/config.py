"""Runtime settings for OBS_director.

Kept intentionally tiny: a single local operator tool, configured via a
handful of environment variables with sane local defaults.
"""

from __future__ import annotations

import os
from pathlib import Path

# Repo root (this file lives at obs_director/config.py).
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    def __init__(self) -> None:
        self.data_dir: Path = Path(os.environ.get("OBS_DIRECTOR_DATA_DIR", str(BASE_DIR / "data")))
        self.host: str = os.environ.get("OBS_DIRECTOR_HOST", "0.0.0.0")
        self.port: int = int(os.environ.get("OBS_DIRECTOR_PORT", "8000"))


settings = Settings()
