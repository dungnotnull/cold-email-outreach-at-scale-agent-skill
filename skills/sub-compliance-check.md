---
name: sub-compliance-check
description: Mandatory anti-spam compliance gate (CAN-SPAM/GDPR/CASL) for cold email — verifies opt-out, lawful basis, and required disclosures before send-ready output.
---

## Purpose
Prevent legally non-compliant outreach from being emitted as send-ready. This gate is mandatory and hard-blocking. It is shared with the broader `marketing-content-branding` cluster (ideas 151 and 72) for any outbound copy that may be sent to prospects.

## Inputs
- Sequence copy (subjects + bodies).
- Prospect geography: US, EU/EEA, Canada, other, or mixed.
- Data source / consent context: how contacts were sourced and whether consent exists.
- Sender details: sending domain, physical address.

## Procedure
1. **Determine prospect geography** → applicable law(s):
   - **US** → CAN-SPAM.
   - **EU/EEA** → GDPR.
   - **Canada** → CASL.
   - **Mixed** → apply the strictest overlap (usually CASL/GDPR consent-first).

2. **CAN-SPAM requirements** (US):
   - Truthful "From", "To", and routing information.
   - Subject line not misleading.
   - Clear and conspicuous opt-out mechanism honored within 10 business days.
   - Valid physical postal address in the email.
   - Identify the message as an advertisement if required.

3. **GDPR requirements** (EU/EEA):
   - Lawful basis for processing personal data: **consent** or **legitimate interest** (documented LIA required).
   - Right to object / opt-out must be as easy as opt-in.
   - Data minimization: only data necessary for the outreach.
   - If no lawful basis is documented, output is **BLOCKED**.

4. **CASL requirements** (Canada):
   - Express or implied consent before sending.
   - Clear sender identification and contact information.
   - Working unsubscribe mechanism honored within 10 business days.
   - If consent is absent, output is **BLOCKED**.

5. **Check each email**:
   - Opt-out link or reply-to-unsubscribe present.
   - Physical address present (US/CASL).
   - No misleading subject lines.
   - No purchased/scraped lists without documented lawful basis.

6. **Decision**:
   - **PASS**: all required elements present for the target geography.
   - **BLOCKED**: any hard requirement missing; output is not send-ready and a fix is prescribed.

## Compliance Decision Tree
```
Geography
├── US only
│   └── PASS if: truthful headers, clear opt-out, physical address
│   └── BLOCK if: missing opt-out or address
├── EU/EEA
│   └── PASS if: documented lawful basis + opt-out + data minimization
│   └── BLOCK if: no lawful basis or no opt-out
├── Canada
│   └── PASS if: consent basis documented + opt-out + sender ID + address
│   └── BLOCK if: no consent basis or missing opt-out
└── Mixed
    └── Apply strictest set; default to consent-first + opt-out + address
```

## Output Format
```markdown
## Compliance Verdict
- **Geography:** US + EU
- **Applicable law:** CAN-SPAM + GDPR (strictest: GDPR)
- **Required elements:** opt-out, lawful basis, physical address
- **Status:** BLOCKED
- **Missing:** documented lawful basis for EU contacts
- **Fix:** run a consent campaign or document a legitimate-interest assessment; do not send until basis is recorded.
- **Disclaimer:** This is informational guidance, not legal advice. Consult qualified counsel for your jurisdiction.
```

## Example
**Input:** Sequence targets EU contacts scraped from LinkedIn; no opt-in recorded.
**Output:** BLOCKED. Missing GDPR lawful basis. Prescribe: either obtain consent via a separate opt-in campaign or document a legitimate-interest assessment with an easy opt-out before any send.

## Quality Gate
- [ ] Opt-out + lawful basis verified for each geography, or output explicitly BLOCKED.
- [ ] Required elements are listed per applicable law.
- [ ] A concrete fix is prescribed when blocked.
- [ ] Disclaimer included that this is not legal advice.
