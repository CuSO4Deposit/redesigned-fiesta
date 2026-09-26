from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

from . import projections
from .config import Config
from .render import write_json


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build(root: Path) -> None:
    """Deterministic: no clock beyond this local one, no network, no secrets."""
    config = Config.from_env(root)
    now = datetime.now(UTC)
    data_dir = root / "data"

    sources: list[dict[str, object]] = []
    for name, projection in (("rhythm", projections.rhythm),):
        result = projection.build(config, now)
        if result is None:
            (data_dir / f"{name}.json").unlink(missing_ok=True)
        else:
            write_json(data_dir / f"{name}.json", result)
            sources.append(result)

    write_json(
        data_dir / "meta.json",
        projections.meta.build(
            now,
            config.embargo_days,
            [str(source["through"]) for source in sources],
        ),
    )


def translate(root: Path) -> None:
    raise SystemExit("pipeline: translate is not implemented yet")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="pipeline")
    parser.add_argument("command", choices=["build", "translate"])
    args = parser.parse_args(argv)
    root = project_root()
    if args.command == "build":
        build(root)
    else:
        translate(root)
