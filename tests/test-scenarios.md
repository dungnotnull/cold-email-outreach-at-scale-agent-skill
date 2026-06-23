# Test Scenarios — Cold Email Outreach at Scale (Idea 211)

Each scenario below has an explicit pass checklist. The structural validators in `tests/validate_skills.py` and the unit tests in `tests/test_knowledge_updater.py` cover the harness machinery; scenario-level quality is enforced by the skill quality gates in `skills/main.md`.

## Scenario 1 — 4-step SaaS sequence
**Input:** Offer = observability tool; ICP = CTOs at Series-B SaaS (US).
**Expected:** 4-touch sequence, each step framework-tagged, tokens, single CTA; CAN-SPAM elements present.
**Pass checklist:**
- [ ] ICP section lists industry, size, geography, persona.
- [ ] Sequence has 4 steps with delays.
- [ ] Every step names a framework (AIDA/PAS/BAB/4 Ps).
- [ ] Every step has ≥1 personalization token.
- [ ] Every step has exactly one CTA.
- [ ] Deliverability scorecard has auth + content + reputation dimensions.
- [ ] Compliance verdict is PASS for US with opt-out + physical address.
- [ ] ≥2 subject + opener A/B variants.

## Scenario 2 — GDPR block
**Input:** Cold outreach to EU contacts scraped without consent.
**Expected:** Compliance gate marks output BLOCKED; prescribes opt-in/lawful-basis path.
**Pass checklist:**
- [ ] Geography identified as EU/EEA.
- [ ] Compliance status is BLOCKED.
- [ ] Missing element is "lawful basis" or "consent".
- [ ] Prescribed fix is a consent campaign or documented LIA.
- [ ] Send-ready status banner says BLOCKED / NOT SEND-READY.

## Scenario 3 — Spam-risk audit
**Input:** Existing sequence with ALL-CAPS subjects, 5 links, no DMARC.
**Expected:** Deliverability scorer flags High risk with specific fixes.
**Pass checklist:**
- [ ] Content dimension risk is High (ALL-CAPS or ≥3 links).
- [ ] Auth dimension risk is High (DMARC missing).
- [ ] Each High risk has a concrete fix.
- [ ] Overall risk is High.
- [ ] Quality reviewer flags misleading subject lines.

## Scenario 4 — A/B variants
**Input:** Any approved sequence.
**Expected:** ≥2 subject + opener variants and an experiment plan.
**Pass checklist:**
- [ ] ≥2 subject-line variants for first touch.
- [ ] ≥2 opener variants for first touch.
- [ ] Each variant is tagged with the lever it tests.
- [ ] Experiment plan includes open-rate, reply-rate, and meeting-rate tests.

## Scenario 5 — Personalization depth
**Input:** Account list with funding + tech-stack data.
**Expected:** Audience-analysis maps fillable tokens per segment; sequence uses them.
**Pass checklist:**
- [ ] Segments are defined by pain/maturity or role.
- [ ] Each segment has ≥1 fillable token with data source.
- [ ] Sequence uses `{{company}}`, `{{funding_round}}`, or `{{tech_stack}}` tokens.
- [ ] Tokens trace to real variables in the ICP table.

## Scenario 6 — Honesty check
**Input:** Draft claims "trusted by 10,000 companies" with no source.
**Expected:** Quality-reviewer flags unverified claim; softens or requests proof.
**Pass checklist:**
- [ ] Quality review issues table includes the unverified claim.
- [ ] Severity is High.
- [ ] Fix either removes the number, softens it, or requests proof.
- [ ] Send-ready copy contains no unverified statistic.
