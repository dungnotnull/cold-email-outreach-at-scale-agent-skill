---
name: sub-deliverability-scorer
description: Scores inbox-placement risk of a cold-email sequence against authentication, content, and sender-reputation best practices.
---

## Purpose
Catch spam-folder risks before sending and prescribe specific fixes.

## Inputs
- Sequence copy (subject lines + bodies).
- Sending setup: sending domain, ESP, SPF/DKIM/DMARC status, warm-up state, daily volume.
- List hygiene context: bounce history, source of contacts, recent imports.

## Procedure
1. **Authentication** — verify or advise:
   - SPF record present and includes sending IP/ESP.
   - DKIM signature present and aligned with From domain.
   - DMARC policy at least `p=quarantine` (ideally `p=reject`) with RUA reporting.
   - Custom tracking domains if links are used.

2. **Content scan** per email:
   - Spam-trigger words/phrases (see list below).
   - ALL CAPS usage.
   - Excessive punctuation (`!!!`, `???`, repeated `$`).
   - Number of links (target ≤1 per email; never URL shorteners).
   - Image-to-text ratio (avoid image-only emails).
   - HTML cleanliness (no broken tags; mobile-readable).

3. **Reputation / volume**:
   - Warm-up status: new domain/IP needs 2–4 weeks of gradual ramp.
   - Daily volume per domain/IP (recommend ≤50/day for cold start, ≤200/day for warmed).
   - Bounce rate target <2%; spam complaint rate <0.1%.
   - List hygiene: remove hard bounces, role-only addresses, catch-alls.

4. **Format**:
   - Plain-text leaning or light HTML.
   - One-click unsubscribe (RFC 8058) in every send-ready email.
   - Valid physical postal address (CAN-SPAM).
   - No URL shorteners or redirect chains.

5. **Assign risk** per dimension and overall:
   - Low: no issues or one minor issue with easy fix.
   - Med: 2–3 moderate issues; send only after fixes.
   - High: auth missing, heavy spam signals, or compliance block; do not send.

## Spam-Trigger Word List (non-exhaustive)
`free`, `guaranteed`, `no obligation`, `act now`, `limited time`, `urgent`, `winner`, `click here`, `buy now`, `order now`, `cash`, `credit`, `earn money`, `make money`, `risk-free`, `act immediately`, `call now`, `exclusive deal`, `double your`, `you're a winner`, `100% free`.

## Risk Scoring Rubric
| Dimension | Low | Med | High |
|-----------|-----|-----|------|
| Auth | SPF+DKIM+DMARC aligned | One auth record missing | DMARC missing or no SPF/DKIM |
| Content | 0–1 spam triggers, ≤1 link | 2–3 triggers or 2 links | ≥4 triggers, ≥3 links, ALL CAPS |
| Reputation | Warm domain, low bounce | New domain or bounce 2–5% | New + high volume or bounce >5% |
| Format | Plain-text lean + unsubscribe | HTML heavy, unsubscribe present | No unsubscribe or URL shortener |

## Output Format
```markdown
## Deliverability Scorecard
| Dimension | Finding | Risk | Fix |
|-----------|---------|------|-----|
| Auth | DKIM aligned, DMARC p=quarantine | Low | Add RUA report mailbox |
| Content | Subject uses "free"; 2 links | Med | Remove "free"; reduce to 1 link |
| Reputation | New domain, no warm-up | High | Run 2-week warm-up; cap volume at 20/day |
| Format | Unsubscribe present, plain text | Low | None |

**Overall risk:** Med
```

## Example
**Input:** 4-step SaaS sequence, new domain, subject line "FREE demo — act now!!!"
**Output:**
- Auth: SPF/DKIM present; DMARC missing → High.
- Content: "FREE", "act now", "!!!", 2 links → High.
- Reputation: new domain, no warm-up → High.
- Format: no unsubscribe, no address → High (also compliance block).
**Verdict:** High risk — fix auth, rewrite copy, warm up, add unsubscribe before sending.

## Quality Gate
- [ ] Auth + content + reputation all assessed.
- [ ] Each High risk has a concrete fix.
- [ ] Each email risk level is assigned.
- [ ] Overall risk is computed from the worst non-empty dimension.
