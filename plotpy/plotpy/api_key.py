"""Provider-agnostic LLM client setup.

Mirror of PlotR's ``R/api_key.R``.  The key insight is that the OpenAI Python
SDK speaks the **Chat Completions** wire format that every modern provider
(Groq, OpenAI, Together, Fireworks, Ollama, vLLM, etc.) implements.  So the
same client code works against any of them — you just change ``base_url``.

Three env vars drive the client:

    PLOTPY_API_KEY    required
    PLOTPY_BASE_URL   default: https://api.groq.com/openai/v1
    PLOTPY_MODEL      default: llama-3.3-70b-versatile

Programmatic override via :func:`set_key` is always available — it writes
back to the process environment so subsequent :func:`get_client` calls pick
it up.  ``python-dotenv`` is loaded on import; users only need a ``.env``
file alongside their notebook.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI

# Load .env once on package import; safe if missing.
load_dotenv(override=False)

_DEFAULT_BASE_URL = "https://api.groq.com/openai/v1"
_DEFAULT_MODEL = "llama-3.3-70b-versatile"


@dataclass(frozen=True)
class ClientConfig:
    """Resolved LLM client settings, surfaced for debugging."""

    api_key: str
    base_url: str
    model: str


def set_key(key: str, base_url: str | None = None, model: str | None = None) -> None:
    """Set credentials for the current process.

    Writes to ``os.environ`` so subsequent :func:`get_client` calls (and any
    in-process libraries that read those vars) see the new values.  Pass
    ``base_url`` and ``model`` to switch providers without touching the
    ``.env`` file.

    Parameters
    ----------
    key
        The provider's API key.
    base_url
        OpenAI-compatible endpoint.  Defaults to Groq.
    model
        Model identifier valid for ``base_url``.

    Examples
    --------
    >>> set_key("sk-...", base_url="https://api.openai.com/v1", model="gpt-4o-mini")
    """
    os.environ["PLOTPY_API_KEY"] = key
    if base_url is not None:
        os.environ["PLOTPY_BASE_URL"] = base_url
    if model is not None:
        os.environ["PLOTPY_MODEL"] = model


def get_key() -> str:
    """Return ``PLOTPY_API_KEY`` or raise a friendly error if missing."""
    key = os.environ.get("PLOTPY_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "PLOTPY_API_KEY is not set. Either call plotpy.set_key('...') or add a "
            ".env file with PLOTPY_API_KEY=... in your project."
        )
    return key


def get_config() -> ClientConfig:
    """Resolve current settings into a frozen :class:`ClientConfig`."""
    return ClientConfig(
        api_key=get_key(),
        base_url=os.environ.get("PLOTPY_BASE_URL", _DEFAULT_BASE_URL).strip(),
        model=os.environ.get("PLOTPY_MODEL", _DEFAULT_MODEL).strip(),
    )


def get_client() -> OpenAI:
    """Build a configured :class:`openai.OpenAI` client.

    Returns a fresh instance every call — cheap to construct and avoids
    cross-thread state.  Provider switching is automatic via ``base_url``.
    """
    cfg = get_config()
    return OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)
