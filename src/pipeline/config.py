"""Configuration, read once from the environment (and .env), failing loudly.

Same rule as the loaders: a parameter that is present but wrong should stop the
run, and a parameter that is absent and guessed is worse than a failure — the
guessed default renders as a plausible, wrong page. `build` needs no secrets and
touches no network; only `translate` reads `LLM_API_KEY`.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from .sanitize import DEFAULT_EMBARGO_DAYS


def die(message: str) -> None:
    sys.exit(f"pipeline: {message}")


def _int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        die(f"{name}={raw!r} is not an integer")


@dataclass(frozen=True)
class Config:
    root: Path
    embargo_days: int
    local_tz: str | None
    pipepipe_exports: str | None
    gadgetbridge_exports: str | None
    firefox_exports: str | None
    yoffline_db: str | None
    yoffline_user: str | None
    arcaea_charts: str | None
    pjsk_musics: str | None
    pjsk_difficulties: str | None
    cytus2_charts: str | None
    llm_api_key: str | None
    llm_base_url: str | None
    llm_model: str | None

    @classmethod
    def from_env(cls, root: Path) -> Config:
        env_file = root / ".env"
        if env_file.exists():
            load_dotenv(env_file)

        def get(name: str) -> str | None:
            return os.environ.get(name) or None

        return cls(
            root=root,
            embargo_days=_int("EMBARGO_DAYS", DEFAULT_EMBARGO_DAYS),
            local_tz=get("CPI_LOCAL_TZ"),
            pipepipe_exports=get("CPI_PIPEPIPE_EXPORTS"),
            gadgetbridge_exports=get("CPI_GADGETBRIDGE_EXPORTS"),
            firefox_exports=get("CPI_FIREFOX_EXPORTS"),
            yoffline_db=get("YOFFLINE_DB"),
            yoffline_user=get("YOFFLINE_USER"),
            arcaea_charts=get("ARCSONG_DB"),
            pjsk_musics=get("PJSK_MUSICS_JSON"),
            pjsk_difficulties=get("PJSK_DIFFICULTIES_JSON"),
            cytus2_charts=get("CYTUS2_CHARTS_JSON"),
            llm_api_key=get("LLM_API_KEY"),
            llm_base_url=get("LLM_BASE_URL") or "https://api.openai.com/v1",
            llm_model=get("LLM_MODEL") or "gpt-4o-mini",
        )
