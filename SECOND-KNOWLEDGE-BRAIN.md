# SECOND-KNOWLEDGE-BRAIN — Personalized Cold Email Outreach

## Core Concepts & Frameworks
- **Copy frameworks** — AIDA (Attention-Interest-Desire-Action), PAS (Problem-Agitate-Solve), BAB (Before-After-Bridge), 4 Ps.
- **Cialdini persuasion** — reciprocity, social proof, authority, scarcity, commitment, liking (use ethically).
- **Deliverability** — SPF/DKIM/DMARC authentication; sender reputation; warm-up; list hygiene; spam-trigger words; text-to-link ratio; one-click unsubscribe (RFC 8058).
- **Anti-spam law** — CAN-SPAM (US): no false headers, clear opt-out honored ≤10 days, physical address. GDPR (EU): lawful basis/consent for personal data, B2B nuance per member state. CASL (Canada): consent-first, strict.
- **B2B benchmarks** — reply rates ~1–10% depending on targeting; personalization + relevance dominate.

## Key Reference Frameworks (citable)
| Framework | Source | Use |
|-----------|--------|-----|
| CAN-SPAM Act | FTC | US compliance |
| GDPR | EU 2016/679 | EU consent/lawful basis |
| CASL | Canada | Consent-first outreach |
| DMARC/DKIM/SPF | IETF RFCs | Authentication |
| M3AAWG sender best practices | M3AAWG | Deliverability |

## Per-Provider Deliverability Notes
| Provider | Auth emphasis | Content/engagement tips |
|----------|---------------|--------------------------|
| Gmail / Google Workspace | SPF/DKIM/DMARC aligned; low spam complaint rate (<0.1%) | Plain-text leaning; one clear CTA; RFC 8058 one-click unsubscribe |
| Outlook / Microsoft 365 | DKIM + low bounce rate (<2%); dedicated sending domain | Avoid spam words; consistent volume; warm up gradually |
| Yahoo / AOL (Verizon) | DMARC p=reject enforced; alignment required | No URL shorteners; honor opt-outs fast; maintain list hygiene |
| Apple Mail | MPP pre-loads pixels; opens are unreliable | Optimize for clicks/replies; concise subject; mobile preview |
| Corporate on-prem | IP/domain reputation, content filters, allowlists | Gradual warm-up; no image-only emails; authenticated headers |

## Key Research Papers / Reports
| Title | Source | Year | Link | Relevance |
|-------|--------|------|------|-----------|
| Email Sender & Provider Best Practices | M3AAWG | ongoing | https://www.m3aawg.org/published-documents | Deliverability |
| Influence: The Psychology of Persuasion | Cialdini | 2006 | — | Persuasion principles |

## State-of-the-Art Methods & Tools
ESP warm-up tools; Google Postmaster Tools; spam-score linters; dynamic personalization (Liquid tokens); intent-data targeting; BIMI; one-click unsubscribe (RFC 8058).

## Authoritative Data Sources
ftc.gov (CAN-SPAM); gdpr.eu / EUR-Lex; fightspam.gc.ca (CASL); m3aawg.org; postmaster.google.com; IETF RFCs.

## Analytical Frameworks
Deliverability risk matrix (auth × content × reputation); persuasion-framework checklist; compliance decision tree (geo → law → requirements).

## Self-Update Protocol
`knowledge_updater.py` weekly: crawl deliverability/anti-spam updates + outreach benchmark reports; dedup by URL hash; append below.

## Knowledge Update Log
- 2026-06-18 — Seed: copy/deliverability/anti-spam frameworks captured.
