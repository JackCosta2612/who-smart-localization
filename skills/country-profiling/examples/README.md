# Country Profiling reference examples

These folders contain draft reference examples for the Country Profiling skill.
They are behavior-shaping examples, not a benchmark, test suite, or gold-standard
evaluation set.

Use them to see how a country profile request should be normalized, how the
profile schema should be filled, how sources and gaps should be represented, and
where the profile should stop before WHO-versus-country policy comparison.

The structural validator may be run on `reference-output.md` files as a sanity
check, but passing validation is not the main purpose of these examples. The
main purpose is to reduce variance in agent behavior during real skill use.

## Italy drafts

| Draft | Focus | Best used to demonstrate |
|---|---|---|
| `italy-reference-draft-1/` | Broad health-system overview | A balanced country profile covering system organization, access, financing, workforce, infrastructure, digital health, equity, risks, and downstream readiness. |
| `italy-reference-draft-2/` | Immunization-oriented country profile | How to prepare for later immunization policy comparison while still producing a country profile rather than a policy comparison. |
| `italy-reference-draft-3/` | Policy-comparison handoff style | A conservative, gap-oriented profile that explicitly identifies source classes, constraints, uncertainties, and handoff actions for the future Policy Comparison skill. |

Each draft contains:

- `input.md`: a realistic user request that should activate the skill;
- `reference-output.md`: a concise source-backed output pattern following `context/profile-schema.md`;
- `source-notes.md`: source rationale and proposed follow-up source work;
- `agent-behavior-notes.md`: what behavior the draft is meant to enforce, including where it stops before policy comparison.

## Use guidance

Before drafting a new country profile, consult the closest example for the
requested use case. Imitate the structure, source discipline, uncertainty
handling, and handoff framing. Do not copy country facts into a different
country, and do not treat these drafts as final WHO or national policy evidence.
