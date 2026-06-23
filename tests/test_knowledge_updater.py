#!/usr/bin/env python3
"""Unit tests for tools/knowledge_updater.py.

Uses mocked network responses so tests are fast, deterministic, and offline-safe.
Run:
    python -m pytest tests/test_knowledge_updater.py -v
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path
from unittest import mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import knowledge_updater as ku


SAMPLE_M3AAWG_HTML = """
<html><head><title>M3AAWG Published Documents</title></head><body>
<a href="/published-documents/sender-best-practices">Sender Best Practices 2025</a>
<a href="/published-documents/anti-abuse-guide.pdf">Anti-Abuse Guide</a>
<p>M3AAWG publishes guidance for email senders and mailbox providers.</p>
</body></html>
"""

SAMPLE_GENERIC_HTML = """
<html><head><title>Email Deliverability Report 2024</title></head><body>
<p>Cold email reply rates improved in 2024 when senders implemented DMARC and reduced spam triggers.</p>
</body></html>
"""


def test_url_hash_is_stable_and_short():
    h1 = ku._url_hash("https://example.com/path/")
    h2 = ku._url_hash("https://example.com/path")
    assert h1 == h2
    assert len(h1) == 12


def test_existing_hashes_parses_markers():
    text = "- entry one <!--h:abc123def456-->\n- entry two <!--h:7890abcdef12-->"
    assert ku._existing_hashes(text) == {"abc123def456", "7890abcdef12"}


def test_extract_year_finds_recent_year():
    assert ku._extract_year("Updated in 2023 and revised 2025") == 2025
    assert ku._extract_year("Old document from 1999") == 1999


def test_extract_year_defaults_to_current():
    assert ku._extract_year("No year here") == date.today().year


def test_parse_generic_extracts_title_and_summary():
    entry = ku._parse_generic(SAMPLE_GENERIC_HTML, "https://example.com/report")
    assert entry["title"] == "Email Deliverability Report 2024"
    assert "DMARC" in entry["summary"]
    assert entry["year"] == 2024


def test_parse_m3aawg_extracts_document_links():
    entries = ku._parse_m3aawg(SAMPLE_M3AAWG_HTML, "https://www.m3aawg.org/published-documents")
    titles = {e["title"] for e in entries}
    assert "Sender Best Practices 2025" in titles
    assert "Anti-Abuse Guide" in titles
    assert all(e["source"] == "M3AAWG" for e in entries)


def test_score_boosts_recent_authoritative_keywords():
    recent = {"title": "DMARC and cold email deliverability 2025", "source": "m3aawg.org", "year": 2025, "summary": "reply rate", "url": "https://x"}
    old = {"title": "Generic marketing thoughts 2010", "source": "blog.example", "year": 2010, "summary": "", "url": "https://y"}
    assert ku.score(recent) > ku.score(old)


def test_append_entries_dedupes_and_appends(tmp_path):
    brain = tmp_path / "SECOND-KNOWLEDGE-BRAIN.md"
    brain.write_text("# Brain\n\n## Knowledge Update Log\n- 2026-06-18 — Seed entry (seed, 2026) https://seed.example <!--h:0aac06c994f9-->\n", encoding="utf-8")

    ku.BRAIN = brain
    entries = [
        {"title": "New deliverability guide", "source": "FTC", "year": 2025, "url": "https://ftc.gov/new", "summary": "Updated guidance."},
        {"title": "Seed entry", "source": "seed", "year": 2026, "url": "https://seed.example", "summary": ""},
    ]
    added = ku.append_entries(entries)
    assert added == 1
    text = brain.read_text(encoding="utf-8")
    assert "New deliverability guide" in text


def test_fetch_entries_uses_mocks(monkeypatch):
    """Mock the network so fetch_entries runs offline and returns expected entries."""
    m3aawg_resp = mock.Mock()
    m3aawg_resp.text = SAMPLE_M3AAWG_HTML
    m3aawg_resp.raise_for_status = mock.Mock()

    ftc_resp = mock.Mock()
    ftc_resp.text = SAMPLE_GENERIC_HTML
    ftc_resp.raise_for_status = mock.Mock()

    google_resp = mock.Mock()
    google_resp.text = SAMPLE_GENERIC_HTML
    google_resp.raise_for_status = mock.Mock()

    gdpr_resp = mock.Mock()
    gdpr_resp.text = SAMPLE_GENERIC_HTML
    gdpr_resp.raise_for_status = mock.Mock()

    casl_resp = mock.Mock()
    casl_resp.text = SAMPLE_GENERIC_HTML
    casl_resp.raise_for_status = mock.Mock()

    call_count = {"n": 0}
    def fake_get(url, **kwargs):
        call_count["n"] += 1
        if "m3aawg" in url:
            return m3aawg_resp
        if "ftc" in url:
            return ftc_resp
        if "google" in url:
            return google_resp
        if "gdpr" in url:
            return gdpr_resp
        return casl_resp

    monkeypatch.setattr(ku.requests, "get", fake_get)
    monkeypatch.setattr(ku, "_robots_allowed", lambda url: True)

    entries = ku.fetch_entries()
    assert len(entries) >= 5  # at least one per source
    assert call_count["n"] == len(ku.SOURCES)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
