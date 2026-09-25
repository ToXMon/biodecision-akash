# BioDecision Public — clinical-trial scoring for investment thesis

**Status:** read-only draft tree. **Do not `git init`, create a GitHub remote, or push** until you confirm repo name + visibility (see below).

**Prior research (cite, do not discard):**
- `/workspace/research/biodecision-akash-clinical-scoring.md` (2026-09-25 ET)
- `/workspace/research/personal-jev-akash-unsloth.md` (2026-09-23 ET)

---

## One-page executive map

### What
A portable project to fine-tune a Tev1-style biomedical decision model (Qwen3.5-4B + QLoRA on Akash Unsloth) on **commercial_ok** rows from [`lighteternal/biodecision-sft-v2.2`](https://huggingface.co/datasets/lighteternal/biodecision-sft-v2.2) (~1.1M Tev1 decisions: state + question + lettered options → one letter), then serve via a **separate** Akash vLLM lease + thin Tev1 wrapper, and score public ClinicalTrials.gov programs for an **investment-thesis journal** (priors/flags, not auto-trade).

### Why
BioDecision gives strong biomedical decision SFT. Closest built-in trial outcome signals (TrialBench: approval, failure reason, AE, duration, dropout, mortality) are **`commercial_ok=false`** (unknown licence). For any money-making scorer you must (1) filter `commercial_ok`, (2) rebuild outcome labels from public CT.gov + press/SEC, (3) never treat this as stock-return prediction.

### Honest limits
| Want | Reality |
|------|---------|
| Phase 1/2/3 “likelihood” from design | Rebuild with your labels; TrialBench blocked commercially |
| Protocol / eligibility / evidence direction | commercial_ok sources (TREC-CT, NLI4CT, evidence_inference, MCQs) help |
| Stock returns | **Out of scope** — separate market labels + model |
| Auto-trade | **Not this product** — human thesis journal only |
| Fake metrics / invented smoke results | **Forbidden** in this repo |

### 10-step execution checklist
1. Confirm GitHub **repo name** + **visibility** (private recommended until licence review); then `git init` / remote / push yourself — **not done here**.
2. Read [`docs/LICENCE-AND-DATA.md`](docs/LICENCE-AND-DATA.md); run [`scripts/filter_commercial_ok.py`](scripts/filter_commercial_ok.py) when HF is available; never use TrialBench commercially; never train on `benchmark`.
3. Smoke-filter: export 20–50k commercial_ok train + commercial_ok dev JSONL.
4. Deploy **Awesome Akash Unsloth AI** (A100/H100); change Jupyter passwords; pin image tag; use `/workspace/work` persistent — see [`runbooks/AKASH-UNSLOTH-TRAIN.md`](runbooks/AKASH-UNSLOTH-TRAIN.md).
5. QLoRA SFT on Qwen3.5-4B using tev1 `prompt`/`completion`; smoke 20–50k first; export adapter/merged; **tear down train lease**.
6. Deploy **separate** Awesome Akash **vLLM** lease; point at your model; harden secrets — [`runbooks/AKASH-VLLM-SERVE.md`](runbooks/AKASH-VLLM-SERVE.md).
7. Thin Tev1 wrapper: `{state, question, options}` → temp=0, max_tokens≈8 → `{label, key, raw}`.
8. CT.gov ingest → Tev1 render → score → sponsor↔ticker overlay (map gap is open) — [`docs/CTGOV-TEV1-RENDERER.md`](docs/CTGOV-TEV1-RENDERER.md), [`scripts/render_ctgov_tev1.py`](scripts/render_ctgov_tev1.py).
9. Human thesis journal: scores as priors/flags; calibrate vs later readouts — Phase 4 in [`docs/EXPERIMENT-MAP.md`](docs/EXPERIMENT-MAP.md).
10. Build-in-public for `@tolu_EVM`: ship-log milestones only — [`docs/BUILD-IN-PUBLIC-SHIP-LOG.md`](docs/BUILD-IN-PUBLIC-SHIP-LOG.md).

---

## Deep docs

| Doc | Purpose |
|-----|---------|
| [HANDOFF.md](HANDOFF.md) | Resume state for any agent/human |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Components + Mermaid |
| [docs/LICENCE-AND-DATA.md](docs/LICENCE-AND-DATA.md) | commercial_ok rules + source table |
| [docs/EXPERIMENT-MAP.md](docs/EXPERIMENT-MAP.md) | Phases 0–4, success/kill criteria |
| [docs/MVP-PRODUCT-FLOW.md](docs/MVP-PRODUCT-FLOW.md) | Investment thesis tool flow |
| [docs/CTGOV-TEV1-RENDERER.md](docs/CTGOV-TEV1-RENDERER.md) | NCT → Tev1 sketch |
| [docs/BUILD-IN-PUBLIC-SHIP-LOG.md](docs/BUILD-IN-PUBLIC-SHIP-LOG.md) | X Public milestone drafts |
| [runbooks/AKASH-UNSLOTH-TRAIN.md](runbooks/AKASH-UNSLOTH-TRAIN.md) | Train lease |
| [runbooks/AKASH-VLLM-SERVE.md](runbooks/AKASH-VLLM-SERVE.md) | Serve lease |
| [sdl/README.md](sdl/README.md) | Awesome-akash template pointers |
| [notebooks/01_smoke_plan.md](notebooks/01_smoke_plan.md) | Smoke train checklist |

## Dataset facts (verified)

- HF: `lighteternal/biodecision-sft-v2.2`
- Config `tev1`: prompt/completion chat-templated for Qwen3.5 non-thinking
- Splits: train ~1.08M, dev ~12k, calibration ~12k (**temp fit only**), benchmark ~46k (**NEVER train**)
- `commercial_ok` filter required for commercial use

## Suggested next git commands (YOU run these — after confirmation)

```bash
# ONLY after you confirm: repo name, visibility (private/public), and that secrets stay out of tree
cd /workspace/research/biodecision-public
git init
git add .
git status   # review: no .env, no HF tokens, no checkpoints
git commit -m "Initial BioDecision public draft tree (no train results)"
# Create empty repo on GitHub with YOUR chosen name/visibility, then:
# git remote add origin git@github.com:<YOU>/<REPO>.git
# git branch -M main
# git push -u origin main
```

**Confirm before any remote:**
1. Exact GitHub repo name
2. Visibility (private recommended until counsel/licence review)
3. That this tree contains no secrets, checkpoints, or invented metrics

**Explicit: this agent did not create or push a GitHub repo.**

## Constraints

- Read-only draft for handoff; no sends (email/X/chat) from this tree
- No fake training results or invented metrics
- No commercial use of TrialBench / other `commercial_ok=false` sources
- Never train on `benchmark`
