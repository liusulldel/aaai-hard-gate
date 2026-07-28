#!/usr/bin/env python3
"""Create missing research-pipeline records without overwriting existing work."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


TEMPLATES = {
    "PRD.md": """# Scientific PRD

Created: {today}
Working title: {title}
Venue: {venue}
Track: {track}

## Objective

## Falsifiable opening witness

## Formal objects and assumptions

## Required theorems and counterexamples

## Experiment contract

## Artifact contract

## Page and format gates

## Claim boundaries

## Explicit deferrals

## Review protocol

Target lens count: {reviewers}

## Definition of done
""",
    "CLAIM_LEDGER.md": """# Claim Ledger

| ID | Claim | Class | Assumptions | Evidence | Allowed wording | Disallowed wording | Status |
|---|---|---|---|---|---|---|---|
""",
    "SOURCE_LEDGER.md": """# Source Ledger

| Claim or topic | Primary source | Stable link | Verified facts | Inference | Citation status |
|---|---|---|---|---|---|
""",
    "REVIEWER_LEDGER.md": """# Researcher-Lens Ledger

These are internal research lenses, not external reviews or endorsements.

| ID | Verified name | Role category | Official source | Dossier | Conflict note | Status |
|---|---|---|---|---|---|---|
""",
    "NOTATION_LEDGER.md": """# Notation and Jargon Ledger

| Symbol or term | Meaning | Type and domain | First definition | Scope | Collision or jargon note |
|---|---|---|---|---|---|
""",
    "ROUND_ACTIONS.md": """# Review Round Actions

## Frozen evidence

## Aggregate

## Strongest resolved objection

## Strongest unresolved objection

| Issue | Lenses | Severity | Evidence | Revision | Verification | Status |
|---|---|---:|---|---|---|---|
""",
    "READABILITY_REPORT.md": """# Readability Report

## Method and extractor

## Baseline

## Round 1

## Round 2

## AI-pattern heuristic

## Preserved technical terms

## LaTeX and visual checks
""",
    "RELEASE_MANIFEST.md": """# Release Manifest

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
""",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Project root")
    parser.add_argument("--folder", default="research_pipeline", help="Record folder name")
    parser.add_argument("--title", default="Untitled research paper")
    parser.add_argument("--venue", default="Unspecified venue")
    parser.add_argument("--track", default="Unspecified track")
    parser.add_argument("--reviewers", type=int, default=8)
    parser.add_argument("--create-root", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.reviewers < 1:
        raise SystemExit("--reviewers must be positive")

    root = args.root.expanduser().resolve()
    if not root.exists():
        if not args.create_root:
            raise SystemExit(f"Project root does not exist: {root}")
        if not args.dry_run:
            root.mkdir(parents=True)

    target = root / args.folder
    paths = [target / name for name in TEMPLATES]
    dirs = [target, target / "reviewers", target / "rounds"]

    if args.dry_run:
        for path in dirs:
            print(f"DIR  {path}")
        for path in paths:
            state = "KEEP" if path.exists() else "CREATE"
            print(f"{state:6} {path}")
        return 0

    for path in dirs:
        path.mkdir(parents=True, exist_ok=True)

    values = {
        "today": date.today().isoformat(),
        "title": args.title,
        "venue": args.venue,
        "track": args.track,
        "reviewers": args.reviewers,
    }
    created = 0
    kept = 0
    for name, template in TEMPLATES.items():
        path = target / name
        if path.exists():
            print(f"KEEP   {path}")
            kept += 1
            continue
        path.write_text(template.format(**values), encoding="utf-8")
        print(f"CREATE {path}")
        created += 1

    print(f"Created {created}; preserved {kept}; records at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
