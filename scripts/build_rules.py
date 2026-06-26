#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "pinterest-domains.txt"
SHADOWROCKET_DIR = ROOT / "rule" / "Shadowrocket" / "Pinterest"
MIHOMO_DIR = ROOT / "rule" / "Mihomo" / "Pinterest"
UPSTREAM_URL = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/pinterest"


def normalize_domain(line: str) -> str | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if line.startswith("include:") or line.startswith("regexp:") or line.startswith("keyword:"):
        return None
    for prefix in ("full:", "domain:"):
        if line.startswith(prefix):
            line = line[len(prefix):]
    line = line.split("@", 1)[0].strip().lower()
    if not line or "*" in line:
        return None
    return line


def load_local_domains() -> set[str]:
    return {
        domain
        for domain in (normalize_domain(line) for line in DATA_FILE.read_text().splitlines())
        if domain
    }


def load_upstream_domains() -> set[str]:
    try:
        with urllib.request.urlopen(UPSTREAM_URL, timeout=20) as resp:
            text = resp.read().decode("utf-8")
    except Exception:
        return set()
    return {
        domain
        for domain in (normalize_domain(line) for line in text.splitlines())
        if domain
    }


def sort_domains(domains: set[str]) -> list[str]:
    return sorted(domains, key=lambda d: (d.count("."), d))


def header(name: str, total: int, extra: list[str] | None = None) -> str:
    lines = [
        f"# NAME: {name}",
        "# AUTHOR: DDcat2025",
        "# REPO: https://github.com/DDcat2025/pinterest-shadowrocket-rules",
        f"# UPDATED: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"# DOMAIN-SUFFIX: {total}",
        f"# TOTAL: {total}",
    ]
    if extra:
        lines.extend(extra)
    return "\n".join(lines) + "\n"


def write_shadowrocket(domains: list[str]) -> None:
    SHADOWROCKET_DIR.mkdir(parents=True, exist_ok=True)

    full = header(
        "Pinterest",
        len(domains),
        ["# DESCRIPTION: Pinterest / Pinimg / Pinterest Ads / Pinterest Business routing rules for Shadowrocket."],
    )
    full += "\n".join(f"DOMAIN-SUFFIX,{domain}" for domain in domains) + "\n"
    (SHADOWROCKET_DIR / "Pinterest.list").write_text(full)

    domain_set = header(
        "Pinterest Domain Set",
        len(domains),
        ["# DESCRIPTION: Domain-only list for clients that use Domain Set format."],
    )
    domain_set += "\n".join(domains) + "\n"
    (SHADOWROCKET_DIR / "Pinterest_Domain.list").write_text(domain_set)


def write_mihomo(domains: list[str]) -> None:
    MIHOMO_DIR.mkdir(parents=True, exist_ok=True)
    body = [
        "payload:",
        *[f"  - '+.{domain}'" for domain in domains],
    ]
    (MIHOMO_DIR / "Pinterest.yaml").write_text("\n".join(body) + "\n")


def main() -> None:
    domains = sort_domains(load_local_domains() | load_upstream_domains())
    write_shadowrocket(domains)
    write_mihomo(domains)
    print(f"Generated {len(domains)} Pinterest rules")


if __name__ == "__main__":
    main()
