# Output schema

The skill output is a markdown localization matrix. Each row should compare one WHO source statement with one local policy statement or explicitly note that the local evidence is missing.

## Required table header

```md
| WHO source statement | Local policy statement | Alignment status | Difference type | Explanation | Evidence from WHO source | Evidence from local source | Confidence | Human review action |
|---|---|---|---|---|---|---|---|---|
```

## Field definitions

### WHO source statement

The source claim, recommendation, rule, or structured WHO component being assessed.

### Local policy statement

The matching local excerpt, or a clear note that no matching local statement was found in the provided material.

### Alignment status

One of the controlled categories from `context/localization-categories.md`.

### Difference type

A short label describing the main comparison issue, such as:

- `none`
- `scope difference`
- `missing element`
- `terminology difference`
- `restriction added`
- `conflict`
- `insufficient evidence`

### Explanation

A brief plain-language explanation of why the row received its alignment status.

### Evidence from WHO source

Quoted or closely paraphrased evidence tied to the provided WHO material.

### Evidence from local source

Quoted or closely paraphrased evidence tied to the provided local material. If none is present, say that no matching local evidence was found in the provided excerpt.

### Confidence

Allowed values:

- `High`
- `Medium`
- `Low`

### Human review action

Allowed values:

- `No action needed`
- `Confirm interpretation`
- `Check missing local evidence`
- `Resolve divergence`
- `Validate terminology mapping`
- `Escalate to clinical or policy expert`

## Validation expectations

The structural validator should check:

- the markdown file exists;
- the required table header is present;
- at least one data row exists;
- `Alignment status` uses a controlled value;
- `Confidence` uses `High`, `Medium`, or `Low`;
- `Human review action` uses an allowed value.

The validator must not claim to assess:

- clinical correctness;
- WHO policy correctness;
- national policy correctness;
- terminology correctness.

## Example empty table

```md
| WHO source statement | Local policy statement | Alignment status | Difference type | Explanation | Evidence from WHO source | Evidence from local source | Confidence | Human review action |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |
```
