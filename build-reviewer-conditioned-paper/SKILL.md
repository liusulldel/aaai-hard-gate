---
name: build-reviewer-conditioned-paper
description: Build or revise rigorous conference research papers through a scientific PRD, primary-source novelty map, verified researcher-lens dossiers, frozen simulated-review rounds, proof and notation audits, reproducibility gates, and technical-prose humanization. Use when Codex needs to develop an AAAI, NeurIPS, ICML, ICLR, AAMAS, or similar submission; simulate editors or referees; distill research taste from papers, talks, or public writing; optimize a manuscript against several reviewer lenses; define jargon and notation; remove AI-writing patterns; or package an auditable paper, supplement, and artifact.
---

# Build a Reviewer-Conditioned Paper

Turn a research idea or draft into a scoped, evidence-backed submission. Treat reviewer simulations as adversarial editing tools. Never present them as external reviews, endorsements, or acceptance forecasts.

## Start

1. Inspect the repository, manuscript, experiments, prior reviews, and venue constraints.
2. Identify the current stage: idea, PRD, draft, revision, artifact, or release.
3. Read [references/workflow.md](references/workflow.md) before planning a full paper cycle.
4. Read [references/review-protocol.md](references/review-protocol.md) before creating researcher dossiers or running simulated reviews.
5. Read [references/templates.md](references/templates.md) before creating project records.
6. Run `scripts/init_pipeline.py` when the project lacks structured research records. Preserve existing files.
7. State which parts of the workflow will run in the current task. Do not imply that unexecuted phases are complete.

## Protect scientific integrity

- Fix the target variable, state support, loss, observation model, and system boundary before choosing a theorem.
- Separate norm definition, information sufficiency, incentives, and execution authority.
- Classify each result as classical, adapted, candidate-new, empirical, interpretive, or future work.
- Preserve failed studies, dissenting reviews, exclusions, and unmet gates.
- Reject score editing, target-mean prompting, evidence laundering, citation padding, and novelty inflation.
- Never count code correctness as efficacy evidence.
- Never convert retrospective or single-agent data into causal, population, deployment, or multi-principal claims.
- Stop rescoring an unchanged evidence bundle.

## Verify people and sources

Browse current official venue pages when the task depends on committee membership, track leadership, deadlines, policies, or formatting. Prefer official conference sources.

For each named researcher:

1. Verify identity, spelling, affiliation, and role.
2. Separate verified organizers or committee members from cited authors and subject-matter lenses.
3. Record conflicts when known.
4. Build the dossier from primary papers, books, technical reports, recorded talks, and first-party public writing.
5. Attach a source to each inferred research preference.
6. Mark uncertain inferences as questions, not facts.
7. Add a non-impersonation statement.

Do not claim that a plausible lens is an assigned reviewer. Do not predict that a named person will accept, reject, champion, or endorse the paper.

## Write the scientific contract

Create a PRD that fixes:

- the research question and falsifiable witness;
- formal objects and assumptions;
- theorem obligations and counterexamples;
- experiment modules and acceptance criteria;
- page, anonymity, citation, and artifact requirements;
- claim boundaries and explicit deferrals;
- review, readability, and release gates;
- stopping rules.

Map each headline sentence to a theorem, stored result, primary citation, or limitation. Remove sentences without evidence owners.

## Build theory and evidence together

- Maintain one notation ledger across the main paper, supplement, figures, and code.
- Give each displayed formula its symbols, assumptions, operational meaning, and non-implications.
- Test general statements with adversarial counterexamples.
- Connect every empirical number to a stored row or deterministic computation.
- Keep theorem and experiment probability models distinct when they differ.
- Maintain a claim ledger that controls abstract and conclusion wording.
- Freeze seeds, dependencies, raw outputs, derived summaries, figures, and hashes.

## Run reviewer-conditioned optimization

Use at least five independent research lenses for a serious review cycle. Use eight to twelve when the user requests a broad panel.

Treat the loop as constrained black-box optimization:

- **State:** one frozen evidence bundle.
- **Reviewer functions:** source-grounded research lenses.
- **Reward:** a vector of correctness, novelty, evidence, integration, venue fit, reproducibility, and clarity.
- **Action:** a bounded revision tied to a recorded objection.
- **Transition:** a rebuilt and newly frozen bundle.
- **Constraints:** the PRD, claim ledger, page limit, and evidence-integrity rules.

Give each reviewer the same bundle and one dossier. Hide peer scores and target means. Require an absolute score before showing that lens's prior-round review. Preserve every review unchanged. Aggregate defects by scientific issue.

Use subagents only when the user requests them or the active collaboration rules allow them. Give each subagent the raw frozen bundle, one dossier, and the common rubric. Do not leak intended scores or other reviewers' conclusions.

Revise after the panel. Rebuild proofs, experiments, figures, and release records when a change touches them. Start another round only after a material evidence or manuscript change.

## Audit notation and jargon

For every symbol, record its meaning, type, domain, first definition, scope, and collisions. Define specialized terms before use. Distinguish graph objects, probability measures, and similarly named risks.

Run these checks:

- undefined or overloaded symbols;
- inconsistent aliases;
- missing assumptions near theorem statements;
- unexplained acronyms and graph names;
- formulas without plain-language interpretations;
- main-paper and supplement drift;
- LaTeX labels, citations, environments, and compilation errors.

Keep notation that carries technical meaning. Remove decorative symbols, private tags, drafting markers, and unexplained shorthand.

## Humanize after correctness stabilizes

Run two red-team and blue-team prose rounds. Measure readability with the same extractor and heuristics across rounds. Treat scores as directional comparisons, not authorship tests.

Improve:

- first-pass comprehension;
- term onboarding;
- sentence rhythm and transitions;
- cognitive load;
- specificity and scope discipline;
- human voice.

Remove theorem-inventory abstracts, rebuttal language, drafting history, stock AI phrases, staged rhetorical questions, repetitive binary contrasts, stylistic em dashes, and passive constructions that hide actors. Preserve necessary hedges, citations, formulas, and domain terms.

Use an available AI-writing audit skill when present. Report its output as a heuristic pattern check, never as proof of human authorship.

## Freeze the release

Compile every deliverable from the frozen source. Run tests, regenerate figures, inspect logs, render every PDF page, check fonts and page size, create archives, and verify hashes.

Report each gate as pass, fail, deferred, or author action. Do not call the project complete while a required gate remains unmet.

## Deliver

Return:

1. the updated paper or research records;
2. a concise change summary;
3. passed and failed gates;
4. the strongest unresolved scientific objection;
5. the exact evidence needed for the next material round;
6. links to the release files.

Avoid promising an acceptance probability from simulated reviews.

## Resources

- [references/workflow.md](references/workflow.md): phase-by-phase gates and stopping rules.
- [references/review-protocol.md](references/review-protocol.md): dossier schema, reviewer rubric, and frozen-round controls.
- [references/templates.md](references/templates.md): reusable PRD, ledger, review, readability, and release templates.
- `scripts/init_pipeline.py`: create missing research-pipeline records without overwriting existing work.
