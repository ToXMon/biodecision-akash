#!/usr/bin/env python3
"""CT.gov → Tev1 renderer stub.

Fetches are TODO. No fake NCT results. See docs/CTGOV-TEV1-RENDERER.md.

Example Tev1 shape (illustrative fixture only — not a model score):

{
  "state": "Phase 2 randomized study of [DRUG] in [POPULATION]. Primary endpoint: ...",
  "question": "Most likely primary-endpoint outcome for this protocol as written?",
  "options": [
    {"label": "A", "key": "clear_win", "description": "Clear primary endpoint win"},
    {"label": "B", "key": "mixed", "description": "Mixed / partial / secondary-only"},
    {"label": "C", "key": "fail", "description": "Primary endpoint fail"},
    {"label": "D", "key": "stop_ae", "description": "Stop / major modification for safety"},
    {"label": "E", "key": "unclear", "description": "Insufficient public protocol text"}
  ]
}
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Option schemas (design choices — must match domain-pack labels when you train)
# ---------------------------------------------------------------------------

ENDPOINT_OUTCOME_OPTIONS = [
    {"label": "A", "key": "clear_win", "description": "Clear primary endpoint win"},
    {"label": "B", "key": "mixed", "description": "Mixed / partial / secondary-only"},
    {"label": "C", "key": "fail", "description": "Primary endpoint fail"},
    {"label": "D", "key": "stop_ae", "description": "Stop / major modification for safety"},
    {"label": "E", "key": "unclear", "description": "Insufficient public protocol text"},
]

FAILURE_MODE_OPTIONS = [
    {"label": "A", "key": "efficacy", "description": "Efficacy shortfall"},
    {"label": "B", "key": "safety", "description": "Safety / AE"},
    {"label": "C", "key": "enrollment", "description": "Enrollment / ops"},
    {"label": "D", "key": "endpoint_choice", "description": "Endpoint / analysis design issue"},
    {"label": "E", "key": "external", "description": "Competitive / regulatory / external"},
]

AE_CLASS_OPTIONS = [
    {"label": "A", "key": "low", "description": "Relatively low expected burden class"},
    {"label": "B", "key": "moderate", "description": "Moderate"},
    {"label": "C", "key": "high", "description": "High / intensive monitoring"},
    {"label": "D", "key": "unknown", "description": "Cannot tell from public text"},
]


@dataclass
class Tev1Request:
    state: str
    question: str
    options: list[dict[str, str]]


@dataclass
class Tev1Response:
    label: str
    key: str
    raw: str


def fetch_nct(nct_id: str) -> dict[str, Any]:
    """Fetch one study from ClinicalTrials.gov API v2.

    TODO:
      - Confirm current API base URL and path (e.g. studies?filter.ids=NCT...)
      - requests/httpx GET with polite User-Agent and retry/backoff
      - Return raw JSON dict for the study
      - Do NOT fabricate NCT payloads for demos committed as "results"
    """
    raise NotImplementedError(
        f"fetch_nct({nct_id!r}): implement against live CT.gov API — "
        "no fake NCT bodies in this stub"
    )


def fetch_by_sponsor(sponsor_query: str, page_size: int = 20) -> list[dict[str, Any]]:
    """Search studies by sponsor name.

    TODO: map sponsor_query to CT.gov filter; paginate; return list of study dicts.
    """
    raise NotImplementedError(
        f"fetch_by_sponsor({sponsor_query!r}): not implemented (page_size={page_size})"
    )


def fields_to_state(record: dict[str, Any], max_chars: int = 6000) -> str:
    """Normalize CT.gov fields into a Tev1 `state` string.

    TODO: pull title, summary, phase, status, outcomes, arms, interventions,
    eligibility synopsis; truncate to max_chars; strip boilerplate.
    """
    # Placeholder structure only — callers must pass a real record from fetch_*.
    _ = record, max_chars
    raise NotImplementedError("fields_to_state: map API fields → state text")


def render_endpoint_outcome(state: str) -> Tev1Request:
    return Tev1Request(
        state=state,
        question="Most likely primary-endpoint outcome for this protocol as written?",
        options=list(ENDPOINT_OUTCOME_OPTIONS),
    )


def render_failure_mode(state: str) -> Tev1Request:
    return Tev1Request(
        state=state,
        question="If this program fails, which failure mode is most plausible from the design text?",
        options=list(FAILURE_MODE_OPTIONS),
    )


def render_ae_class(state: str) -> Tev1Request:
    return Tev1Request(
        state=state,
        question="Which adverse-event burden class best fits this intervention/population description?",
        options=list(AE_CLASS_OPTIONS),
    )


def render_question_bank(state: str) -> list[Tev1Request]:
    """Fixed MVP question bank."""
    return [
        render_endpoint_outcome(state),
        render_failure_mode(state),
        render_ae_class(state),
    ]


def score_via_wrapper(
    req: Tev1Request,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Tev1Response:
    """POST Tev1Request to the thin wrapper (temp=0, max_tokens≈8).

    TODO:
      - POST {api_base}/v1/decide with JSON body asdict(req)
      - Headers: Authorization if api_key
      - Parse {"label","key","raw"}
      - Env defaults: TEV1_API_BASE, TEV1_API_KEY
    """
    api_base = api_base or os.environ.get("TEV1_API_BASE")
    api_key = api_key or os.environ.get("TEV1_API_KEY")
    _ = req, api_base, api_key
    raise NotImplementedError(
        "score_via_wrapper: wire to Akash vLLM Tev1 wrapper when serve lease exists"
    )


def join_ticker(
    sponsor_name: str,
    map_path: Optional[str] = None,
) -> Optional[str]:
    """Join sponsor name → ticker.

    TODO: load curated CSV (sponsor_name,ticker,...); exact then fuzzy match.
    GAP: no universal free map in-repo — return None and log miss rather than invent.
    """
    _ = sponsor_name, map_path
    # Honest stub: always unknown until a curated map exists
    return None


def rollup_company(nct_scores: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate per-NCT score cards into a company-level card.

    TODO: heatmap by phase/question; readout calendar fields; list ticker if joined.
    """
    return {
        "n_programs": len(nct_scores),
        "programs": nct_scores,
        "notes": "rollup stub — no invented risk scores",
    }


def example_tev1_fixture() -> dict[str, Any]:
    """Illustrative JSON only — not tied to a real NCT or model output."""
    req = render_endpoint_outcome(
        "Phase 2 randomized study of [DRUG] in [POPULATION]. "
        "Primary endpoint: [ENDPOINT]. Key eligibility: [...]. Arms: [...]."
    )
    return asdict(req)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--print-fixture",
        action="store_true",
        help="Print example Tev1 JSON shape (not a real NCT)",
    )
    p.add_argument(
        "--nct",
        type=str,
        default=None,
        help="NCT id to fetch+render (will fail until fetch_nct implemented)",
    )
    args = p.parse_args(argv)

    if args.print_fixture:
        print(json.dumps(example_tev1_fixture(), indent=2))
        return 0

    if args.nct:
        try:
            record = fetch_nct(args.nct)
            state = fields_to_state(record)
            for req in render_question_bank(state):
                print(json.dumps(asdict(req), indent=2))
        except NotImplementedError as e:
            print(f"TODO: {e}", file=sys.stderr)
            return 2
        return 0

    p.print_help()
    print(
        "\nStub ready. Try: python scripts/render_ctgov_tev1.py --print-fixture",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
