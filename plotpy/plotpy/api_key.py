"""Legacy credential helpers — thin shim over :mod:`plotpy.providers`.

The provider layer (:mod:`plotpy.providers`) is now the source of truth for
"which model am I talking to."  This module stays so existing notebooks and
the README's ``plotpy.set_key(...)`` / ``.env`` flow keep working unchanged:

    PLOTPY_API_KEY    required (unless you built a Chat explicitly)
    PLOTPY_BASE_URL   default: https://api.groq.com/openai/v1
    PLOTPY_MODEL      default: llama-3.3-70b-versatile

New code should prefer the ellmer-style constructors instead::

    plotpy.use(plotpy.chat_groq())                 # or chat_openai(), chat_anthropic() …
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from .providers import PROVIDERS, Chat, get_active, use

_DEFAULT_BASE_URL = PROVIDERS["groq"].base_url
_DEFAULT_MODEL = PROVIDERS["groq"].default_model


@dataclass(frozen=True)
class ClientConfig:
    """Resolved LLM client settings, surfaced for debugging."""

    api_key: str
    base_url: str
    model: str


def set_key(key: str, base_url: str | None = None, model: str | None = None) -> None:
    """Set credentials for the current process and make them the active model.

    Writes to ``os.environ`` (so anything reading ``PLOTPY_*`` sees them) *and*
    installs a matching active :class:`~plotpy.providers.Chat`, so a following
    bare ``plotpy.ask(...)`` uses exactly these settings.

    >>> set_key("sk-...", base_url="https://api.openai.com/v1", model="gpt-4o-mini")
    """
    os.environ["PLOTPY_API_KEY"] = key
    resolved_base = base_url or os.environ.get("PLOTPY_BASE_URL", _DEFAULT_BASE_URL)
    resolved_model = model or os.environ.get("PLOTPY_MODEL", _DEFAULT_MODEL)
    if base_url is not None:
        os.environ["PLOTPY_BASE_URL"] = base_url
    if model is not None:
        os.environ["PLOTPY_MODEL"] = model
    use(Chat(provider="legacy", model=resolved_model, api_key=key, base_url=resolved_base))


def get_key() -> str:
    """Return ``PLOTPY_API_KEY`` or raise a friendly error if missing."""
    key = os.environ.get("PLOTPY_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "PLOTPY_API_KEY is not set. Either call plotpy.set_key('...'), build a "
            "Chat with plotpy.chat_openai(api_key=...), or add a .env file."
        )
    return key


def get_config() -> ClientConfig:
    """Resolve the active model into a frozen :class:`ClientConfig`."""
    c = get_active()
    return ClientConfig(api_key=c.api_key, base_url=c.base_url, model=c.model)


def get_client():
    """Return the raw ``openai.OpenAI`` client behind the active model."""
    return get_active()._get_client()
