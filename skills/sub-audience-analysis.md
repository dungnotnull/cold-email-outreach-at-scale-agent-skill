---
name: sub-audience-analysis
description: Defines the ideal customer profile, segments, and per-segment personalization variables for cold outreach. Shared across marketing-content-branding cluster.
---

## Purpose
Ground the sequence in a precise audience so personalization is real, not cosmetic. This sub-skill is also shared with the broader `marketing-content-branding` cluster (ideas 151 and 72) for audience segmentation.

## Inputs
- **Offer / value proposition**: what problem you solve, for whom, with what outcome.
- **Target market**: geography, industry, company size, go-to-market motion.
- **Account / contact list (optional)**: fields available for personalization.
- **Constraints**: compliance regime (US, EU, Canada, mixed), send volume, brand voice.

## Procedure
1. **Define the ICP** with firmographics:
   - Industry / vertical
   - Company size (employees, revenue, funding stage)
   - Geography (US, EU/EEA, Canada, other)
   - Tech stack or stack signals if known
   - Role / persona (title, seniority, function)
   - Trigger events (recent funding, hiring, expansion, regulation change, M&A)

2. **Segment by pain and maturity** into 2–4 segments. Common axes:
   - Primary pain (cost, risk, speed, growth)
   - Maturity (early vs. scaled)
   - Role (economic buyer vs. practitioner)

3. **For each segment, list fillable personalization variables**:
   - Account-level: `{{company}}`, `{{industry}}`, `{{funding_round}}`, `{{tech_stack}}`, `{{hiring_signal}}`, `{{recent_news}}`
   - Contact-level: `{{first_name}}`, `{{title}}`, `{{department}}`, `{{content_published}}`, `{{mutual_connection}}`
   - Intent-level: `{{tool_used}}`, `{{job_posting}}`, `{{growth_signal}}`

4. **Map each segment's primary pain → offer benefit → proof point**.

5. **Note data source for each variable** so tokens can actually be filled (CRM, LinkedIn, ZoomInfo, job boards, press releases, intent data).

## Output Template

```markdown
### ICP
- Industry: [e.g., B2B SaaS]
- Size: [e.g., 100–500 employees, Series B/C]
- Geography: [e.g., US + Canada]
- Persona: [e.g., VP Engineering]
- Trigger: [e.g., recent SOC 2 certification push]

### Segments
| Segment | Persona | Pain | Benefit | Personalization variables | Data source |
|---------|---------|------|---------|---------------------------|-------------|
| A — High-growth | CTO | Observability gaps during scaling | Cut MTTR 40% | `{{company}}`, `{{funding_round}}`, `{{stack}}` | Crunchbase + BuiltWith |
| B — Security-first | CISO | Compliance audit fatigue | Pass SOC 2 faster | `{{framework}}`, `{{audit_date}}` | LinkedIn + job posts |

### Pain → Benefit Mapping
- A: Scaling infra → unified observability → proof: "Series-B SaaS reduced MTTR 40%"
- B: Compliance burden → automated evidence → proof: "SOC 2 in 6 weeks"
```

## Example Walkthrough
**Input:** Offer = AI-powered observability; target = CTOs at Series-B SaaS in the US.
**Output:**
- ICP: B2B SaaS, 100–500 employees, Series B, US, CTO, scaling engineering team.
- Segment A (fast scaling): pain = alert fatigue; benefit = noise reduction; variables = `{{company}}`, `{{headcount_growth}}`, `{{stack}}`.
- Segment B (reliability focused): pain = downtime cost; benefit = MTTR reduction; variables = `{{company}}`, `{{recent_outage_signal}}`, `{{team_size}}`.

## Quality Gate
- [ ] At least one segment defined.
- [ ] Each segment has ≥1 fillable personalization variable with a named data source.
- [ ] Each segment has a clear pain → benefit mapping.
- [ ] Geography is noted so the compliance gate can choose the correct law.
