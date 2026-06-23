# CLAUDE.md — Personalized Cold Email Outreach at Scale (Idea 211)

**Skill name:** cold-email-outreach-at-scale
**Tagline:** Designs personalized, deliverable, legally compliant B2B cold-email sequences at scale, scored against copywriting and deliverability best practices.
**Cluster:** marketing-content-branding (compliance-gated — anti-spam law applies)
**Source idea:** 211
**Current phase:** Production-grade deliverable set complete

## Problem This Skill Solves
Cold email is high-leverage but easy to do badly: poor personalization tanks reply rates, weak technical setup (SPF/DKIM/DMARC) and spammy copy land in spam, and CAN-SPAM/GDPR/CASL violations create legal risk. This skill turns an ICP + offer into a personalized multi-step sequence, scores it for deliverability and persuasion, and runs a mandatory compliance gate before output.

## Harness Flow Summary
1. **Audience analysis** → sub-audience-analysis — ICP, segments, personalization variables.
2. **Sequence design** → sub-sequence-designer — multi-step cadence with AIDA/PAS copy + personalization tokens.
3. **Deliverability scoring** → sub-deliverability-scorer — spam-trigger, auth, sender-reputation checks.
4. **Compliance gate** → sub-compliance-check (MANDATORY) — CAN-SPAM/GDPR/CASL, opt-out, consent.
5. **Quality review** → sub-quality-reviewer — challenge claims, A/B suggestions.
6. **Synthesize** → sequence + scorecard + roadmap.

## Sub-skills
- sub-audience-analysis.md — ICP & personalization variable extraction.
- sub-sequence-designer.md — multi-touch copy + cadence.
- sub-deliverability-scorer.md — inbox-placement risk scoring.
- sub-compliance-check.md — anti-spam law gate (mandatory).
- sub-quality-reviewer.md — persuasion/clarity review + A/B variants.

## Tools Required
WebSearch, WebFetch, Read, Write, Bash.

## Knowledge Sources
- CAN-SPAM Act (FTC) — https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- GDPR — https://gdpr.eu/ / EUR-Lex
- CASL — https://fightspam.gc.ca/
- M3AAWG sender best practices — https://www.m3aawg.org/published-documents
- Google Postmaster Tools — https://support.google.com/mail/answer/81126
- IETF SPF/DKIM/DMARC RFCs
- Cialdini persuasion principles

## Per-ESP Deliverability Tip Table

| Provider | Key signals | Actions that improve placement |
|----------|-------------|------------------------------|
| Gmail / Google Workspace | User engagement, spam report rate, auth alignment | SPF/DKIM/DMARC aligned; low spam complaints (<0.1%); gradual warm-up; clear unsubscribe |
| Outlook / Microsoft 365 | Sender reputation, engagement, list quality | Authenticate with DKIM; maintain low bounce rate (<2%); use dedicated sending domain |
| Yahoo / AOL (Verizon) | DMARC p=reject strongly enforced | Align SPF/DKIM with From domain; one-click unsubscribe; honor opt-outs ≤10 days |
| Apple Mail | Privacy Mail Protection Pixel (MPP) inflates opens | Optimize for real clicks/replies; subject line relevance; avoid open-rate-only metrics |
| Corporate on-prem filters | Content filters, IP/domain reputation, allowlists | Plain-text leaning; minimal links; no URL shorteners; warm-up IP/domain gradually |

## Supporting Tools
- 	ools/knowledge_updater.py — crawls deliverability + outreach-benchmark sources.

## Active Development Tasks
- [x] Scaffold deliverables
- [x] Add per-ESP deliverability tip table
- [x] Track reply-rate benchmark drift

## Reference Docs
PROJECT-detail.md, PROJECT-DEVELOPMENT-PHASE-TRACKING.md, SECOND-KNOWLEDGE-BRAIN.md, docs/cluster-integration.md.
