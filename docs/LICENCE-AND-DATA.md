# Licence and data rules

Dataset: [`lighteternal/biodecision-sft-v2.2`](https://huggingface.co/datasets/lighteternal/biodecision-sft-v2.2)  
Config: `tev1` (prompt/completion chat-templated for Qwen3.5 non-thinking)  
Scale: ~1.1M Tev1-format biomedical decisions (state + question + lettered options → one letter)

**Rule:** for any commercial product, filter `commercial_ok == True` before train or serve. Treat `commercial_ok == False` as research-only unless counsel clears it.

---

## Splits (do not violate)

| Split | Approx size | Allowed use |
|-------|-------------|-------------|
| train | ~1.08M | Train **after** commercial_ok filter |
| dev | ~12k | Eval / early stopping (prefer commercial_ok subset) |
| calibration | ~12k | **Temperature fit only** — not SFT |
| benchmark | ~46k | **NEVER train** — holdout eval only |

---

## commercial_ok = false (blocked for commercial use)

| Source / family | Reason (per dataset card / prior note) |
|-----------------|----------------------------------------|
| TrialBench: `trial_approval`, `failure_reason`, `adverse_event`, `duration`, `dropout`, `mortality` | unknown licence |
| `pubmed_rct` | commercial_ok=false |
| `ade_corpus` | commercial_ok=false |
| `mediqa_rqe` | commercial_ok=false |
| `medical_question_pairs` | commercial_ok=false |
| `tev1_general` mix | commercial_ok=false |
| DDI / SciFact / SciQ | NC or unknown |

**Implication:** closest “trial outcome from design” signals in the card are TrialBench — **licence-blocked commercially**. Rebuild outcome labels from public ClinicalTrials.gov + press/SEC for investment thesis.

---

## commercial_ok = true (examples — verify on card before ship)

| Source | Licence note (examples) |
|--------|-------------------------|
| `trec_ct` | CC BY-SA |
| `evidence_inference` | MIT |
| `nli4ct` | CC BY-SA |
| `medmcqa` | Apache-2.0 |
| many MIT MCQs | MIT |
| `drug_reviews` | CC BY |

Always re-check the live Hugging Face dataset card; this table is a summary from verified research notes, not a legal opinion.

---

## How to filter in code

```python
from datasets import load_dataset

ds = load_dataset("lighteternal/biodecision-sft-v2.2", "tev1")

train_ok = ds["train"].filter(lambda r: r["commercial_ok"] is True)
dev_ok = ds["dev"].filter(lambda r: r["commercial_ok"] is True)

# Optional focus on trial-ish commercial sources:
TRIALISH = {"trec_ct", "evidence_inference", "nli4ct"}  # extend after card review
train_focus = train_ok.filter(lambda r: r.get("source") in TRIALISH)

# NEVER:
# ds["benchmark"] for training
# TrialBench sources for commercial products
# calibration for SFT (temp fit only)
```

Working stub: [`../scripts/filter_commercial_ok.py`](../scripts/filter_commercial_ok.py).

---

## What this dataset is not

- Not a stock-return label set
- Not a licence-cleared TrialBench replacement
- Not permission to invent metrics or publish fake smoke numbers

---

## Citations

- HF dataset card: https://huggingface.co/datasets/lighteternal/biodecision-sft-v2.2  
- Prior note: `/workspace/research/biodecision-akash-clinical-scoring.md`
