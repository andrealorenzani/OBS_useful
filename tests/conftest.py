"""Shared pytest fixtures.

Every test gets an isolated temporary data directory (Testing information:
"Persistence isolation") and a freshly reset in-memory ScreenState /
ConnectionManager, so nothing leaks between tests or between test runs and a
real ``data/`` directory.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from obs_director import config
from obs_director import state as state_module
from obs_director.app import app as fastapi_app


@pytest.fixture
def data_dir(tmp_path, monkeypatch):
    directory = tmp_path / "data"
    directory.mkdir()
    monkeypatch.setattr(config.settings, "data_dir", directory)
    return directory


@pytest.fixture(autouse=True)
def _reset_live_state():
    state_module.reset_state()
    state_module.manager.active = []
    yield
    state_module.reset_state()
    state_module.manager.active = []


@pytest.fixture
def client(data_dir):
    with TestClient(fastapi_app) as test_client:
        yield test_client
