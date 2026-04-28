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

## Predefined WHO retrieval task

When this skill is called, the Agent should run the WHO retrieval task before drafting the country profile:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py --country "<country>" --domain "<health-domain>"
```

The task writes a markdown and JSON retrieval bundle. It fetches candidate WHO source pages, saves text snapshots and link inventories, downloads supported linked documents when safely sized, looks up WHO GHO country metadata when possible, retrieves selected country-filtered GHO data samples, and records skipped or failed retrievals as explicit evidence gaps.

To check the runtime first:

```bash
python3 skills/country-profiling/scripts/check_environment.py
```

The MVP uses only Python standard library modules.
