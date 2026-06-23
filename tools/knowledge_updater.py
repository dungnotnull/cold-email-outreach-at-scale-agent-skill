#!/usr/bin/env python3
"""knowledge_updater.py — Cold Email Outreach at Scale (idea 211).

Crawls deliverability / anti-spam guidance and B2B outreach benchmark reports,
appending dated, deduplicated entries to SECOND-KNOWLEDGE-BRAIN.md.

Usage:
    python tools/knowledge_updater.py              # fetch and append
    python tools/knowledge_updater.py --dry-run    # preview without writing
    python tools/knowledge_updater.py --max-entries 30

Production readiness:
- Real HTTP fetching with retries, timeouts, and respectful headers.
- Source-specific parsers plus a generic fallback.
- URL-hash deduplication against existing SECOND-KNOWLEDGE-BRAIN.md entries.
- Keyword scoring + year decay so the most relevant recent items rank first.
- Graceful degradation: a failed source does not crash the whole run.
"""
from __future__ import annotations

import argparse
import hashlib
import logging
import re
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

BRAIN = Path(__file__).resolve().parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"

SOURCES: dict[str, str] = {
    "m3aawg": "https://www.m3aawg.org/published-documents",
    "ftc_canspam": "https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business",
    "google_postmaster": "https://support.google.com/mail/answer/81126",
    "gdpr": "https://gdpr.eu/",
    "casl": "https://fightspam.gc.ca/",
}

KEYWORDS: list[str] = [
    "deliverability", "spam", "dmarc", "dkim", "spf", "open rate", "reply rate",
    "cold email", "outreach", "can-spam", "gdpr", "consent", "unsubscribe",
    "authentication", "sender reputation", "list hygiene", "warm-up", "one-click unsubscribe",
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36 "
    "KnowledgeBot/1.0 (+https://github.com/yourorg/cold-email-outreach-at-scale)"
)

REQUEST_TIMEOUT = 15
MAX_RETRIES = 3


def _url_hash(url: str) -> str:
    """Stable 12-char SHA-256 hash of a normalized URL."""
    normalized = url.strip().lower().rstrip("/")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:12]


def _existing_hashes(text: str) -> set[str]:
    """Parse <!--h:HASH--> markers already in SECOND-KNOWLEDGE-BRAIN.md."""
    return set(re.findall(r"<!--h:([0-9a-f]{12})-->", text))


def _extract_year(text: str) -> int:
    """Find the most recent 19xx/20xx year in text, else current year."""
    years = [int(y) for y in re.findall(r"\b(?:19|20)\d{2}\b", text)]
    if years:
        return max(years)
    return date.today().year


def _fetch(url: str, retries: int = MAX_RETRIES, timeout: int = REQUEST_TIMEOUT) -> str | None:
    """Fetch a URL with retries, timeouts, and a real User-Agent."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as exc:
            logging.warning("Fetch attempt %d/%d failed for %s: %s", attempt + 1, retries, url, exc)
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    return None


def _robots_allowed(url: str) -> bool:
    """Check robots.txt for the target URL; default to allow on failure."""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        rp = RobotFileParser(robots_url)
        rp.read()
        return rp.can_fetch(USER_AGENT, url)
    except Exception as exc:
        logging.warning("Could not read robots.txt for %s: %s", parsed.netloc, exc)
        return True


def _clean_soup(soup: BeautifulSoup) -> None:
    """Remove noisy elements before extracting text."""
    for selector in ("script", "style", "nav", "footer", "header", "aside", "noscript"):
        for tag in soup.find_all(selector):
            tag.decompose()


def _first_meaningful_paragraph(soup: BeautifulSoup) -> str:
    """Return the first paragraph-like text chunk that looks like a summary."""
    _clean_soup(soup)
    for tag in soup.find_all(["p", "div", "article", "section"]):
        text = tag.get_text(" ", strip=True)
        if 80 <= len(text) <= 600:
            return text
    for p in soup.find_all("p"):
        text = p.get_text(" ", strip=True)
        if len(text) > 40:
            return text
    return ""


def _parse_generic(html: str, url: str) -> dict[str, Any]:
    """Generic page parser: title + first meaningful paragraph."""
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else urlparse(url).netloc
    summary = _first_meaningful_paragraph(soup)
    year = _extract_year(title + " " + summary + " " + url)
    source = urlparse(url).netloc.replace("www.", "")
    return {
        "title": title,
        "source": source,
        "year": year,
        "url": url,
        "summary": summary[:240],
    }


def _parse_m3aawg(html: str, url: str) -> list[dict[str, Any]]:
    """M3AAWG published documents: extract document links and titles."""
    soup = BeautifulSoup(html, "html.parser")
    entries: list[dict[str, Any]] = []
    seen = set()
    for link in soup.find_all("a", href=True):
        href = urljoin(url, link["href"])
        if "/published-documents/" not in href and not href.endswith(".pdf"):
            continue
        title = link.get_text(" ", strip=True)
        if not title or len(title) < 8 or title in seen:
            continue
        seen.add(title)
        year = _extract_year(title + " " + href)
        entries.append({
            "title": title,
            "source": "M3AAWG",
            "year": year,
            "url": href,
            "summary": "M3AAWG published document on deliverability or anti-abuse.",
        })
    if not entries:
        entries.append(_parse_generic(html, url))
        entries[0]["source"] = "M3AAWG"
    return entries


def _parse_ftc_canspam(html: str, url: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    summary = _first_meaningful_paragraph(soup)
    return [{
        "title": "CAN-SPAM Act Compliance Guide for Business",
        "source": "FTC",
        "year": _extract_year(summary + " " + url),
        "url": url,
        "summary": summary[:240],
    }]


def _parse_google_postmaster(html: str, url: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    summary = _first_meaningful_paragraph(soup)
    return [{
        "title": "Google Postmaster Tools — Sender Guidelines",
        "source": "Google",
        "year": _extract_year(summary + " " + url),
        "url": url,
        "summary": summary[:240],
    }]


def _parse_gdpr(html: str, url: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    summary = _first_meaningful_paragraph(soup)
    return [{
        "title": "GDPR — General Data Protection Regulation",
        "source": "gdpr.eu",
        "year": _extract_year(summary + " " + url),
        "url": url,
        "summary": summary[:240],
    }]


def _parse_casl(html: str, url: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    summary = _first_meaningful_paragraph(soup)
    return [{
        "title": "Canada's Anti-Spam Legislation (CASL)",
        "source": "Government of Canada",
        "year": _extract_year(summary + " " + url),
        "url": url,
        "summary": summary[:240],
    }]


def fetch_entries() -> list[dict[str, Any]]:
    """Crawl all SOURCES and return a deduplicated list of knowledge entries."""
    parsers: dict[str, Any] = {
        "m3aawg": _parse_m3aawg,
        "ftc_canspam": _parse_ftc_canspam,
        "google_postmaster": _parse_google_postmaster,
        "gdpr": _parse_gdpr,
        "casl": _parse_casl,
    }
    entries: list[dict[str, Any]] = []
    for key, url in SOURCES.items():
        logging.info("Fetching source: %s (%s)", key, url)
        if not _robots_allowed(url):
            logging.warning("robots.txt disallows %s; skipping.", url)
            continue
        html = _fetch(url)
        if html is None:
            logging.warning("Could not fetch %s after retries.", url)
            continue
        parser = parsers.get(key, _parse_generic)
        try:
            result = parser(html, url)
            if isinstance(result, list):
                entries.extend(result)
            elif result:
                entries.append(result)
        except Exception as exc:
            logging.error("Parser failed for %s: %s", url, exc, exc_info=True)
    return entries


def score(entry: dict[str, Any]) -> float:
    """Score an entry by keyword density and recency.

    Recent items (current/previous year) get full weight; older items decay.
    """
    text = f"{entry.get('title', '')} {entry.get('summary', '')}".lower()
    keyword_hits = sum(1 for k in KEYWORDS if k in text)
    year = entry.get("year", 0)
    current_year = date.today().year
    recency = 1.0 if year >= current_year - 1 else 0.4 if year >= current_year - 3 else 0.1
    authoritative = {"ftc.gov", "gdpr.eu", "fightspam.gc.ca", "m3aawg.org", "support.google.com"}
    source_bonus = 1.2 if any(a in entry.get("source", "").lower() for a in authoritative) else 1.0
    return keyword_hits * recency * source_bonus


def append_entries(entries: list[dict[str, Any]]) -> int:
    """Append scored, deduplicated entries to SECOND-KNOWLEDGE-BRAIN.md."""
    if not BRAIN.exists():
        logging.error("Brain file not found: %s", BRAIN)
        return 0
    text = BRAIN.read_text(encoding="utf-8")
    seen = _existing_hashes(text)
    lines: list[str] = []
    added = 0
    for entry in sorted(entries, key=score, reverse=True):
        url = entry.get("url")
        if not url:
            continue
        h = _url_hash(url)
        if h in seen:
            continue
        title = entry.get("title", "(untitled)").replace("\n", " ")
        source = entry.get("source", "?")
        year = entry.get("year", "?")
        summary = entry.get("summary", "").replace("\n", " ").strip()
        line = f"- {date.today().isoformat()} — {title} ({source}, {year}) {url}"
        if summary:
            line += f" — {summary}"
        line += f" <!--h:{h}-->"
        lines.append(line)
        seen.add(h)
        added += 1
    if added:
        new_text = text.rstrip() + "\n\n" + "\n".join(lines) + "\n"
        BRAIN.write_text(new_text, encoding="utf-8")
    return added


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Update SECOND-KNOWLEDGE-BRAIN.md with deliverability and anti-spam knowledge.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print entries that would be appended without writing to the brain file.",
    )
    parser.add_argument(
        "--max-entries",
        type=int,
        default=50,
        help="Maximum number of entries to append per run (default: 50).",
    )
    args = parser.parse_args(argv)

    entries = fetch_entries()
    ranked = sorted(entries, key=score, reverse=True)[: args.max_entries]

    if args.dry_run:
        print(f"[dry-run] Would append {len(ranked)} entries (score >= cutoff):\n")
        for entry in ranked:
            print(f"  score={score(entry):.2f}  {entry['title']} ({entry.get('source')}, {entry.get('year')})")
            print(f"  url={entry['url']}")
            if entry.get("summary"):
                print(f"  summary={entry['summary'][:100]}...")
            print()
        return 0

    added = append_entries(ranked)
    print(f"[211] appended {added} entries to {BRAIN.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
