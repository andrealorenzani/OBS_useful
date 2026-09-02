"""Entry point: run with `python main.py` (or `uvicorn obs_director.app:app`)."""

import uvicorn

from obs_director.config import settings


def main() -> None:
    uvicorn.run("obs_director.app:app", host=settings.host, port=settings.port, reload=False)


if __name__ == "__main__":
    main()
