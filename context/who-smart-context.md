# WHO SMART Guidelines context

## What SMART Guidelines are

WHO SMART Guidelines are an effort to convert narrative health guidance into digital components that can be reused more consistently in health systems and software.

SMART stands for standards-based, machine-readable, adaptive, requirements-based, and testable guidance. In practice, this means moving from prose documents toward structured artifacts that support implementation.

## The L1 to L5 layers

### L1: Narrative guidance

Human-readable WHO recommendations and guideline text.

### L2: Digital Adaptation Kits

Structured operational content derived from guidance, such as workflows, personas, data elements, business rules, indicators, and functional requirements.

### L3: Machine-readable implementation guides

Formal representations of the guidance, often using standards such as HL7 FHIR and CQL.

### L4: Executable software tools

Applications and digital systems that implement the machine-readable guidance.

### L5: AI-supported dynamic systems

More adaptive or precision-oriented systems that may use AI to support guidance use, localization, or implementation.

## What localization means in this project

For this repository, localization means adapting WHO global guidance or SMART Guideline components to country-specific policy language, terminology, schedules, formularies, and implementation realities.

The task is comparative and traceable. It is not only translation. The team needs to understand whether local policy aligns with WHO intent, differs from it, adds constraints, or leaves gaps.

## Why human review is required

Localization decisions can affect policy interpretation, implementation choices, and ultimately health system behavior. Because of that:

- evidence must remain traceable to the provided source text;
- uncertainty must be surfaced, not hidden;
- ambiguous rows must be escalated to experts;
- the skill output should support review, not replace it.

This repository therefore treats the localization matrix as a structured review aid rather than a final authority.
