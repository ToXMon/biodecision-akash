#!/usr/bin/env python3
"""Filter lighteternal/biodecision-sft-v2.2 (tev1) to commercial_ok rows.

Documents the load_dataset + filter pattern. Runs when `datasets` + network
are available; otherwise prints instructions and exits non-zero.

Rules:
  - Keep commercial_ok is True only for commercial products.
  - Never write the benchmark split into train exports.
  - calibration is for temperature fitting only (optional separate export).
  - Do not invent counts if the dataset is not actually loaded.

Usage:
  python scripts/filter_commercial_ok.py
  python scripts/filter_commercial_ok.py --smoke-n 30000 --out-dir ./data
  python scripts/filter_commercial_ok.py --dry-run-docs-only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

DATASET_ID = "lighteternal/biodecision-sft-v2.2"
CONFIG = "tev1"

# Documented blocked families (commercial). Re-check HF card before ship.
BLOCKED_SOURCES_DOC = frozenset(
    {
        "trial_approval",
        "failure_reason",
        "adverse_event",
        "duration",
        "dropout",
        "mortality",
        "pubmed_rct",
        "ade_corpus",
        "mediqa_rqe",
        "medical_question_pairs",
        "tev1_general",
        # DDI / SciFact / SciQ — NC or unknown; names may vary in `source` field
        "ddi",
        "scifact",
        "sciq",
    }
)


def _is_commercial_ok(row: dict) -> bool:
    v = row.get("commercial_ok")
    return v is True or v == True  # noqa: E712 — HF may use bool or weird types


def print_licence_banner() -> None:
    print("=" * 72)
    print("BioDecision commercial_ok filter")
    print(f"  dataset={DATASET_ID!r} config={CONFIG!r}")
    print("  NEVER train on split=benchmark")
    print("  calibration = temperature fit only")
    print("  TrialBench + listed sources = commercial_ok=false (blocked)")
    print("=" * 72)


def dry_run_docs_only() -> int:
    print_licence_banner()
    print("\n[dry-run] Code path when HF is available:\n")
    print(
        f'''
from datasets import load_dataset

ds = load_dataset("{DATASET_ID}", "{CONFIG}")
train_ok = ds["train"].filter(lambda r: r["commercial_ok"] is True)
dev_ok = ds["dev"].filter(lambda r: r["commercial_ok"] is True)
# optional: train_ok.select(range(smoke_n)).to_json("...jsonl")
'''.strip()
    )
    print("\nDocumented blocked source name fragments:", sorted(BLOCKED_SOURCES_DOC))
    return 0


def run_filter(out_dir: Path, smoke_n: int | None, export_calibration: bool) -> int:
    print_licence_banner()
    try:
        from datasets import load_dataset
    except ImportError:
        print(
            "ERROR: `datasets` not installed. pip install datasets  "
            "or re-run with --dry-run-docs-only",
            file=sys.stderr,
        )
        return 1

    print(f"Loading {DATASET_ID} ({CONFIG}) — may download; be patient…")
    try:
        ds = load_dataset(DATASET_ID, CONFIG)
    except Exception as e:  # noqa: BLE001 — surface HF/network errors clearly
        print(f"ERROR: load_dataset failed: {e}", file=sys.stderr)
        print("Hint: check network, HF access, and dataset card config name.", file=sys.stderr)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)

    def filter_ok(split_name: str):
        if split_name not in ds:
            print(f"WARN: split {split_name!r} missing; skip")
            return None
        split = ds[split_name]
        n_all = len(split)
        ok = split.filter(_is_commercial_ok)
        n_ok = len(ok)
        print(f"  split={split_name:12} all={n_all:,}  commercial_ok={n_ok:,}")
        return ok

    # Explicitly do not filter benchmark into train artifacts
    print("Splits present:", list(ds.keys()))
    if "benchmark" in ds:
        print(
            f"  split=benchmark   all={len(ds['benchmark']):,}  "
            "(HOLD OUT — will not export as train)"
        )

    train_ok = filter_ok("train")
    dev_ok = filter_ok("dev")

    if train_ok is None:
        print("ERROR: no train split", file=sys.stderr)
        return 1

    # Spot-check: among commercial_ok, count rows whose source looks blocked
    # (should be ~0 if card labels are consistent)
    src_field = "source"
    if src_field in train_ok.column_names:
        def looks_blocked(r: dict) -> bool:
            s = (r.get(src_field) or "").lower()
            return any(b in s for b in BLOCKED_SOURCES_DOC)

        blocked_in_ok = train_ok.filter(looks_blocked)
        print(
            f"  spot-check: commercial_ok rows matching blocked name fragments: "
            f"{len(blocked_in_ok):,} (expect 0; investigate if >0)"
        )

    export = train_ok
    if smoke_n is not None:
        smoke_n = min(smoke_n, len(train_ok))
        export = train_ok.select(range(smoke_n))
        print(f"  smoke export n={smoke_n:,}")

    train_path = out_dir / (
        "biodecision_ok_train_smoke.jsonl"
        if smoke_n is not None
        else "biodecision_ok_train.jsonl"
    )
    print(f"Writing {train_path} …")
    export.to_json(str(train_path))

    if dev_ok is not None:
        dev_path = out_dir / "biodecision_ok_dev.jsonl"
        print(f"Writing {dev_path} …")
        dev_ok.to_json(str(dev_path))

    if export_calibration and "calibration" in ds:
        cal = ds["calibration"]  # full split; consumer must not SFT on this
        cal_path = out_dir / "biodecision_calibration_TEMP_FIT_ONLY.jsonl"
        print(f"Writing {cal_path} (TEMP FIT ONLY — not for SFT) …")
        cal.to_json(str(cal_path))

    print("Done. Do not train on benchmark. Do not commercial-use TrialBench.")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--dry-run-docs-only",
        action="store_true",
        help="Print filter pattern without downloading",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        default=Path("./data"),
        help="Directory for JSONL exports",
    )
    p.add_argument(
        "--smoke-n",
        type=int,
        default=None,
        help="If set, export only first N commercial_ok train rows (e.g. 30000)",
    )
    p.add_argument(
        "--export-calibration",
        action="store_true",
        help="Also export calibration split (temp fit only; not SFT)",
    )
    args = p.parse_args(argv)

    if args.dry_run_docs_only:
        return dry_run_docs_only()
    return run_filter(args.out_dir, args.smoke_n, args.export_calibration)


if __name__ == "__main__":
    raise SystemExit(main())
