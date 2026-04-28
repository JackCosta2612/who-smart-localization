# Repository structure

This repository is organized as a collection of localization skills rather than a single skill package.

## Root files

| Path | Purpose |
|---|---|
| `README.md` | Project overview, team workflow, and validator commands. |
| `SKILLS.md` | Index of available skills. |
| `docs/` | Cross-skill design notes. |
| `shared/` | Shared assets or materials that apply to more than one skill. |
| `skills/` | Individual Agent Skill packages. |

## Skill package convention

Each skill should follow this structure:

```text
skills/<skill-name>/
├── SKILL.md
├── README.md
├── context/
├── examples/
├── scripts/
└── tests/
```

## Current skills

| Skill | Status |
|---|---|
| `skills/country-profiling/` | First planned skill, scaffolded for implementation. |
| `skills/policy-comparison/` | Existing comparison skill moved into its own package. |

## Adding a new skill

When adding another skill:

1. Create `skills/<new-skill-name>/`.
2. Add a valid `SKILL.md` with frontmatter.
3. Keep long definitions in `context/`.
4. Put structural examples in `examples/`.
5. Put lightweight validation or helper code in `scripts/`.
6. Add evaluation notes or test cases in `tests/`.
7. Update the root `README.md` and `SKILLS.md`.
