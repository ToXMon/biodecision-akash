# Experiment map (phased)

No invented metrics. Record real outcomes only when a phase actually runs. Kill criteria stop spend early.

Prior notes: `biodecision-akash-clinical-scoring.md`, `personal-jev-akash-unsloth.md`.

---

## Phase 0 — Licence + smoke data prep

**Goal:** prove filter works; export small commercial_ok JSONL; confirm no blocked sources in train mix.

**Actions:**
- Read `docs/LICENCE-AND-DATA.md`
- Run `scripts/filter_commercial_ok.py` (when HF available)
- Export 20–50k commercial_ok train + commercial_ok dev
- Spot-check `source` column for TrialBench / blocked names

**Success:**
- Filter runs without error; counts printed
- Spot-check finds zero TrialBench in commercial_ok export
- `benchmark` not in train files

**Kill:**
- Cannot determine `commercial_ok` field — stop until card/schema clarified
- Counsel forbids commercial_ok subset you planned to use

---

## Phase 1 — commercial_ok SFT (smoke → optional scale)

**Goal:** QLoRA on Qwen3.5-4B via Akash Unsloth; smoke 20–50k first; then optional larger commercial_ok mix.

**Actions:**
- Follow `runbooks/AKASH-UNSLOTH-TRAIN.md`
- Change passwords; pin image tag; use `/workspace/work`
- Train tev1 prompt/completion; eval on commercial_ok dev
- Export adapter/merged; **tear down train lease**

**Success:**
- Smoke job completes; checkpoint exported to HF or volume
- Dev letter-accuracy (or exact-match) logged honestly from the run — no invented numbers in docs
- Train lease destroyed after export

**Kill:**
- GPU lease unstable / cost exceeds budget before smoke finishes
- Unsloth cannot load chosen Qwen3.5-4B variant — switch only after documenting the id, do not fake results
- Any blocked source found in train mix after the fact — discard checkpoint; refilter

---

## Phase 2 — Domain pack (historical outcomes)

**Goal:** add 500–5k self-labeled Tev1 rows from past public trials (CT.gov + press/SEC) with ordered outcome options.

**Actions:**
- Build labels offline (win / mixed / fail / AE-stop, etc.)
- Mix small % into commercial_ok SFT (or continued SFT)
- Keep licence audit trail for every row

**Success:**
- Domain pack schema matches Tev1; labels documented
- Continued SFT or mix train completes; qualitative review of held-out historical cases

**Kill:**
- Cannot get reliable historical labels for target universe
- Domain pack contaminates with non-public / restricted text

---

## Phase 3 — CT.gov scoring MVP

**Goal:** ingest open Phase 1/2/3 records → render Tev1 → score via wrapper → company rollup + ticker overlay attempt.

**Actions:**
- Implement/extend `scripts/render_ctgov_tev1.py`
- Fixed question bank (endpoint outcome / failure mode / AE class)
- Serve path: `runbooks/AKASH-VLLM-SERVE.md` + wrapper
- Join sponsor ↔ ticker (map gap is open — see open decisions)

**Success:**
- End-to-end: ≥1 real NCT scored with real model output (logged, not invented)
- Rollup view for ≥1 sponsor/company
- Explicit note where ticker map fails

**Kill:**
- CT.gov API access or schema change blocks ingest with no fallback
- Wrapper cannot reliably parse letter at temp=0 after prompt fixes
- Ticker map gap blocks the only intended user value **and** no manual map is acceptable — document and pause product, keep model research

---

## Phase 4 — Calibration journal

**Goal:** human thesis journal; scores as priors/flags; track vs later readouts; optional temp fit on `calibration` split (not SFT).

**Actions:**
- Log prediction date, NCT, question, letter, rationale (human)
- After readout: grade; update calibration notes
- Optional: fit temperature on calibration split only

**Success:**
- Journal has dated entries and at least a few closed-loop grades over time
- No auto-trade hooks

**Kill:**
- Journal unused for N weeks while serving costs burn — tear down serve lease
- Stakeholders demand auto-trade — refuse; product scope is thesis tool only

---

## Cross-phase rules

- Never train on `benchmark`
- Never commercial-use TrialBench / commercial_ok=false without counsel
- Never publish fake smoke metrics in README or ship-log
- Tear down idle train GPUs
