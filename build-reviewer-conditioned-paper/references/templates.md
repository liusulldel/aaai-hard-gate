# Research Record Templates

## Contents

1. PRD
2. Claim ledger
3. Source ledger
4. Notation ledger
5. Review action ledger
6. Readability report
7. Release manifest

## 1. PRD

```markdown
# Scientific PRD

## Objective
## Venue and constraints
## Falsifiable opening witness
## Formal objects and assumptions
## Required theorems and counterexamples
## Experiment contract
## Artifact contract
## Page and format gates
## Claim boundaries
## Explicit deferrals
## Review protocol
## Definition of done
```

## 2. Claim ledger

```markdown
| ID | Claim | Class | Assumptions | Evidence | Allowed wording | Disallowed wording | Status |
|---|---|---|---|---|---|---|---|
```

Use classes: classical, adapted, candidate-new, exact artifact result, descriptive result, interpretation, limitation, future work.

## 3. Source ledger

```markdown
| Claim or topic | Primary source | Stable link | Verified facts | Inference | Citation status |
|---|---|---|---|---|---|
```

## 4. Notation ledger

```markdown
| Symbol or term | Meaning | Type and domain | First definition | Scope | Collision or jargon note |
|---|---|---|---|---|---|
```

## 5. Review action ledger

```markdown
| Issue | Lenses raising it | Severity | Evidence | Revision | Verification | Status |
|---|---|---:|---|---|---|---|
```

## 6. Readability report

```markdown
# Readability Report

## Method and extractor
## Baseline
## Red-team findings
## Blue-team changes
## Round 1 scores
## Round 2 scores
## AI-pattern heuristic
## Preserved technical terms
## LaTeX and visual checks
```

Track Flesch, Flesch-Kincaid, Fog, SMOG, nominalizations, passive voice, jargon, hedges, specificity, and a clearly labeled cohesion proxy. Do not report a local proxy as an official Coh-Metrix, TAACO, or TAALES score.

## 7. Release manifest

```markdown
# Release Manifest

## Submission files
## Source and artifact freeze
## Seeds, data, and tests
## Figure inventory
## Scientific gates
## Failed and invalid studies
## Deferred claims
## Reviewer-simulation status
## Author actions
## SHA-256 verification
```
