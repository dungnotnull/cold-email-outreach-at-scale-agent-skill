# PROJECT-detail.md — Personalized Cold Email Outreach at Scale

## Executive Summary
A harness that converts an ideal-customer profile (ICP) and offer into a personalized, deliverable, legally compliant multi-step cold-email sequence. It grounds copy in proven frameworks (AIDA, PAS, Cialdini), scores inbox-placement risk against deliverability standards (SPF/DKIM/DMARC, M3AAWG guidance), and enforces a mandatory anti-spam compliance gate (CAN-SPAM/GDPR/CASL) before emitting output.

## Problem Statement
At scale, cold outreach fails on three axes: relevance (generic copy → low replies), deliverability (auth/reputation/spam-words → spam folder), and legality (missing opt-out, no consent basis → fines). Teams need a system that optimizes all three simultaneously with citations.

## Target Users & Use Cases
- **SDR / founder-led sales** — "Write a 4-step sequence for CTOs at Series-B SaaS." → personalized cadence.
- **Agency** — "Audit our client's sequence for spam risk." → deliverability scorecard.
- **Compliance-aware marketer** — "Is this GDPR-safe for EU prospects?" → compliance gate verdict.
- **Growth lead** — "Give me A/B subject-line variants." → quality-reviewer variants.
- **RevOps** — "Personalization variables from this account list?" → audience-analysis output.

## Harness Architecture
```
/cold-email-outreach-at-scale
  Stage 1 Audience      → sub-audience-analysis      → ICP + variables
  Stage 2 Sequence      → sub-sequence-designer      → multi-touch copy
  Stage 3 Deliverability→ sub-deliverability-scorer  → inbox-risk score
  Stage 4 Compliance    → sub-compliance-check (REQ) → legal verdict + opt-out
  Stage 5 Review        → sub-quality-reviewer       → variants + issues
  Stage 6 Synthesize    → main.md                    → final package
```

## Full Sub-Skill Catalog
| Sub-skill | Purpose | Inputs | Outputs | Tools | Quality gate |
|-----------|---------|--------|---------|-------|--------------|
| audience-analysis | ICP + variables | offer, list | segments + tokens | WebSearch | ≥1 personalization variable/segment |
| sequence-designer | Copy + cadence | ICP, offer | sequence | — | Each step uses a named framework |
| deliverability-scorer | Inbox risk | sequence | risk score | WebFetch | Auth + spam-word checks |
| compliance-check | Anti-spam law | sequence, geo | verdict + opt-out | WebFetch | Opt-out + consent basis present |
| quality-reviewer | Persuasion/variants | draft | variants + issues | — | ≥2 A/B variants; claims checked |

## Skill File Format Specification
Standard Claude skill frontmatter + sections. See `skills/main.md`.

## E2E Execution Flow
Audience → sequence → deliverability → compliance (block if fail) → review → assemble. Fallback to cached benchmarks if web down. Error: no consent basis for EU list → refuse send-ready output, advise opt-in path.

## Compliance Decision Tree
```
Prospect geography
├── US only  → CAN-SPAM: truthful headers/subject, opt-out ≤10 days, physical address
├── EU/EEA   → GDPR: lawful basis required (consent or documented legitimate interest),
│              opt-out, data minimization, no send-ready output without lawful basis
├── Canada   → CASL: consent (express/implied) before send, documented basis
└── Multi    → Apply strictest overlap; default to consent-first path
```

## SECOND-KNOWLEDGE-BRAIN Integration
`knowledge_updater.py` crawls deliverability/anti-spam + B2B outreach benchmark sources; dated append with URL-hash deduplication.

## Quality Gates
- Each sequence step uses a named copy framework.
- Deliverability score covers auth + spam triggers.
- Compliance gate passed; opt-out + lawful basis present.
- ≥2 A/B variants provided.
- Claims in copy fact-checked or softened.

## Test Scenarios
See `tests/test-scenarios.md` and executable validators in `tests/validate_skills.py`.

## Key Design Decisions
1. Compliance gate is hard — no send-ready output without opt-out + lawful basis.
2. Deliverability treated as first-class, not an afterthought.
3. Personalization at segment + individual token level.
4. Persuasion grounded in Cialdini, not manipulation/dark patterns.
5. EU prospects require explicit consent path (GDPR) — flagged, not assumed.

## Production-Readiness Checklist
- [x] All skill files use valid frontmatter.
- [x] Compliance gate explicitly BLOCKS non-compliant output.
- [x] Knowledge updater implements real web crawling (not stub).
- [x] Automated validators cover structure and scenario assertions.
- [x] Cross-cluster integration links documented.
