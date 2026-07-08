"""Multi-provider LLM layer — PlotPy's answer to R's ``ellmer``.

``ellmer`` gives R users one constructor per provider (``chat_openai()``,
``chat_claude()``, ``chat_ollama()`` …) that all return the same ``Chat``
object, so you can swap the model behind your code at any moment.  This module
is the Python mirror of that idea.

The trick that makes it small: every modern provider speaks the OpenAI
**Chat Completions** wire format, either natively (OpenAI, Groq, Together,
Fireworks, Ollama, vLLM) or through an official compatibility endpoint
(Anthropic, Google Gemini).  So one :class:`Chat` wrapping ``openai.OpenAI``
with the right ``base_url`` serves them all.

Quickstart
----------
>>> import plotpy
>>> from plotpy import chat_groq, chat_openai, chat_anthropic
>>> plotpy.use(chat_groq())                       # free default
>>> plotpy.use(chat_openai(model="gpt-4o-mini"))  # switch any time
>>> res = plotpy.ask(df, "interactive GWAS Manhattan", llm=chat_anthropic())

Every constructor resolves its API key from (in order): the ``api_key``
argument, the provider's conventional env var (``OPENAI_API_KEY`` …), then the
generic ``PLOTPY_API_KEY``.  Local servers (Ollama, vLLM) need no key.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from dotenv import load_dotenv

# Load .env once on import; harmless if absent.
load_dotenv(override=False)


# --------------------------------------------------------------------- registry
@dataclass(frozen=True)
class ProviderSpec:
    """Static facts about a provider: where it lives and how to auth."""

    name: str
    base_url: str
    default_model: str
    key_env: tuple[str, ...] = ()          # env vars tried in order for the key
    key_optional: bool = False             # True for local servers (Ollama/vLLM)


# base_urls are the providers' OpenAI-compatible endpoints. Anthropic's and
# Google's compat endpoints are documented but younger than the native APIs —
# override base_url if a provider moves it.
PROVIDERS: dict[str, ProviderSpec] = {
    "groq": ProviderSpec(
        "groq", "https://api.groq.com/openai/v1", "llama-3.3-70b-versatile",
        ("GROQ_API_KEY", "PLOTPY_API_KEY"),
    ),
    "openai": ProviderSpec(
        "openai", "https://api.openai.com/v1", "gpt-4o-mini",
        ("OPENAI_API_KEY", "PLOTPY_API_KEY"),
    ),
    "anthropic": ProviderSpec(
        "anthropic", "https://api.anthropic.com/v1/", "claude-3-5-sonnet-latest",
        ("ANTHROPIC_API_KEY", "PLOTPY_API_KEY"),
    ),
    "google": ProviderSpec(
        "google", "https://generativelanguage.googleapis.com/v1beta/openai/",
        "gemini-1.5-flash", ("GEMINI_API_KEY", "GOOGLE_API_KEY", "PLOTPY_API_KEY"),
    ),
    "together": ProviderSpec(
        "together", "https://api.together.xyz/v1",
        "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        ("TOGETHER_API_KEY", "PLOTPY_API_KEY"),
    ),
    "fireworks": ProviderSpec(
        "fireworks", "https://api.fireworks.ai/inference/v1",
        "accounts/fireworks/models/llama-v3p3-70b-instruct",
        ("FIREWORKS_API_KEY", "PLOTPY_API_KEY"),
    ),
    "ollama": ProviderSpec(
        "ollama", "http://localhost:11434/v1", "llama3.1",
        (), key_optional=True,
    ),
    "vllm": ProviderSpec(
        "vllm", "http://localhost:8000/v1", "",
        (), key_optional=True,
    ),
}


def _resolve_key(spec: ProviderSpec, api_key: str | None) -> str:
    if api_key:
        return api_key
    for var in spec.key_env:
        val = os.environ.get(var, "").strip()
        if val:
            return val
    if spec.key_optional:
        return "not-needed"  # local servers ignore the key but the SDK wants a string
    raise RuntimeError(
        f"No API key for provider {spec.name!r}. Pass api_key=..., or set one of "
        f"{', '.join(spec.key_env)} (or the generic PLOTPY_API_KEY)."
    )


# ------------------------------------------------------------------- Chat object
@dataclass
class Chat:
    """A configured connection to one model — the unit you pass around and swap.

    Duck-typed on :meth:`complete`; anything with the same signature (e.g. the
    ``MockChat`` used in the tests) works everywhere a ``Chat`` does.

    Attributes
    ----------
    provider, model, base_url
        Identify the endpoint; shown by ``repr`` so a notebook can confirm which
        model is live after a :func:`use` swap.
    temperature
        Default sampling temperature; per-call ``complete(temperature=...)`` wins.
    """

    provider: str
    model: str
    api_key: str = field(repr=False, default="")
    base_url: str = ""
    temperature: float = 0.0
    extra: dict[str, Any] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        self._client: Any | None = None

    def _get_client(self) -> Any:
        if self._client is None:
            from openai import OpenAI

            self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        return self._client

    def complete(
        self,
        messages: list[dict[str, str]],
        temperature: float | None = None,
        json_mode: bool = False,
    ) -> str:
        """Send ``messages`` and return the assistant's text.

        ``json_mode`` asks the provider to constrain output to a JSON object.
        Providers that don't support ``response_format`` are retried once
        without it, so the same call works everywhere.
        """
        client = self._get_client()
        temp = self.temperature if temperature is None else temperature
        kw: dict[str, Any] = {"model": self.model, "messages": messages,
                              "temperature": temp, **self.extra}
        if json_mode:
            kw["response_format"] = {"type": "json_object"}
        try:
            resp = client.chat.completions.create(**kw)
        except Exception:
            if json_mode:                       # provider rejected response_format
                kw.pop("response_format", None)
                resp = client.chat.completions.create(**kw)
            else:
                raise
        return resp.choices[0].message.content or ""

    def chat(self, prompt: str, system: str | None = None) -> str:
        """One-shot convenience mirroring ellmer's ``chat$chat()``."""
        msgs: list[dict[str, str]] = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.append({"role": "user", "content": prompt})
        return self.complete(msgs)


# ----------------------------------------------------------------- constructors
def chat(provider: str, model: str | None = None, *, api_key: str | None = None,
         base_url: str | None = None, temperature: float = 0.0, **extra: Any) -> Chat:
    """Generic constructor — ``chat("groq")``, ``chat("openai", "gpt-4o")``.

    The ``chat_<provider>`` helpers below are thin wrappers over this.
    """
    if provider not in PROVIDERS:
        raise KeyError(
            f"Unknown provider {provider!r}. Known: {', '.join(PROVIDERS)}. "
            "For anything else, pass base_url= to point at its OpenAI-compatible endpoint."
        )
    spec = PROVIDERS[provider]
    return Chat(
        provider=provider,
        model=(model or spec.default_model),
        api_key=_resolve_key(spec, api_key),
        base_url=(base_url or spec.base_url),
        temperature=temperature,
        extra=extra,
    )


def chat_groq(model: str | None = None, *, api_key: str | None = None, **kw: Any) -> Chat:
    """Groq — fast, free tier, the PlotPy default. Default ``llama-3.3-70b-versatile``."""
    return chat("groq", model, api_key=api_key, **kw)


def chat_openai(model: str | None = None, *, api_key: str | None = None, **kw: Any) -> Chat:
    """OpenAI. Default ``gpt-4o-mini`` — strong first-try codegen, needs a paid key."""
    return chat("openai", model, api_key=api_key, **kw)


def chat_anthropic(model: str | None = None, *, api_key: str | None = None, **kw: Any) -> Chat:
    """Anthropic Claude via its OpenAI-compatibility endpoint. Default ``claude-3-5-sonnet-latest``."""
    return chat("anthropic", model, api_key=api_key, **kw)


def chat_google(model: str | None = None, *, api_key: str | None = None, **kw: Any) -> Chat:
    """Google Gemini via its OpenAI-compatibility endpoint. Default ``gemini-1.5-flash``."""
    return chat("google", model, api_key=api_key, **kw)


def chat_together(model: str | None = None, *, api_key: str | None = None, **kw: Any) -> Chat:
    """Together AI. Default ``Meta-Llama-3.1-70B-Instruct-Turbo``."""
    return chat("together", model, api_key=api_key, **kw)


def chat_fireworks(model: str | None = None, *, api_key: str | None = None, **kw: Any) -> Chat:
    """Fireworks AI. Default ``llama-v3p3-70b-instruct``."""
    return chat("fireworks", model, api_key=api_key, **kw)


def chat_ollama(model: str | None = None, *, base_url: str | None = None, **kw: Any) -> Chat:
    """Local Ollama server — no API key. Default ``llama3.1``; pass any pulled model."""
    return chat("ollama", model, base_url=base_url, **kw)


def chat_vllm(model: str, *, base_url: str | None = None, **kw: Any) -> Chat:
    """Local/remote vLLM server — no API key. You must name the served ``model``."""
    return chat("vllm", model, base_url=base_url, **kw)


# ------------------------------------------------------------- global default
_ACTIVE: Chat | None = None


def use(chat_obj: Chat) -> Chat:
    """Make ``chat_obj`` the active model for bare ``plotpy.ask(...)`` calls.

    Switch as often as you like — this is the ellmer "swap the backend" move::

        plotpy.use(chat_openai(model="gpt-4o-mini"))
        plotpy.use(chat_groq())          # back to free
    """
    global _ACTIVE
    _ACTIVE = chat_obj
    return chat_obj


def get_active() -> Chat:
    """Return the active :class:`Chat`, lazily building the env/``set_key`` default.

    Back-compat: if nobody called :func:`use`, fall back to the legacy
    ``PLOTPY_BASE_URL`` / ``PLOTPY_MODEL`` / ``PLOTPY_API_KEY`` env trio so
    existing ``set_key(...)`` notebooks keep working unchanged.
    """
    global _ACTIVE
    if _ACTIVE is None:
        _ACTIVE = _from_legacy_env()
    return _ACTIVE


def _from_legacy_env() -> Chat:
    base_url = os.environ.get("PLOTPY_BASE_URL", PROVIDERS["groq"].base_url).strip()
    model = os.environ.get("PLOTPY_MODEL", PROVIDERS["groq"].default_model).strip()
    api_key = os.environ.get("PLOTPY_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "No active model. Call plotpy.use(plotpy.chat_groq()) (or another "
            "chat_* provider), or set PLOTPY_API_KEY / call plotpy.set_key('...')."
        )
    return Chat(provider="legacy", model=model, api_key=api_key, base_url=base_url)
