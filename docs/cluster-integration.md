# Cluster Integration — marketing-content-branding

This skill belongs to the `marketing-content-branding` cluster. Two reusable sub-skills and one shared quality gate are designed to be consumed by sibling ideas in the cluster, especially **idea 151** and **idea 72**.

## Shared sub-skills

### `sub-audience-analysis.md`
**Reusable for:** any marketing or content skill that needs an ICP, segments, and fillable personalization variables.

**Contract:**
- Inputs: offer/value proposition, target market, optional account/contact list.
- Outputs: ICP summary + segment table with pain → benefit → personalization variable → data source.
- Quality gate: ≥1 fillable variable per segment.

**Integration note for ideas 151 and 72:** import this sub-skill when the parent task starts with audience definition. It produces the same segment table format, so downstream sequence or content generators can consume `{{tokens}}` directly.

### `sub-compliance-check.md`
**Reusable for:** any outbound or content-distribution skill that touches email, SMS, or direct messages.

**Contract:**
- Inputs: sequence/copy + prospect geography + consent context.
- Outputs: PASS / BLOCKED verdict with law-specific required elements and fixes.
- Quality gate: opt-out + lawful basis present, or output explicitly BLOCKED.

**Integration note for ideas 151 and 72:** wire this gate before emitting any send-ready copy. If the sibling idea targets EU/Canada, this gate provides the GDPR/CASL decision tree automatically.

### `sub-quality-reviewer.md`
**Reusable for:** any persuasive copy task across the cluster.

**Contract:**
- Inputs: draft copy.
- Outputs: issues list + ≥2 A/B variants + experiment suggestions.
- Quality gate: no unverified claims, no dark patterns, ≥2 variants.

## How to reference these sub-skills from another idea

In the parent skill's `main.md`, list the shared sub-skill under **Sub-skills Available** and describe the hand-off in the workflow:

```markdown
## Sub-skills Available
- `../cold-email-outreach-at-scale/skills/sub-audience-analysis.md` — shared audience segmentation.
- `../cold-email-outreach-at-scale/skills/sub-compliance-check.md` — shared compliance gate.
- `../cold-email-outreach-at-scale/skills/sub-quality-reviewer.md` — shared copy review.

## Workflow
1. Use `sub-audience-analysis` to define ICP and segments.
2. Generate copy with your idea-specific sub-skill.
3. Run `sub-compliance-check` before sending.
4. Run `sub-quality-reviewer` for variants and issue checking.
```

## Knowledge reuse
`SECOND-KNOWLEDGE-BRAIN.md` in this repository is kept current by `tools/knowledge_updater.py`. Sibling ideas can reference it as the cluster's deliverability and anti-spam knowledge base rather than duplicating citations.

## Avoiding duplication
- Do **not** recreate an audience-analysis sub-skill if this one covers the use case.
- Do **not** implement a separate spam/compliance gate unless the channel (e.g., SMS) has materially different laws.
- Do reuse `sub-quality-reviewer.md` for any persuasive copy variant generation to keep A/B variant standards consistent across the cluster.
