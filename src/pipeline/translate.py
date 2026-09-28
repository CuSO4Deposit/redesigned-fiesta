"""Translate exported content pages to English, incrementally.

The Chinese pages under content/ are the source of truth (they come from
Logseq). This derives English siblings (`<name>.en.md`) and keeps a state file
so a run only redoes pages whose source actually changed.

State: `.translate-state.json`, mapping each source path to the content hash it
was translated from. A page is retranslated when its hash changes, when its
English file is missing, or when the prompt version is bumped. Pages whose
source disappeared have their English file removed. `--seed` records the current
hashes without calling the model, to adopt already-translated files. `--force`
retranslates everything.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

from .config import Config

PROMPT_VERSION = "v1"
STATE_NAME = ".translate-state.json"
CONTENT_DIR = "content"
EN_SUFFIX = ".en.md"

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

SYSTEM_LINES = (
    "You translate short strings into natural English. Translate each input "
    "line and output exactly one line per input line, in the same order, with "
    "no commentary and no extra lines."
)
SYSTEM_BODY = (
    "You translate Markdown into natural, fluent English. Preserve fenced code "
    "blocks and everything inside them, inline code, URLs, Markdown images, "
    "HTML tags and attributes, and shortcode tags exactly; you may translate "
    "human-readable text inside a shortcode's opening and closing tags, but "
    "never the tags themselves. Keep internal links unchanged. Output only the "
    "translation, with no commentary and no surrounding code fence."
)


def _split(text: str) -> tuple[list[str], str]:
    if not text.startswith("---"):
        raise ValueError("missing front matter")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("unterminated front matter")
    fm = [line for line in text[3:end].strip("\n").split("\n")]
    body = text[end + 4 :]
    return fm, body.lstrip("\n")


def _get(fm: list[str], key: str) -> tuple[int, str | None]:
    for i, line in enumerate(fm):
        if line.startswith(key + ":"):
            return i, line[len(key) + 1 :].strip()
    return -1, None


def _content_hash(title: str | None, summary: str | None, body: str) -> str:
    h = hashlib.sha256()
    h.update((title or "").encode())
    h.update(b"\x00")
    h.update((summary or "").encode())
    h.update(b"\x00")
    h.update(body.encode())
    return "sha256:" + h.hexdigest()


def _yaml(value: str) -> str:
    if value == "" or re.search(r"[:#[\]{}&*!|>'\"%@`]|^\s|\s$|\n", value):
        return json.dumps(value, ensure_ascii=False)
    return value


def _en_url(value: str) -> str:
    url = value.strip().strip('"')
    if not url.startswith("/") or url.startswith("/en/"):
        return url
    return "/en" + url


def _strip_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[^\n]*\n", "", text)
        text = re.sub(r"\n```$", "", text)
    return text.strip()


def _llm(cfg: Config, system: str, user: str, temperature: float = 0.2) -> str:
    if not cfg.llm_api_key:
        raise SystemExit("translate: LLM_API_KEY is not set")
    base = (cfg.llm_base_url or "https://api.openai.com/v1").rstrip("/")
    payload = json.dumps(
        {
            "model": cfg.llm_model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
    ).encode()
    request = urllib.request.Request(
        base + "/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {cfg.llm_api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")
        raise SystemExit(
            f"translate: LLM request failed ({error.code}): {detail}"
        ) from None
    return _strip_fence(data["choices"][0]["message"]["content"])


def _translate_page(cfg: Config, fm: list[str], body: str) -> tuple[str, str]:
    _, title = _get(fm, "title")
    _, summary = _get(fm, "summary")
    if not CJK.search((title or "") + (summary or "") + body):
        ai = "human"
        title_en, summary_en, body_en = title, summary, body
    else:
        ai = "translated"
        inputs = [title or ""] + ([summary] if summary is not None else [])
        out = _llm(cfg, SYSTEM_LINES, "\n".join(inputs)).split("\n")
        title_en = out[0].strip() if out else title
        if summary is not None:
            summary_en = out[1].strip() if len(out) > 1 else summary
        else:
            summary_en = summary
        body_en = _llm(cfg, SYSTEM_BODY, body)

    rebuilt: list[str] = []
    for line in fm:
        if line.startswith("title:"):
            rebuilt.append("title: " + _yaml(title_en or ""))
        elif line.startswith("summary:"):
            rebuilt.append(
                "summary:" if not summary_en else "summary: " + _yaml(summary_en)
            )
        elif line.startswith("url:"):
            rebuilt.append("url: " + _yaml(_en_url(line[len("url:") :].strip())))
        else:
            rebuilt.append(line)
    rebuilt.append("ai: " + ai)
    return "---\n" + "\n".join(rebuilt) + "\n---\n\n" + body_en.lstrip("\n"), ai


def _en_path(source: Path) -> Path:
    return source.with_name(source.name[: -len(".md")] + EN_SUFFIX)


def run(cfg: Config, seed: bool = False, force: bool = False) -> None:
    root = cfg.root
    content = root / CONTENT_DIR
    state_path = root / STATE_NAME
    state: dict[str, dict[str, str]] = {}
    if state_path.exists() and not seed:
        state = json.loads(state_path.read_text(encoding="utf-8"))

    sources = sorted(
        p for p in (content / "pages").rglob("*.md") if not p.name.endswith(EN_SUFFIX)
    )

    translated = copied = skipped = 0
    for source in sources:
        rel = str(source.relative_to(root))
        fm, body = _split(source.read_text(encoding="utf-8"))
        _, title = _get(fm, "title")
        _, summary = _get(fm, "summary")
        digest = _content_hash(title, summary, body)
        target = _en_path(source)
        record = state.get(rel, {})

        if seed:
            if target.exists():
                state[rel] = {"src": digest, "prompt": PROMPT_VERSION}
            continue

        if (
            not force
            and record.get("src") == digest
            and record.get("prompt") == PROMPT_VERSION
            and target.exists()
        ):
            skipped += 1
            continue

        rendered, ai = _translate_page(cfg, fm, body)
        target.write_text(rendered, encoding="utf-8")
        state[rel] = {"src": digest, "prompt": PROMPT_VERSION}
        if ai == "translated":
            translated += 1
        else:
            copied += 1
        print(f"{'trans' if ai == 'translated' else 'copy '} {rel}")

    for rel in list(state):
        if not (root / rel).exists():
            _en_path(root / rel).unlink(missing_ok=True)
            del state[rel]

    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if seed:
        print(f"seeded {len(state)} page(s)")
    else:
        print(f"translated {translated}, copied {copied}, skipped {skipped}")
