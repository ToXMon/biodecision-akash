# HANDOFF — BioDecision Public

For **any** agent or human on another machine. Read this first; then README + LICENCE.

**Handoff time:** 2026-09-25 ~18:46 ET (America/New_York)  
**Tree root:** `/workspace/research/biodecision-public/`  
**Prior notes (keep, cite):**  
- `/workspace/research/biodecision-akash-clinical-scoring.md`  
- `/workspace/research/personal-jev-akash-unsloth.md`

---

## Current state

| Item | Status |
|------|--------|
| Project tree + docs + stubs | **Done** (this draft) |
| `git init` / GitHub remote / push | **Not done** — user must confirm name + visibility first |
| HF dataset download / filter run | **Not done** — script stub ready |
| Akash Unsloth train lease | **Not started** |
| Smoke train / checkpoints | **None** — do not invent metrics |
| vLLM serve lease | **Not started** |
| Tev1 wrapper deployed | **Not started** |
| CT.gov ingest live | **Not started** — renderer stub only |
| Sponsor↔ticker map | **Open gap** |
| X Public posts sent | **Not done** — drafts outline only; no sends from agents unless user asks |
| Fake/invented results in tree | **Forbidden / absent** |

## Paths that matter

```
/workspace/research/biodecision-public/     # this portable tree
/workspace/research/biodecision-akash-clinical-scoring.md
/workspace/research/personal-jev-akash-unsloth.md
# On Akash Unsloth lease (when you create it):
#   /workspace/work   # persistent datasets + checkpoints
```

## What is done vs not

**Done:** documentation architecture, licence rules, experiment map, MVP flow, CT.gov Tev1 sketch, ship-log outline, Akash train/serve runbooks, filter + renderer script stubs, smoke plan outline, `.gitignore`, SDL pointers.

**Not done:** any training, any inference lease, any real NCT scores, any ticker overlay data, any git remote, any public posts.

## How to resume

1. Open `README.md` executive map + this file.
2. Re-read licence constraints in `docs/LICENCE-AND-DATA.md`.
3. If HF available: `python scripts/filter_commercial_ok.py` (may print counts; expect download cost).
4. Follow `docs/EXPERIMENT-MAP.md` Phase 0 → Phase 1; use `notebooks/01_smoke_plan.md`.
5. Train only via `runbooks/AKASH-UNSLOTH-TRAIN.md`; serve via `runbooks/AKASH-VLLM-SERVE.md` on a **separate** lease.
6. Product path: `docs/MVP-PRODUCT-FLOW.md` + `docs/CTGOV-TEV1-RENDERER.md`.
7. Before git remote: user confirms repo name + visibility; then user runs git commands in README.

## Constraints (hard)

- **Read-only draft mindset:** no unsolicited sends (X/email/chat), no pushes.
- **No fake results:** no invented loss curves, accuracy, or NCT outcomes.
- **No TrialBench commercial use** (`commercial_ok=false`, unknown licence). Same for pubmed_rct, ade_corpus, mediqa_rqe, medical_question_pairs, tev1_general mix, DDI/SciFact/SciQ (NC or unknown).
- **Never train on `benchmark`** (~46k). Calibration (~12k) = temperature fit only.
- **BioDecision does not predict stock returns.**
- Copy SDL locally; never commit secrets/passwords/HF tokens.
- Change Akash Jupyter passwords; pin Unsloth image tags; tear down train lease after export.

## Open decisions (need human)

1. GitHub **repo name** and **visibility** (private vs public).
2. Whether counsel clears any `commercial_ok=false` source (default: no).
3. Base model exact id if Unsloth naming differs from “Qwen3.5-4B”.
4. HF org/private repo for adapters vs Akash volume only.
5. Sponsor name ↔ ticker mapping strategy (manual CSV vs vendor vs fuzzy match).
6. First ticker universe for MVP (e.g. small-cap biotech watchlist size).
7. Whether `@tolu_EVM` posts go live after draft review only.
8. Budget cap (Akash GPU-hours) for smoke vs full commercial_ok SFT.

## Contact / ownership

Build-in-public target: `@tolu_EVM` — ship-log milestones only (see `docs/BUILD-IN-PUBLIC-SHIP-LOG.md`). Agents must not post unless explicitly instructed.
## Repo decision

- **Chosen name:** `biodecision-akash` (public)
- **Status:** create/push on user go (2026-09-25) — pushed to https://github.com/ToXMon/biodecision-akash (public)

