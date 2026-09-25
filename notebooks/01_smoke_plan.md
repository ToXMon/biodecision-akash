# Notebook outline — smoke train checklist

Use this as a markdown checklist inside Unsloth Studio / Jupyter on the Akash train lease (`/workspace/work`). Not a fake results notebook — fill metrics only from the real run.

Prior: `runbooks/AKASH-UNSLOTH-TRAIN.md`, `docs/EXPERIMENT-MAP.md` Phase 0–1.

---

## 0. Lease hygiene

- [ ] Confirmed passwords changed (`JUPYTER_PASSWORD`, `USER_PASSWORD`)
- [ ] Image tag pinned; recorded in RUNLOG
- [ ] Persistent path writable: `/workspace/work`
- [ ] HF token available via env (not pasted into committed cells)

## 1. Data

- [ ] commercial_ok smoke JSONL present (20–50k), e.g. `/workspace/work/biodecision_ok_train_smoke.jsonl`
- [ ] commercial_ok dev JSONL present
- [ ] Spot-check: no TrialBench / blocked `source` values in smoke file
- [ ] Confirmed **benchmark** not used for training
- [ ] Record exact row counts in RUNLOG (from `wc -l` or datasets — real counts only)

## 2. Model / recipe

- [ ] Base model HF id recorded (Qwen3.5-4B or closest Unsloth-supported id)
- [ ] QLoRA/LoRA config written down (rank, alpha, targets, lr, epochs/steps, seq len, batch/grad accum)
- [ ] Using tev1 `prompt` / `completion` (non-thinking chat template)
- [ ] Eval each N steps on commercial_ok **dev** only

## 3. Train

- [ ] Smoke job launched
- [ ] Loss curve saved from actual logs (do not invent)
- [ ] Dev letter exact-match or parse-rate logged from actual eval
- [ ] No OOM / or OOM mitigated and noted

## 4. Export & tear-down

- [ ] Adapter and/or merged weights exported under `/workspace/work/exports/` and/or private HF
- [ ] Revision / path recorded
- [ ] RUNLOG.md completed with **real** numbers only
- [ ] Training deployment destroyed

## 5. Explicit non-goals for smoke

- [ ] Did **not** train on full 1.08M yet
- [ ] Did **not** use calibration for SFT
- [ ] Did **not** claim stock-picking metrics
- [ ] Did **not** paste secrets into ship-log drafts

## Suggested cell order (when you create the .ipynb)

1. Imports + env checks  
2. Load JSONL → HF `Dataset`  
3. Formatting sanity (one printed prompt/completion)  
4. Unsloth model + LoRA attach  
5. `SFTTrainer` / Unsloth train call  
6. Eval loop / sample generations at temp=0  
7. `save_pretrained` / push_to_hub  
8. RUNLOG dump  

Replace this outline with a real `.ipynb` only after cells exist and contain no secrets.
