"""Community-message provider abstraction (Deep Dive Q2): v1 ships no
concrete provider — search always returns an empty list, without erroring,
for any platform."""

from __future__ import annotations

import pytest

from obs_director.providers import MessageProvider, get_provider
from obs_director.providers.manual import NoOpProvider


@pytest.mark.parametrize("platform", ["x", "discord", "facebook", "whatsapp", "some-future-platform"])
def test_get_provider_always_returns_a_provider_that_returns_no_results(platform):
    provider = get_provider(platform)
    assert isinstance(provider, MessageProvider)
    assert provider.search("anything") == []


def test_no_op_provider_does_not_error_on_empty_query():
    provider = NoOpProvider()
    assert provider.search("") == []
