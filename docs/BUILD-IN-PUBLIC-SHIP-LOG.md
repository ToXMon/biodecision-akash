# Build-in-public ship log (`@tolu_EVM`)

**Rules:** milestone posts only — what shipped, what was learned, what is blocked. **No hype**, no invented metrics, no “alpha guaranteed,” no TrialBench-as-commercial claims.

Agents: **do not send** posts unless the user explicitly asks. Draft here; human posts from X.

X account target: `@tolu_EVM`.

---

## Cadence outline

| When | Post type |
|------|-----------|
| After Phase 0 filter works | Licence + data hygiene milestone |
| After smoke train exports | Train path milestone (Akash Unsloth) — report only real run facts |
| After first real NCT scored | MVP scoring milestone |
| Later | Domain pack, calibration journal, honest fails |

Each post: 1–4 short paragraphs + optional link to public repo (once it exists) + one “next.”

---

## First 3 concrete milestones (ready to draft)

### Milestone 1 — Licence-safe data path
**Trigger:** `scripts/filter_commercial_ok.py` run successfully; commercial_ok counts known; blocked sources documented.

**Draft angle:**
- Building a Tev1-style biotech decision scorer on Akash.
- Using `lighteternal/biodecision-sft-v2.2` **only** via `commercial_ok`.
- TrialBench-style outcome rows stay out of commercial train (unknown licence) — will rebuild labels from public CT.gov later.
- Next: smoke QLoRA on Qwen3.5-4B (20–50k rows).

**Do not claim:** any accuracy number you have not measured.

---

### Milestone 2 — Smoke train on Akash Unsloth
**Trigger:** smoke job finished; adapter/merged exported; train lease torn down.

**Draft angle:**
- Deployed Awesome Akash Unsloth AI (A100/H100); persistent `/workspace/work`; passwords rotated; image tag pinned.
- QLoRA SFT smoke on commercial_ok tev1 prompt/completion.
- Lease destroyed after export (cost discipline).
- Next: separate vLLM lease + thin Tev1 wrapper (temp=0).

**Do not claim:** “beat BioDecision-4B” or fake loss/accuracy. Only post metrics from the actual run logs.

---

### Milestone 3 — First live NCT → Tev1 → letter
**Trigger:** one real NCT fetched, rendered, scored by your wrapper; output logged.

**Draft angle:**
- CT.gov → Tev1 renderer → vLLM wrapper returned a letter for a fixed question (endpoint / failure / AE).
- Scores = priors for a human thesis journal, not auto-trade.
- Open gap called out: sponsor name ↔ ticker map.
- Next: small company rollup + calibration journal template.

**Do not claim:** the letter is a validated probability of trial success or a trade signal.

---

## Post checklist (before Publish)

- [ ] Real milestone completed (not aspirational)
- [ ] No invented numbers
- [ ] No commercial TrialBench claim
- [ ] No “predicts stock returns” language
- [ ] Repo link only if public/remote exists and user approved visibility
- [ ] “Next” is one concrete step
