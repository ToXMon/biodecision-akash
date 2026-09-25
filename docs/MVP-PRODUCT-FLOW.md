# MVP product flow — investment thesis tool

**Product identity:** clinical-program scoring priors for a human biotech thesis journal.  
**Not:** stock-return prediction, auto-trade, or “this ticker wins Phase 3” oracle.

BioDecision SFT teaches lettered biomedical decisions. Investment value comes from (1) commercial_ok general biomedical skill, (2) your domain pack of historical outcomes, (3) CT.gov → Tev1 → score → company rollup, (4) human judgment.

---

## Flow

```
Ticker / sponsor watchlist
        │
        ▼
ClinicalTrials.gov API (by sponsor or NCT list)
        │
        ▼
Normalize: phase, status, synopsis, endpoints, arms, AE text if public
        │
        ▼
Tev1 renderer (fixed question bank + option schemas)
        │
        ▼
Tev1 wrapper → vLLM (temp=0, max_tokens≈8) → {label, key, raw}
        │
        ▼
Per-NCT score card (multiple questions)
        │
        ▼
Company rollup: pipeline heatmap + upcoming readout calendar
        │
        ▼
Human thesis journal: priors / flags / disagreement notes
        │
        ▼
Later: grade vs actual readout (calibration) — Phase 4
```

---

## How to use scores (allowed)

- **Prior:** “Model leans B (mixed) on primary endpoint given protocol text.”
- **Flag:** “AE-burden class high vs peers in same phase — review SOF before sizing.”
- **Disagreement:** “Model says clear win; sell-side says fail — dig into endpoint choice.”
- **Calendar:** surface NCT readout windows for journal follow-up.

## How not to use scores (forbidden product claims)

- Auto-entry/exit signals
- “Predicted return” or Sharpe from BioDecision alone
- Commercial TrialBench-style approval odds without your own labels + licence clearance
- Presenting smoke/dev letter-match as validated alpha

---

## Data layers

| Layer | Source | Commercial? |
|-------|--------|-------------|
| Base SFT | biodecision commercial_ok | Yes if filtered |
| Domain pack | Your CT.gov+press/SEC labels | Yes if you own/clear text |
| Live score input | CT.gov public API fields | Public data; respect ToS |
| TrialBench in HF set | Do not use commercially | No |

---

## Minimal UI / API surface (MVP)

1. `POST /v1/decide` — Tev1 body in, letter out (wrapper).
2. `POST /v1/score_nct` — NCT id → rendered questions → batch decide → score card.
3. `GET /v1/company/{sponsor_or_ticker}` — rollup of active NCTs (ticker join may be stubbed).
4. Local markdown/CSV **thesis journal** (gitignored if personal) — not auto-trade.

---

## Honest “phase likelihood” table

| User ask | Honest mechanism |
|----------|------------------|
| Success odds from design | Rebuild labels; TrialBench blocked commercially |
| Protocol / eligibility quality | TREC-CT / NLI4CT-style commercial_ok tasks |
| Evidence direction from text | evidence_inference / PubMedQA-style (check commercial_ok) |
| Stock return | Out of scope |

See also: `ARCHITECTURE.md`, `docs/CTGOV-TEV1-RENDERER.md`, `docs/EXPERIMENT-MAP.md`.
