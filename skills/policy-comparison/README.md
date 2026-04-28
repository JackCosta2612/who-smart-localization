# Policy Comparison Skill

The Policy Comparison skill compares WHO source content with country-specific policy material and produces a traceable localization matrix for human review.

This skill is now one skill inside a larger multi-skill localization repository. It should be used after the team has enough country context, often produced by the Country Profiling skill.

## What this skill supports

- Compare WHO guidance or DAK components with local policy excerpts.
- Classify alignment, partial alignment, divergence, missing content, or expert-review cases.
- Preserve evidence from WHO and local sources.
- Produce a structured matrix that can be reviewed by policy, clinical, or implementation experts.

## Folder structure

```text
policy-comparison/
├── SKILL.md
├── README.md
├── context/
├── examples/
├── scripts/
└── tests/
```

## Validator

Run from the repository root:

```bash
python3 skills/policy-comparison/scripts/validate_matrix.py skills/policy-comparison/examples/example-output-1.md
```
