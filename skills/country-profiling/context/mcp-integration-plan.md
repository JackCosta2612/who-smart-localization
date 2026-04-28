# MCP integration assessment and plan

## Recommendation

MCP integration is recommended later, but it should not be required for the first prototype.

The Country Profiling skill can produce useful profiles from plain documents and open WHO data APIs. MCP becomes valuable when the project needs structured access to SMART/FHIR artifacts, terminology services, ValueSet expansion, CodeSystem lookup, or ImplementationGuide context.

## Why MCP is useful

Country profiling needs to connect country context to DAK implementation. When DAKs are available as SMART Implementation Guides or FHIR packages, MCP tools could help retrieve structured artifacts rather than relying only on PDF or HTML extraction.

Potential MCP-supported tasks:

- inspect ImplementationGuide metadata;
- list available PlanDefinition, ActivityDefinition, ValueSet, CodeSystem, Questionnaire, and StructureMap resources;
- expand ValueSets relevant to a DAK;
- look up code meanings;
- identify terminology bindings that may need country adaptation;
- map DAK data elements to country-specific terminology candidates;
- flag unresolved terminology or workflow dependencies for human review.

## Candidate MCP source

The project prompt identified this server as relevant:

```text
https://github.com/DigitalSQR/smart-mcp-server
```

This should be evaluated as a later implementation task before being treated as a project dependency.

## Proposed implementation phases

### Phase 1: No MCP dependency

- Keep the skill model-neutral.
- Use provided documents, WHO pages, and the GHO OData helper script.
- Store MCP requirements as documentation only.

### Phase 2: MCP discovery spike

- Install and run the SMART MCP server in a disposable environment.
- List available tools and resources.
- Test read-only operations against one public SMART Implementation Guide.
- Document required configuration, authentication, and data inputs.

### Phase 3: Read-only integration

- Add a wrapper script or usage note for read-only MCP calls.
- Retrieve ImplementationGuide metadata and artifact lists.
- Export MCP responses into markdown or JSON evidence files.
- Keep all outputs traceable to artifact IDs and versions.

### Phase 4: Terminology support

- Add optional workflows for ValueSet expansion and CodeSystem lookup.
- Compare DAK terminology needs with country terminology sources supplied by the user.
- Flag uncertain mappings for expert validation.

## Proposed scaffold

Future MCP files can be added under:

```text
skills/country-profiling/mcp/
├── README.md
├── smart-mcp-config.example.json
└── sample-queries.md
```

These files should remain examples until the team confirms the MCP server and the expected deployment environment.

## Safety rules

- Use MCP read-only at first.
- Do not treat FHIR terminology matches as policy decisions.
- Record artifact version, package URL, retrieval date, and tool output.
- Keep MCP-derived facts separate from human-authored country policy documents.
