# Country Profiling Skill

The Country Profiling skill creates a structured country context profile for DAK implementation and later localization work.

The first use case is:

> Given a country name and target health domain, produce a structured, verifiable profile of that country's health system relevant to DAK implementation, drawing from DAK material, WHO/open data sources, and national health documents, while flagging what is known, uncertain, and requiring expert input.

## What this skill supports

- Faster discovery of country context before detailed localization.
- Reduced mapping errors by separating facts, sources, assumptions, and unknowns.
- Regional reuse by making country context comparable across countries.
- Better handoff into later skills, especially Policy Comparison.

## Folder structure

```text
country-profiling/
├── SKILL.md
├── README.md
├── context/
│   ├── input-documentation.md
│   ├── mcp-integration-plan.md
│   ├── profile-schema.md
│   └── who-data-retrieval.md
├── examples/
│   ├── example-input-1.md
│   └── example-output-1.md
├── scripts/
│   ├── validate_profile.py
│   └── who_gho_client.py
└── tests/
    ├── evaluation-notes.md
    └── test-case-1.md
```

## Current status

This is scaffolding for the first implementation pass. It defines the expected inputs, output profile structure, WHO source retrieval guidance, an MCP implementation plan, and basic structural validation.
