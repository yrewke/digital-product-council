#!/usr/bin/env python3
"""Import old restaurant council memory into the Codex Council V2 library.

This is a provenance-preserving import. It copies historical artifacts into a
V2-local read-only archive and creates a compact evidence index that future V2
runs can inspect before asking for new research.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
LIBRARY = ROOT / "library"
IMPORT_ROOT = LIBRARY / "legacy-council-import"
ARCHIVE = IMPORT_ROOT / "source-archive"

LEGACY_INPUTS = [
    REPO / "handoffs" / "company-memory.md",
    REPO / "working" / "cache",
    REPO / "working" / "council-runs",
    REPO / "working" / "dry-runs",
    REPO / "working" / "ledgers",
]

RUNS = [
    {
        "run_id": "2026-06-13-commercial-council-001",
        "role": "initial commercial validation council",
        "next": "Run 2 should test a bounded primary-validation pilot portfolio.",
    },
    {
        "run_id": "2026-06-14-restaurant-roi-fulfillment-economics-002A",
        "role": "early ROI and fulfillment economics pass",
        "next": "Superseded by 002A-redo for final ROI memory.",
    },
    {
        "run_id": "2026-06-14-full-restaurant-roi-research-calculator-002A-redo",
        "role": "ROI boundaries, calculator model, and measured-value gates",
        "next": "Run 2B packaging work is ready using the ROI jobs and restrictions.",
    },
    {
        "run_id": "2026-06-14-feature-packaging-decision-002B",
        "role": "final packaging decision for base tiers and gated modules",
        "next": "Run 2C can price the chosen scope and obligations.",
    },
    {
        "run_id": "2026-06-14-pricing-and-commercial-justification-002C",
        "role": "internal pricing hypothesis and commercial justification",
        "next": "Run 003 should build internal sales/proposal/discovery deliverables.",
    },
]

HIGH_VALUE_FILES = {
    "RUN_001_COMPLETION_REPORT.md",
    "RUN_002A_REDO_COMPLETION_REPORT.md",
    "RUN_002B_COMPLETION_REPORT.md",
    "RUN_002C_COMPLETION_REPORT.md",
    "NEXT_SESSION_HANDOFF.md",
    "RUN_2B_HANDOFF.md",
    "RUN_2C_PRICING_HANDOFF.md",
    "RUN_003_SALES_DELIVERABLES_HANDOFF.md",
    "PRICING_FINAL_VERDICT.md",
    "PACKAGING_FINAL_VERDICT.md",
    "CHAIRMAN_FINAL_ROI_VERDICT.md",
    "ROI_AND_FULFILLMENT_VERDICT.md",
    "EVIDENCE_LEDGER.md",
    "SOURCE_LEDGER.md",
    "ASSUMPTION_LEDGER.md",
    "RESEARCH_LEDGER.md",
    "NUMBER_LEDGER.md",
    "PRICING_LEDGER.md",
    "PACKAGE_LEDGER.md",
    "RESPONSIBILITY_LEDGER.md",
    "PROVIDER_COST_LEDGER.md",
    "MODULE_PRICING_LEDGER.md",
    "ALLOWANCE_LEDGER.md",
    "HOSTING_RESPONSIBILITY_LEDGER.md",
    "CUSTOM_QUOTE_LEDGER.md",
    "COMPETITOR_LEDGER.md",
    "PRICE_CARD_DRAFT_INTERNAL.md",
    "PRICING_BASIS_MAP.md",
    "PROVIDER_COST_AND_ALLOWANCE_MODEL.md",
    "ALLOWANCES_AND_OVERAGES.md",
    "HOSTING_AND_RESPONSIBILITY_PRICING_OPTIONS.md",
    "COMPETITOR_PRICE_AND_SCOPE_COMPARISON.md",
    "CHEAP_WORDPRESS_COMPETITOR_JUSTIFICATION.md",
    "ROI_CALCULATOR_SPEC.md",
    "ROI_CALCULATOR_MODEL.csv",
    "ROI_OWNER_QUESTIONNAIRE.md",
    "RESTAURANT_ARCHETYPE_ROI_MATRIX.md",
    "FULL_RESTAURANT_ROI_MAP.md",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def archive_rel(path: Path) -> str:
    return path.relative_to(LIBRARY).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def normalize_key(text: str) -> str:
    words = re.findall(r"[a-z0-9]+", text.lower())
    stop = {"the", "and", "for", "with", "from", "into", "run", "council"}
    return "-".join(w for w in words if w not in stop)[:120] or "legacy-memory"


def classification_for(path: Path) -> str:
    name = path.name.upper()
    if "SOURCE" in name or "EVIDENCE" in name or "RESEARCH" in name:
        return "INTERNAL_PROJECT_FACT"
    if "ASSUMPTION" in name or "SCENARIO" in name or "HYPOTHESIS" in name:
        return "SCENARIO_ASSUMPTION"
    if "FINAL_VERDICT" in name or "COMPLETION_REPORT" in name or "HANDOFF" in name:
        return "INTERNAL_PROJECT_FACT"
    if "PRICING" in name or "PRICE" in name:
        return "SCENARIO_ASSUMPTION"
    return "COUNCIL_INFERENCE"


def title_for(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").title()


def copy_inputs() -> list[dict[str, object]]:
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, object]] = []
    for source in LEGACY_INPUTS:
        if not source.exists():
            continue
        if source.is_file():
            files = [source]
        else:
            files = [p for p in source.rglob("*") if p.is_file()]
        for path in sorted(files):
            relative = path.relative_to(REPO)
            dest = ARCHIVE / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                os.chmod(dest, 0o700)
            shutil.copy2(path, dest)
            manifest.append(
                {
                    "original_path": relative.as_posix(),
                    "archive_path": archive_rel(dest),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                    "classification": classification_for(path),
                }
            )
    return manifest


def run_for_path(path: str) -> str | None:
    for run in RUNS:
        if run["run_id"] in path:
            return run["run_id"]
    return None


def extract_summary(path: Path) -> str:
    text = read_text(path)
    lines: list[str] = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("#") or stripped.startswith("- ") or stripped.startswith("|"):
            lines.append(stripped)
        if len(" ".join(lines)) > 900:
            break
    return " ".join(lines)[:1200]


def build_library(manifest: list[dict[str, object]]) -> dict[str, object]:
    sources = []
    evidence = []
    requests = []
    today = date.today().isoformat()

    for idx, item in enumerate(manifest, start=1):
        source_id = f"LEG-SRC-{idx:04d}"
        evidence_id = f"LEG-EV-{idx:04d}"
        original_path = str(item["original_path"])
        archived = LIBRARY / str(item["archive_path"])
        run_id = run_for_path(original_path)
        classification = str(item["classification"])
        is_high_value = Path(original_path).name in HIGH_VALUE_FILES
        source = {
            "source_id": source_id,
            "title": title_for(Path(original_path)),
            "classification": classification,
            "geography": "UAE/GCC/global",
            "retrieval_date": today,
            "original_path": original_path,
            "archive_path": str(item["archive_path"]),
            "sha256": item["sha256"],
            "limitations": "Legacy council artifact; preserve evidence labels and verify time-sensitive third-party costs before external use.",
        }
        if run_id:
            source["legacy_run_id"] = run_id
        sources.append(source)

        if is_high_value or run_id:
            claim = extract_summary(archived)
            evidence.append(
                {
                    "evidence_id": evidence_id,
                    "request_id": None,
                    "cache_key": normalize_key(original_path),
                    "claim": claim,
                    "classification": classification,
                    "source_id": source_id,
                    "geography": "UAE/GCC/global",
                    "freshness_days": 9999 if classification != "SOURCE_BACKED_ESTIMATE" else 365,
                    "answer_source": "legacy council import",
                    "legacy_run_id": run_id,
                    "high_value": is_high_value,
                }
            )

    for idx, run in enumerate(RUNS, start=1):
        requests.append(
            {
                "request_id": f"LEG-REQ-{idx:04d}",
                "requester": "librarian",
                "question": f"What should V2 know from {run['run_id']}?",
                "normalized_question": normalize_key(run["run_id"]),
                "cache_key": normalize_key(run["run_id"]),
                "decision_affected": run["role"],
                "scope": "legacy-council-memory",
                "geography": "UAE/GCC/global",
                "freshness_days": 9999,
                "acceptable_evidence_type": "INTERNAL_PROJECT_FACT",
                "status": "ANSWERED_BY_LEGACY_IMPORT",
                "response_id": None,
                "answer_source": "legacy council import",
                "handoff": run["next"],
            }
        )

    return {
        "import_id": "legacy-council-memory-2026-06-18",
        "generated_at": today,
        "sources": sources,
        "evidence": evidence,
        "requests": requests,
        "contradictions": [],
        "rules": {
            "public_pricing_status": "not authorized",
            "latest_completed_run": "2026-06-14-pricing-and-commercial-justification-002C",
            "next_run": "Run 003 sales/proposal/discovery deliverables",
            "time_sensitive_warning": "Re-check provider/vendor prices before external publication or client commitments.",
        },
    }


def write_outputs(manifest: list[dict[str, object]], library: dict[str, object]) -> None:
    LIBRARY.mkdir(parents=True, exist_ok=True)
    for path in [IMPORT_ROOT / "MANIFEST.json", LIBRARY / "EVIDENCE_LIBRARY.json", LIBRARY / "SOURCE_LEDGER.csv", LIBRARY / "START_HERE.md"]:
        if path.exists():
            os.chmod(path, 0o700)
    (IMPORT_ROOT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
    (LIBRARY / "EVIDENCE_LIBRARY.json").write_text(json.dumps(library, indent=2, sort_keys=True), encoding="utf-8", newline="\n")

    with (LIBRARY / "SOURCE_LEDGER.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_id",
                "title",
                "classification",
                "geography",
                "retrieval_date",
                "legacy_run_id",
                "original_path",
                "archive_path",
                "sha256",
                "limitations",
            ],
        )
        writer.writeheader()
        for source in library["sources"]:
            writer.writerow({field: source.get(field, "") for field in writer.fieldnames})

    start_here = """# Codex Council V2 Legacy Memory Start Here

## Current Position

The old restaurant commercial council stopped after Run `2026-06-14-pricing-and-commercial-justification-002C`.

The next authorized continuation is Run 003: internal sales/proposal/discovery deliverables that explain the internal pricing hypotheses while preserving alternative-fit, responsibility, third-party-cost, and non-guaranteed-ROI boundaries.

## Use First

1. `codex-council-v2/library/EVIDENCE_LIBRARY.json`
2. `codex-council-v2/library/SOURCE_LEDGER.csv`
3. `codex-council-v2/library/legacy-council-import/source-archive/working/council-runs/2026-06-14-pricing-and-commercial-justification-002C/artifacts/RUN_003_SALES_DELIVERABLES_HANDOFF.md`
4. `codex-council-v2/library/legacy-council-import/source-archive/working/council-runs/2026-06-14-pricing-and-commercial-justification-002C/artifacts/PRICING_FINAL_VERDICT.md`
5. `codex-council-v2/library/legacy-council-import/source-archive/working/council-runs/2026-06-14-feature-packaging-decision-002B/artifacts/PACKAGING_FINAL_VERDICT.md`
6. `codex-council-v2/library/legacy-council-import/source-archive/working/council-runs/2026-06-14-full-restaurant-roi-research-calculator-002A-redo/artifacts/ROI_CALCULATOR_SPEC.md`

## Boundaries

- Internal prices remain hypotheses, not public price claims.
- Third-party costs must remain direct-pay or transparent pass-through.
- ROI must use owner inputs and conservative scenarios; no guaranteed ROI.
- Aggregators, POS/SaaS, WhatsApp/manual, agencies, QR/static sites, and doing nothing must remain valid alternatives when they fit better.
- Re-check vendor/provider pricing before external publication or client commitment.
"""
    (LIBRARY / "START_HERE.md").write_text(start_here, encoding="utf-8", newline="\n")


def main() -> None:
    manifest = copy_inputs()
    library = build_library(manifest)
    write_outputs(manifest, library)
    print(
        json.dumps(
            {
                "import_root": IMPORT_ROOT.as_posix(),
                "sources": len(library["sources"]),
                "evidence": len(library["evidence"]),
                "requests": len(library["requests"]),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
