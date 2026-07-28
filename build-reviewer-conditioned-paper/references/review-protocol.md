# Researcher-Lens Review Protocol

## Contents

1. Ethical boundary
2. Dossier construction
3. Evidence freeze
4. Common rubric
5. Independent review prompt
6. Aggregation

## 1. Ethical boundary

Describe every output as a profile-conditioned internal simulation. State that the named researcher did not write, approve, or endorse it. Do not infer assigned-reviewer status from expertise, citations, or committee history.

## 2. Dossier construction

Use this schema:

```markdown
# Researcher lens: [verified name]

## Identity and role
- Verified name:
- Affiliation and date:
- Role category:
- Official-role source:
- Conflict note:

## Primary sources
| Source | Year | Venue | Relevant method or concern |
|---|---:|---|---|

## Repeated research standards
- Problems emphasized:
- Formal methods favored:
- Evidence favored:
- Constructive bar:
- Scope or governance concerns:

## Questions this lens should press
1.
2.
3.

## Uncertainty
- Inferences with weak support:

## Disclosure
This dossier models a research lens from public sources. It does not represent the researcher's views or participation.
```

Verify titles, authors, years, venues, links, and names. Use talks and public writing to supplement technical papers, not replace them.

## 3. Evidence freeze

Create a manifest with file paths and SHA-256 hashes. Give every lens the same bundle. Exclude unpublished diagnostics, future plans, peer scores, desired means, and post-freeze changes.

If a failed study produced no valid result, include the failure record and exclude hidden or partial outcomes.

## 4. Common rubric

Adapt weights to the venue before Round 1, then freeze them. A general theory-and-systems rubric is:

| Dimension | Weight |
|---|---:|
| Correctness and formal rigor | 20% |
| Novelty and field contribution | 20% |
| Empirical validity and grounding | 20% |
| Constructive integration | 15% |
| Venue and track significance | 10% |
| Reproducibility and claim discipline | 10% |
| Clarity and presentation | 5% |

Define score anchors. Do not use “9” as a command. Example anchors:

- 5: major correctness or contribution problems.
- 7: credible paper with substantial revision needs.
- 8: strong paper with one clear ceiling.
- 9: exceptional evidence and field-level contribution.
- 10: rare, near-definitive work.

## 5. Independent review prompt

Require the reviewer to:

1. read only the frozen bundle and one dossier;
2. disclose the simulation boundary;
3. score each dimension with evidence;
4. set the overall score before reading its own prior review;
5. identify fatal flaws;
6. name the strongest resolved objection;
7. name the strongest unresolved objection;
8. list evidence credited and excluded;
9. state the smallest evidence package that would change the verdict;
10. report confidence.

Do not show peer scores, target scores, or desired outcomes.

## 6. Aggregation

Check arithmetic and disclosures. Group objections by issue:

- correctness;
- novelty;
- external grounding;
- integrated mechanism;
- venue fit;
- reproducibility;
- clarity.

Create one action ledger with issue, evidence, proposed change, owner, verification method, and status. Preserve dissent. Report means and ranges only after the scientific objections.

Start a new round only after a material frozen change. Stop when every remaining ceiling requires new external evidence.
