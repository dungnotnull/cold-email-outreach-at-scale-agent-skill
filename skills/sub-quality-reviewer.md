---
name: sub-quality-reviewer
description: Reviews cold-email copy for persuasion, clarity, honesty, and provides A/B variants. Shared across marketing-content-branding cluster.
---

## Purpose
Final persuasion and integrity pass before output. This sub-skill is shared with the broader `marketing-content-branding` cluster (ideas 151 and 72).

## Inputs
- Draft sequence from `sub-sequence-designer`.
- Deliverability scorecard and compliance verdict.
- Any source material for claims in the copy.

## Procedure
1. **Fact-check claims**: every statistic, customer count, revenue figure, or result must have a source. If unverified, soften to "customers like {{example}}" or flag for proof.

2. **Remove dark patterns / false urgency**: no fake countdowns, no "Re: " prefixes on new threads, no misleading preview text, no false scarcity.

3. **Readability check**:
   - Average sentence length ≤20 words.
   - Mobile preview looks good (subject + first line).
   - Scanning: key point visible in 3 seconds.
   - Tone: concise, respectful, human.

4. **Generate A/B variants**:
   - ≥2 subject-line variants per first-touch email.
   - ≥2 opener variants (first sentence) per first-touch email.
   - Tag each variant with the lever it tests (curiosity, specificity, personalization, social proof).

5. **Suggest experiments**:
   - One experiment for **open rate** (subject line).
   - One experiment for **reply rate** (CTA / body).
   - One experiment for **meeting rate** (offer framing).

## Output Format
```markdown
## Quality Review

### Issues
| # | Issue | Severity | Fix |
|---|-------|----------|-----|
| 1 | "trusted by 10,000 companies" unverified | High | Replace with "used by teams like {{named_customer}}" until proof available |
| 2 | CTA too vague | Low | Change "let me know" to "worth a 10-minute call on Thursday?" |

### A/B Variants
**Subject variants**
- A: `{{company}}'s observability gap` (personalization)
- B: `Cutting alert noise by 60%` (specificity)

**Opener variants**
- A: `Congrats on the Series B, {{first_name}}.` (social/liking)
- B: `Saw {{company}} is hiring 10 backend engineers.` (intent signal)

### Experiments
- Open rate: test subject A vs. B over 200 emails each.
- Reply rate: test reply CTA vs. calendar-link CTA.
- Meeting rate: test pain-first vs. social-proof-first angle.
```

## Example
**Input:** Draft claims "we're the #1 observability platform" with no citation.
**Output:** Issue flagged (High); softened to "observability platform used by Series-B SaaS teams" until third-party proof is attached.

## Quality Gate
- [ ] ≥2 A/B variants for subject line and opener.
- [ ] No unverified claims remain in send-ready copy.
- [ ] No dark patterns or misleading subjects.
- [ ] One experiment suggested per metric (open, reply, meeting).
