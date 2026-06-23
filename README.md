# cold-email-outreach-at-scale

A production-grade Codex skill that designs personalized, deliverable, and legally compliant B2B cold-email sequences at scale.

## What it does
Given an ICP (ideal-customer profile) and offer, the skill produces a multi-touch email sequence, scores it for inbox placement, runs a mandatory anti-spam compliance gate, and supplies A/B variants plus an optimization roadmap.

## Harness stages
1. **Audience analysis** — ICP, segments, personalization variables.
2. **Sequence design** — 4–6 touch cadence with AIDA/PAS/BAB copy frameworks.
3. **Deliverability scoring** — SPF/DKIM/DMARC, spam-trigger words, volume, list hygiene.
4. **Compliance gate** — CAN-SPAM / GDPR / CASL hard block if requirements are missing.
5. **Quality review** — claim checking, dark-pattern removal, A/B variants.
6. **Synthesize** — final send-ready package (or BLOCKED with fix list).

## Repository layout
```
.
├── CLAUDE.md                         # Skill overview and per-ESP tips
├── PROJECT-detail.md                 # Architecture and design decisions
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md
├── SECOND-KNOWLEDGE-BRAIN.md         # Curated deliverability/compliance knowledge
├── skills/
│   ├── main.md                       # Central orchestrator
│   ├── sub-audience-analysis.md
│   ├── sub-sequence-designer.md
│   ├── sub-deliverability-scorer.md
│   ├── sub-compliance-check.md
│   └── sub-quality-reviewer.md
├── tools/
│   └── knowledge_updater.py          # Real crawler for knowledge updates
├── tests/
│   ├── test-scenarios.md             # Scenario checklists
│   ├── validate_skills.py            # Structural validation
│   └── test_knowledge_updater.py     # Unit tests (mocked network)
├── docs/
│   └── cluster-integration.md        # Cross-cluster reuse guide
├── requirements.txt
├── pytest.ini
└── LICENSE
```

## Quick start
### Run structural validation
```bash
python tests/validate_skills.py
```

### Run unit tests
```bash
python -m pytest tests/ -v
```

### Update knowledge brain (dry-run)
```bash
python tools/knowledge_updater.py --dry-run
```

To actually append new entries to `SECOND-KNOWLEDGE-BRAIN.md`, remove `--dry-run`.

## Design principles
- **Compliance is a hard gate.** No send-ready output without opt-out + lawful basis.
- **Deliverability is first-class.** Auth, content, and reputation are scored before sending.
- **Personalization is data-driven.** Every segment has fillable tokens tied to real data sources.
- **Persuasion is ethical.** Cialdini levers are applied; dark patterns are rejected.

## License
MIT — see `LICENSE`.
