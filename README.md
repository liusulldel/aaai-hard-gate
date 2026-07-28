# AAAI Hard Gate

AAAI Hard Gate is a Codex skill for researchers who want a conference paper checked as a scientific artifact, not polished as a sales pitch.

It turns an idea, draft, or revision into an auditable research package. The workflow fixes the scientific contract, maps novelty against primary sources, tests proofs and experiments together, and runs independent researcher-lens reviews against frozen evidence. It also checks notation, claim scope, reproducibility, readability, and release files.

## What it guards

- **Scientific claims:** Every headline claim needs a theorem, stored result, primary citation, or explicit limitation.
- **Reviewer simulations:** Researcher lenses use the same frozen evidence, preserve dissent, and never pose as real reviews or endorsements.
- **Theory and experiments:** Assumptions, counterexamples, seeds, raw outputs, figures, and hashes stay connected.
- **Writing quality:** The workflow defines jargon, audits notation, and removes formulaic prose after the science stabilizes.
- **Release integrity:** Tests, PDFs, archives, manifests, and deferred gates receive a final check before handoff.

## Use it when

Use the skill to develop or revise an AAAI, NeurIPS, ICML, ICLR, AAMAS, or similar submission; build a reviewer-conditioned revision loop; audit a technical manuscript; or package a reproducible paper and supplement.

Example prompt:

```text
Use $build-reviewer-conditioned-paper to turn this draft into a rigorous,
reviewer-tested AAAI submission package. Preserve failed studies, keep claims
within the evidence, and report every release gate as pass, fail, deferred, or
author action.
```

## Install

Copy `build-reviewer-conditioned-paper` into your Codex skills directory:

```bash
cp -R build-reviewer-conditioned-paper "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Start a new Codex task, then invoke `$build-reviewer-conditioned-paper`.

## Included

- A complete hard-gate workflow from intake through release
- A researcher-lens review protocol with ethical boundaries
- Templates for the PRD, claim ledger, source ledger, notation ledger, review actions, readability report, and release manifest
- A safe initializer that creates missing research records without overwriting existing work

## Scope

This is an independent research workflow. It is not affiliated with AAAI or any other venue. Simulated reviews do not represent named researchers, assigned reviewers, endorsements, or acceptance forecasts.
