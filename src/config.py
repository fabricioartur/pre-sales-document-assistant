from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


class ConfigError(RuntimeError):
    """Raised when required runtime configuration is missing."""


@dataclass(frozen=True)
class AppConfig:
    provider: str
    api_key: str | None
    model: str

    @classmethod
    def from_env(
        cls,
        *,
        provider_override: str | None = None,
        model_override: str | None = None,
    ) -> "AppConfig":
        if load_dotenv is not None:
            load_dotenv()

        provider = (
            provider_override or os.getenv("ANALYSIS_PROVIDER") or "mock"
        ).strip().lower()
        if provider not in {"mock", "openai"}:
            raise ConfigError("ANALYSIS_PROVIDER must be either 'mock' or 'openai'.")

        api_key = os.getenv("OPENAI_API_KEY")
        if provider == "openai" and not api_key:
            raise ConfigError(
                "OPENAI_API_KEY is required when the openai provider is selected."
            )

        model = model_override or os.getenv("OPENAI_MODEL") or "gpt-4.1-mini"
        return cls(provider=provider, api_key=api_key, model=model)
