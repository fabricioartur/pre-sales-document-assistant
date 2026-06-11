from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


class ConfigError(RuntimeError):
    """Raised when required runtime configuration is missing."""


MODEL_CHOICES: dict[str, str] = {
    "gpt-5.4-mini": "Fast, cost-efficient ($0.75/$4.50 per MTok). Best default for routine RFP analysis.",
    "gpt-5.4":      "High quality ($2.50/$15 per MTok). Use for complex enterprise tenders or final reports.",
    "gpt-5.5":      "Frontier model ($5/$30 per MTok). Best for strategic accounts and board-level deliverables.",
}

DEFAULT_MODEL = "gpt-5.4-mini"

REASONING_CHOICES = ("low", "medium", "high", "extra_high")


@dataclass(frozen=True)
class AppConfig:
    provider: str
    api_key: str | None
    model: str
    reasoning_effort: str | None = None

    @classmethod
    def from_env(
        cls,
        *,
        provider_override: str | None = None,
        model_override: str | None = None,
        reasoning_override: str | None = None,
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

        model = model_override or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL
        if provider == "openai" and model not in MODEL_CHOICES:
            valid = ", ".join(MODEL_CHOICES)
            raise ConfigError(f"Unknown model '{model}'. Supported models: {valid}.")

        if reasoning_override is not None and reasoning_override not in REASONING_CHOICES:
            valid_r = ", ".join(REASONING_CHOICES)
            raise ConfigError(
                f"Unknown reasoning effort '{reasoning_override}'. Valid options: {valid_r}."
            )

        return cls(provider=provider, api_key=api_key, model=model, reasoning_effort=reasoning_override)
