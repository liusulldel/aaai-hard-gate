# AAAI-27 Hard Gate

Catch submission-format failures before they become desk-rejection reasons.

AAAI-27 Hard Gate is a fail-closed Codex skill for checking—and then fixing—an
AAAI 2027 main-track review submission against the official AAAI Author Kit,
submission instructions, and technical-track page rules. A successful LaTeX
build or OpenReview upload is not treated as proof of compliance.

## What it checks

- Official, unmodified `aaai2027.sty` and anonymous submission mode
- US-Letter geometry, two-column layout, margins, gutter, and page limits
- Pages 1–7 for all paper content and pages 8–9 for references only
- Forbidden LaTeX packages, spacing tricks, cropping, and table scaling
- PDF version, encryption, metadata, links, bookmarks, page rotation, and fonts
- Missing checklist, acknowledgments, author leaks, and source/PDF mismatch

## Plot and table hard gate

The skill also finds plot-format violations and drives the repair loop:

- Plot labels and in-figure text must be at least 9 pt at final placed size
- Raster graphics must be 300 dpi
- Fonts must be embedded, with no Type 3 or Identity encoding
- Lines must be at least 0.5 pt
- Contrast must exceed 4.5:1 and meaning must survive grayscale
- Figure callouts use Times Roman or Helvetica
- Captions stay below figures and tables in 10 pt Roman
- Graphics must be externally cropped, legible, and inside margins and gutter
- Tables use 10 pt Roman where possible, never below 9 pt, with no whole-table scaling

Automatic checks are combined with required rendered-page inspection. The gate
does not silently downgrade uncertain visual issues to advice.

## Install

Copy `aaai27-hard-gate` into your Codex skills directory:

```bash
cp -R aaai27-hard-gate "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Start a new Codex task and invoke `$aaai27-hard-gate`.

## Run

```bash
python3 aaai27-hard-gate/scripts/check_aaai27.py \
  --tex /absolute/path/main.tex \
  --pdf /absolute/path/main.pdf \
  --checklist /absolute/path/ReproducibilityChecklist.pdf
```

Fix every `FAIL`, inspect every `MANUAL` gate, add only attestations that were
actually verified, and rerun until the result is `PASS`.

## Authority and scope

The bundled rules were verified against the official AAAI-27 materials on
2026-07-27:

- [AAAI-27 Author Kit](https://aaai.org/authorkit27/)
- [AAAI-27 submission instructions](https://aaai.org/conference/aaai/aaai-27/submission-instructions/)
- [AAAI-27 Main Technical Track call](https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/)

The official AAAI materials remain authoritative if they change. This
independent tool is not affiliated with or endorsed by AAAI.
