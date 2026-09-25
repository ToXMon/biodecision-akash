# Runbook — Akash vLLM serve (+ Tev1 wrapper)

**Separate lease from training.** Do not use Unsloth Studio as production.

Prior notes: `personal-jev-akash-unsloth.md`, `biodecision-akash-clinical-scoring.md`.

---

## Template

- Awesome Akash vLLM: https://github.com/akash-network/awesome-akash/tree/master/vllm  
- Prefer API-only examples such as `vllm_no_ui_deployment.yml` when present.
- Qwen-sized GPU configs in the same repo as guidance for VRAM.

Copy SDL locally; never commit secrets (`sdl/README.md`).

---

## Model

| Field | Guidance |
|-------|----------|
| `MODEL` / HF id | Your fine-tuned merge **or** base + LoRA load path if template supports adapters |
| Alt | Mount `/models` from persistent storage populated at deploy |
| Thinking | Off / non-thinking path consistent with tev1 Qwen3.5 templating |

Record the exact model id and revision in a serve RUNLOG (on box or private notes — not fake numbers).

---

## Tev1 wrapper contract

Thin app (sidecar or separate small service) in front of OpenAI-compatible vLLM chat:

**Request**
```json
{
  "state": "...",
  "question": "...",
  "options": [
    {"label": "A", "key": "clear_win", "description": "..."},
    {"label": "B", "key": "mixed", "description": "..."}
  ]
}
```

**Behavior**
- Inject system prompt: select exactly one listed option; return **only** its letter.
- `temperature=0`
- `max_tokens` ≈ 8
- Parse model text → letter → map to `key`

**Response**
```json
{"label": "B", "key": "mixed", "raw": "B"}
```

Optional later: calibration-split temperature; logprobs if vLLM exposes them for ranking — not required for MVP.

---

## Harden secrets

1. API key or mTLS in front of wrapper (reject unauthenticated).
2. Reverse proxy / TLS termination as appropriate for your exposure model.
3. **No default passwords**; no Jupyter on the serve lease unless required.
4. HF token via env / sealed secret — **not** in committed SDL.
5. Private model repos: least-privilege token; rotate if lease logs leaked.
6. Network: expose only wrapper port publicly if possible; keep vLLM internal.

---

## Deploy steps

1. Confirm train export exists (HF revision or volume).
2. Fill local SDL: image tags pinned, GPU size, `MODEL`, secrets via provider mechanism.
3. Deploy; health-check OpenAI `/v1/models` or equivalent.
4. Deploy/start wrapper; hit with one synthetic Tev1 fixture (not a fake “result metric” — just parse check).
5. Point CT.gov scorer (`scripts/render_ctgov_tev1.py`) at wrapper base URL via env `TEV1_API_BASE`.

---

## Ops

- Idle train lease must already be gone.
- If thesis journal unused and GPU burns cash → destroy serve lease (Phase 4 kill criteria).
- Never log full HF tokens or patient-like free text to public ship-log.
