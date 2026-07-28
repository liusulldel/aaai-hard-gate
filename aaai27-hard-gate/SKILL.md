---
name: aaai27-hard-gate
description: Run a fail-closed AAAI-27 submission-format gate against LaTeX source, the compiled review PDF, figures/tables, and the reproducibility checklist. Use when asked to validate, preflight, lint, audit, or hard-check an AAAI 2027 paper for page limits, anonymity, official style integrity, forbidden LaTeX, US-Letter geometry, PDF/font integrity, and official graphics requirements such as 9 pt plot text, 300 dpi raster art, captions, contrast, line width, and margin safety.
---

# AAAI-27 Hard Gate

Validate against the AAAI-27 main-track review-submission rules current on 2026-07-27. Treat the official website and Author Kit as authoritative when they conflict with this skill.

## Run the gate

1. Identify the main `.tex`, compiled review `.pdf`, reproducibility-checklist file, and local `aaai2027.sty` when present.
2. Run:

```bash
python3 <skill-dir>/scripts/check_aaai27.py \
  --tex /absolute/path/main.tex \
  --pdf /absolute/path/main.pdf \
  --checklist /absolute/path/ReproducibilityChecklist.pdf
```

3. Fix every `FAIL`. Do not reinterpret a failure as advice.
4. Resolve every `MANUAL` item through direct inspection. Read [official-gates.md](references/official-gates.md) before deciding borderline cases.
5. Rerun with only the attestations actually verified, for example:

```bash
python3 <skill-dir>/scripts/check_aaai27.py \
  --tex /absolute/path/main.tex \
  --pdf /absolute/path/main.pdf \
  --checklist /absolute/path/ReproducibilityChecklist.pdf \
  --attest layout --attest anonymity --attest title-case \
  --attest figures --attest tables --attest checklist-complete \
  --attest source-pdf-match \
  --attest references-only --attest official-style
```

Omit `references-only` when the PDF has at most seven pages. Omit `official-style` when the checker verifies a local `aaai2027.sty` hash. Never pass an attestation without inspecting that item.

## Interpret the result

- `PASS` / exit `0`: no automatic failures and no unresolved manual gates.
- `FAIL` / exit `1`: at least one blocker exists.
- `INPUT OR TOOL ERROR` / exit `2`: the gate could not execute reliably.
- `MANUAL REVIEW REQUIRED` / exit `3`: automatic checks passed, but required attestations remain.

Use `--json` for machine-readable output. A successful OpenReview upload or successful LaTeX compilation does not replace this gate.

## Manual inspection

Render the PDF pages when needed. Verify:

- `layout`: two-column AAAI layout; no text, equations, tables, or figures cross margins or the gutter; no headers, footers, page numbers, or visible squeezing.
- `anonymity`: no author names, affiliations, acknowledgments, identifying self-references, deanonymizing URLs, or other identity leaks.
- `title-case`: the title follows Chicago Title Case.
- `figures`: render at final paper size and verify every official graphics requirement: in-figure labels/text are at least 9 pt; captions are below in 10 pt Roman; raster art is 300 dpi; formats are JPG/PNG/PDF; callouts use Times Roman or Helvetica; fonts are embedded with no Type 3 or Identity encoding; strokes are at least 0.5 pt; WCAG contrast is greater than 4.5:1; meaning survives grayscale and does not rely on color; figures are legible, externally cropped, inside margins/gutter, and compliant for non-Roman scripts.
- `tables`: verify 10 pt Roman table text, with 9 pt the absolute minimum only when necessary; captions are below in 10 pt Roman; no whole-table resize/scaling is used; tables are legible and stay inside margins/gutter.
- `references-only`: when the PDF exceeds seven pages, every item on pages 8–9 is a reference entry—no main text, body sections, floats, figures, tables, algorithms, proofs, appendices, or extra content. Main body content MUST fit strictly within pages 1–7; spilling any main text onto Page 8 is a hard gate violation resulting in desk rejection.
- `checklist-complete`: the separate reproducibility checklist is complete and matches the paper.
- `source-pdf-match`: the supplied TeX source is the source that produced the checked PDF; spot-check the title, section order, figures, and final content.
- `official-style`: when no local style file was hash-checked, confirm the build resolved the official 2027.1 style without modification.

Treat every numerical graphics threshold above as a hard requirement even though PDF/source analysis cannot prove all of them automatically. Never pass `--attest figures` or `--attest tables` from source inspection alone.

## Scope

Apply this skill to the AAAI-27 main technical track review submission. Track-specific calls may differ. Recheck the official site if the user targets AI Alignment, AI for Social Impact, EAAI, IAAI, a camera-ready paper, or a later AAAI year.
