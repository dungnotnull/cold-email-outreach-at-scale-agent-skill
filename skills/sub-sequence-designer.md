---
name: sub-sequence-designer
description: Builds a multi-step cold-email cadence with subject lines and bodies, each step grounded in a named copy framework and using personalization tokens.
---

## Purpose
Produce a relevant, varied sequence that earns replies without burning the prospect or the sender's domain reputation.

## Inputs
- ICP and segments from `sub-audience-analysis`.
- Offer / value proposition.
- Personalization variables and data sources.
- Compliance context (geo, opt-out, lawful basis).

## Procedure
1. **Choose cadence length** based on use case:
   - **4 touches** for warm inbound / trial sign-ups.
   - **5–6 touches** for outbound cold.
   - **Breakup email** as final touch.

2. **Set send delays** (business days):
   - Touch 1 → 2: 2–3 days
   - Touch 2 → 3: 3–4 days
   - Touch 3 → 4: 4–5 days
   - Touch 4 → 5: 5–7 days
   - Touch 5 → 6: 7+ days (breakup)

3. **For each step, select a framework** and angle:
   - Touch 1 — AIDA or BAB: value-first hook.
   - Touch 2 — PAS: agitate the pain.
   - Touch 3 — Social proof / Authority: case study or peer result.
   - Touch 4 — Scarcity / Commitment (ethical): limited-time insight or small ask.
   - Touch 5 — Breakup / Liking: polite close-the-loop.

4. **Write each email**:
   - Subject: ≤50 characters, no ALL CAPS, no excessive punctuation.
   - Body: 50–125 words; 3–5 short paragraphs; one clear CTA.
   - Personalization token in first sentence or subject where natural.
   - Avoid multiple links; prefer one link or a reply CTA.

5. **Apply ethical Cialdini levers**: social proof (real customer), authority (real credential), liking (shared context), reciprocity (free insight). Never fake scarcity or false authority.

## Framework Selection Guide
| Framework | Best use | Structure |
|-----------|----------|-----------|
| AIDA | Cold open / awareness | Attention → Interest → Desire → Action |
| PAS | Problem-centric buyer | Problem → Agitate → Solve |
| BAB | Transformation story | Before → After → Bridge |
| 4 Ps | Product-led pitch | Picture → Promise → Prove → Push |

## Copy Templates

**AIDA cold open**
```
Subject: {{company}}'s {{team}} scaling pain
Hi {{first_name}},

Saw {{company}} doubled its engineering team this quarter — congrats. That growth usually surfaces observability gaps right when uptime matters most.

We help Series-B SaaS teams cut alert noise by 60% and shave hours off MTTR.

Worth a 10-minute chat to see if it fits your stack?

{{signature}}
```

**PAS follow-up**
```
Subject: The cost of silent failures
Hi {{first_name}},

Quick follow-up. The hardest part of scaling isn't writing code — it's knowing what's breaking before customers do.

One missed alert at 2 a.m. can turn a minor bug into a churn risk.

{{product}} auto-groups related alerts so your team sees the incident, not the noise.

Open to a 10-minute look?
```

## Output Format
```markdown
| Step | Delay | Framework | Angle | Subject | Body | Tokens | CTA |
|------|-------|-----------|-------|---------|------|--------|-----|
| 1 | Day 0 | AIDA | Value hook | ... | ... | `{{company}}`, `{{team}}` | Reply for 10-min chat |
```

## Quality Gate
- [ ] Each step tagged to a named framework (AIDA/PAS/BAB/4 Ps).
- [ ] Single CTA per email.
- [ ] Tokens map to real variables from audience analysis.
- [ ] No ALL CAPS, excessive punctuation, or image-heavy emails.
- [ ] No fake scarcity, false social proof, or misleading subject lines.
