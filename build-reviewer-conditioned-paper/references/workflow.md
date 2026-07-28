# Workflow and Gates

## Contents

1. Intake
2. Scientific contract
3. Prior work
4. Researcher lenses
5. Theory and experiments
6. Frozen review loop
7. Writing and notation
8. Release
9. Stopping rules

## 1. Intake

Inspect all manuscript, bibliography, code, data, figures, previous reviews, and release files. Preserve user changes. Record the venue, track, deadline, page limit, anonymity rule, and artifact policy from current official sources.

Classify the starting point:

- **Idea:** no fixed claim or model.
- **Specification:** PRD exists, paper does not.
- **Draft:** prose and formal claims exist.
- **Revision:** reviews or defect ledgers exist.
- **Release:** paper and artifact need final checks.

## 2. Scientific contract

Define the decision problem before the story. Record:

- state and support;
- target variable or outcome;
- observation and communication model;
- allowed decision rules;
- loss and evaluation measure;
- strategic actors and utilities, if any;
- intervention authority and failure semantics.

Create a concrete witness with two supported cases that expose the central distinction. Avoid analogy-only openings.

Write theorem obligations as testable contracts. Include assumptions, equality or boundary cases, counterexamples, and disallowed interpretations.

Gate: a cold reader can state what the system observes, predicts, chooses, and loses.

## 3. Prior work and novelty

Search primary literature by claim, formal object, proof technique, and application. Build a closest-work table. For each claimed contribution, record:

- nearest theorem or method;
- shared assumptions;
- changed assumptions;
- new object or operational use;
- allowed novelty language.

Gate: every contribution has a primary-source boundary and no unsupported “first” claim.

## 4. Researcher lenses

Build a balanced panel. Cover the paper's core mathematics, experiments, deployment setting, human factors, and governance. Verify current venue roles from official pages. Treat cited experts without verified roles as subject-matter lenses.

Build each dossier from primary sources. Infer stable preferences from repeated choices across several works, not one sentence. Record uncertainty and conflicts.

Gate: each lens has verified identity, source list, research-standard summary, likely objections framed as questions, and a non-impersonation note.

## 5. Theory and experiments

Develop theorem, proof, counterexample, and experiment in one cycle. Use code to test finite constructions and edge cases. Keep a notation ledger and claim ledger active from the first draft.

For experiments, prerecord:

- unit of analysis;
- sampling or enumeration rule;
- seed schedule;
- primary and secondary endpoints;
- exclusions;
- uncertainty method;
- failure handling;
- plot and table contract.

Separate exact finite audits, simulations, retrospective archive analyses, and prospective studies. Give each the claims it can support.

Gate: every number regenerates; every theorem assumption appears near its statement; every probability model has one name.

## 6. Frozen review loop

Freeze the main paper, supplement, claim ledger, PRD, experiment report, and artifact manifest. Hash the inputs. Give every reviewer lens the same evidence plus its dossier.

Require:

- absolute score before prior-round comparison;
- dimension scores and confidence;
- fatal-flaw status;
- strongest resolved and unresolved objections;
- credited and excluded evidence;
- exact evidence needed for the next score band.

Aggregate objections into a revision ledger. Prioritize correctness, then novelty, evidence, integration, and presentation. Reject revisions that improve rhetoric by weakening scope.

Freeze again after material work. Never rescore an unchanged bundle.

Gate: all stored reviews remain unchanged and the action ledger traces each revision to evidence.

## 7. Writing and notation

Run a notation audit before prose simplification. Define symbols, types, domains, aliases, and first-use locations. Add a plain-language glossary when the paper spans fields.

Run two prose cycles after formal stabilization:

1. Red team measures readability, term onboarding, cognitive load, passive voice, jargon, hedging, and specificity.
2. Blue team edits sentences, transitions, examples, and definitions.

Use the same metric implementation across rounds. Preserve necessary technical vocabulary. Treat AI-pattern tools as style heuristics.

Gate: the main paper carries the first-pass explanation burden; the supplement carries proof completeness.

## 8. Release

Rebuild from the frozen source. Run all tests and figure generation. Check page limits, anonymity, citations, references, fonts, PDF size, and LaTeX logs. Render and inspect every page.

Create source and artifact archives. Generate and verify hashes. Record passed, failed, deferred, and author-only actions in the release manifest.

Gate: the release contains one authoritative version of each deliverable and one honest manifest.

## 9. Stopping rules

Stop when:

- all required gates pass;
- a remaining gate requires new participants, authority, independent custody, or a fresh holdout;
- another review round would see the same evidence;
- a style gain would cost scientific precision;
- the user chooses a scoped release with documented deferrals.

State the strongest unresolved objection and the smallest new evidence package that could address it.
