# who-smart-localization

Model-neutral Agent Skills for WHO SMART Guidelines localization work.

This repository is part of a one-month, 3 ECTS university NLP project connected to WHO SMART Guidelines localization. Country Profiling is the currently active skill. Policy Comparison is planned after the Country Profiling package is stable enough to support source-backed examples and downstream comparison work.

## Project scope

The skills support preparation and review work for WHO SMART Guidelines and Digital Adaptation Kits (DAKs). They help organize sources, identify evidence gaps, and prepare structured outputs for human review.

Country Profiling creates a healthcare country profile. It is for any target
country where WHO / SMART / DAK content needs country-specific
contextualization before policy comparison or localization, not only for
countries missing from WHO databases. It does not perform policy alignment
analysis. Later, Policy Comparison should use the country profile as context
when comparing WHO/SMART content with national policy material.

The skills do not make clinical decisions, provide patient advice, draft final national policy, or replace WHO, national, legal, clinical, policy, WASH, epidemiological, environmental health, or country expert review.

Shared source artifacts used by multiple skills live under `shared/assets/`.
The repository currently includes `shared/assets/who-immunizations-dak.pdf` as
the shared WHO immunization DAK source for immunization-focused profiling
handoff and later Policy Comparison work.

## Repository structure

```text
.
├── README.md
├── SKILLS.md
├── docs/
│   └── repository-structure.md
├── shared/
│   └── assets/
└── skills/
    ├── country-profiling/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── context/
    │   ├── examples/
    │   ├── sourcing_scripts/
    │   └── tests/
    └── policy-comparison/
        ├── SKILL.md
        ├── README.md
        ├── context/
        ├── examples/
        ├── scripts/
        └── tests/
```

## Current skills

### Country Profiling

Status: active / MVP polish.

Creates a source-backed textual healthcare country profile covering country context, main health issues, health system organization, implementation environment, access and coverage, sanitary conditions, financing, workforce, infrastructure, digital health, equity, risks, and readiness for later policy comparison.

The preferred minimal input is a country name plus optional downstream focus.
The skill supports document-only profiling, deterministic script-assisted
retrieval for selected baseline indicators, reviewed source artifacts, and controlled
web-assisted retrieval when scripts are unavailable.

Path: `skills/country-profiling/`

### Policy Comparison

Status: planned / migrated starting point.

Will compare WHO/SMART content with national policy material after Country Profiling is stable. It should use country profile outputs as context.

Path: `skills/policy-comparison/`

## Examples and tests

Country Profiling includes a retrieval-assisted Italy reference example under
`skills/country-profiling/examples/italy-reference/`. It is a behavior-shaping
example for manual review, not a benchmark case or final policy evidence. Tests
and validators check structure only; they do not validate clinical correctness,
policy correctness, country facts, source interpretation, or WHO interpretation.

## Basic workflow

```bash
git checkout main
git pull origin main
git checkout -b short-description
```

After editing:

```bash
git status
git add .
git commit -m "Short description of change"
git push -u origin short-description
```

Open a pull request on GitHub for team review before merging.

## Local checks

Country profile validator:

```bash
python3 skills/country-profiling/sourcing_scripts/validate_profile.py --help
```

Policy comparison validator:

```bash
python3 skills/policy-comparison/scripts/validate_profile.py --help
```

Validators check structure only. They do not validate clinical correctness, policy correctness, country facts, source interpretation, or WHO interpretation.
