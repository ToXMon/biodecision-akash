# Runbook — Akash Unsloth train

**Train only. Tear down when done.** Production serve is a separate lease (`AKASH-VLLM-SERVE.md`).

Prior notes:
- `/workspace/research/personal-jev-akash-unsloth.md`
- `/workspace/research/biodecision-akash-clinical-scoring.md`

---

## Template & console

- Template: https://github.com/akash-network/awesome-akash/tree/master/unsloth-ai  
- Console: https://console.akash.network/new-deployment?step=edit-deployment&templateId=akash-network-awesome-akash-unsloth-ai  

Copy SDL **locally**; never commit filled secrets (`sdl/README.md`).

---

## Before create deployment

1. **Change passwords** — set strong unique `JUPYTER_PASSWORD` and `USER_PASSWORD` (defaults are unsafe).
2. **Pin image tag** — e.g. `unsloth/unsloth:2026.4.6-…-studio-…` (exact tag from awesome-akash at deploy time). Do not use floating `latest` for reproducibility.
3. **GPU** — 1× NVIDIA A100 or H100 (A100-80GB if available/needed).
4. **Persistent storage** — mount at `/workspace/work` for datasets + checkpoints.
5. **Ports** — Jupyter `:8888`, Unsloth Studio `:8000` (per template); expose only what you need; prefer SSH/tunnel patterns if template allows.
6. **Budget** — market GPU-hour bids; include image pull + train + export time; plan tear-down.

---

## Data onto the lease

1. Locally filter commercial_ok (`scripts/filter_commercial_ok.py`); smoke **20–50k** train rows first.
2. Upload JSONL (or HF download inside lease) into `/workspace/work/`:
   - `biodecision_ok_train_smoke.jsonl`
   - `biodecision_ok_dev.jsonl`
3. Confirm **no** `benchmark` split in train files; spot-check sources for TrialBench.

---

## Train steps (on lease)

1. Open Jupyter or Unsloth Studio; authenticate with **your** password.
2. QLoRA / LoRA SFT on **Qwen3.5-4B** (or closest Unsloth-supported Qwen3.5-4B id — record exact HF id in the run log).
3. Use tev1 `prompt` / `completion` columns (already chat-templated for Qwen3.5 non-thinking in config `tev1`).
4. Hyperparams: start conservative; log them; **do not invent final metrics in repo docs**.
5. Eval on commercial_ok `dev` only for early decisions.
6. Export: LoRA adapter and/or merged weights → private HF repo **or** keep under `/workspace/work/exports/`.
7. Save a short `RUNLOG.md` on the volume: date (ET), image tag, model id, row count, real train/eval numbers from logs.

---

## Tear down

1. Verify export reachable (HF revision or volume backup).
2. Close / destroy the **training** deployment — do not leave GPU idle.
3. Rotate any passwords/tokens used on that lease if they were exposed in chat logs.

---

## Env / secret warnings

| Item | Rule |
|------|------|
| Jupyter / user passwords | Change before first login; not in git |
| HF token | Env / secret store only; never commit |
| SDL with secrets | Local only; gitignored patterns in root `.gitignore` |
| Image tag | Pin; record in RUNLOG |
| `/workspace/work` | Persistent — still back up exports off-lease |

---

## Smoke checklist pointer

See `notebooks/01_smoke_plan.md`.
