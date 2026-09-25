# CT.gov → Tev1 renderer (sketch)

**Goal:** fetch public ClinicalTrials.gov records → build Tev1 JSON (`state`, `question`, `options`) → score via wrapper → join ticker overlay.

**Stub code:** [`../scripts/render_ctgov_tev1.py`](../scripts/render_ctgov_tev1.py)  
**No fake NCT results in this repo.** Implement against live API when ready.

---

## Fetch

- API: ClinicalTrials.gov (modern API v2 preferred; confirm current base URL in implementation).
- Keys: `NCT` id and/or sponsor name query for a ticker universe.
- Fields useful for **state** text (illustrative — map to actual API paths when coding):
  - Brief / official title
  - Brief summary / detailed description (truncate thoughtfully)
  - Phase, overall status, study type
  - Primary / secondary outcome measures
  - Intervention names + arm descriptions
  - Eligibility synopsis (if used for eligibility-style questions)
  - Sponsor / collaborator names
  - Start / primary completion dates (for calendar, not for inventing outcomes)

Respect CT.gov terms; cache politely; no scraping-behind-login.

---

## Fixed question bank (MVP)

1. **Primary-endpoint outcome (most likely)**  
   Question: “Most likely primary-endpoint outcome for this protocol as written?”
2. **Dominant failure mode if it fails**  
   Question: “If this program fails, which failure mode is most plausible from the design text?”
3. **AE burden class**  
   Question: “Which adverse-event burden class best fits this intervention/population description?”

Extend later (duration band, dropout band) **only** with your own labeled domain pack — do not pull TrialBench commercially.

---

## Option schemas (example shapes — labels are design choices, not trained facts)

### Endpoint outcome
| key | label | description (short) |
|-----|-------|---------------------|
| clear_win | A | Clear primary endpoint win |
| mixed | B | Mixed / partial / secondary-only |
| fail | C | Primary endpoint fail |
| stop_ae | D | Stop / major modification for safety |
| unclear | E | Insufficient public protocol text |

### Failure mode
| key | label | description |
|-----|-------|-------------|
| efficacy | A | Efficacy shortfall |
| safety | B | Safety / AE |
| enrollment | C | Enrollment / ops |
| endpoint_choice | D | Endpoint / analysis design issue |
| external | E | Competitive / regulatory / external |

### AE class
| key | label | description |
|-----|-------|-------------|
| low | A | Relatively low expected burden class |
| moderate | B | Moderate |
| high | C | High / intensive monitoring |
| unknown | D | Cannot tell from public text |

These schemas must match what you train in the domain pack. Do not claim BioDecision already learned these exact keys from TrialBench for commercial use.

---

## Example Tev1 JSON shape (illustrative — not a real NCT score)

```json
{
  "state": "Phase 2 randomized study of [DRUG] in [POPULATION]. Primary endpoint: [ENDPOINT]. Key eligibility: [...]. Arms: [...].",
  "question": "Most likely primary-endpoint outcome for this protocol as written?",
  "options": [
    {"label": "A", "key": "clear_win", "description": "Clear primary endpoint win"},
    {"label": "B", "key": "mixed", "description": "Mixed / partial / secondary-only"},
    {"label": "C", "key": "fail", "description": "Primary endpoint fail"},
    {"label": "D", "key": "stop_ae", "description": "Stop / major modification for safety"},
    {"label": "E", "key": "unclear", "description": "Insufficient public protocol text"}
  ]
}
```

Wrapper contract: temp=0, max_tokens≈8, return `{"label":"B","key":"mixed","raw":"..."}`.

---

## Ticker overlay join keys

| Left (CT.gov) | Right (markets) | Notes |
|---------------|-----------------|-------|
| Lead sponsor name | Company legal name | Fuzzy match; subsidiaries hard |
| Collaborator names | Same | Multi-sponsor noise |
| NCT id | Internal map NCT→ticker | Best when curated |
| — | Ticker | **Map gap:** no reliable free universal sponsor↔ticker map in this tree |

**Open work:** maintain a curated CSV `sponsor_name,ticker,exchange,notes` for the MVP universe; document misses rather than inventing links.

---

## Pipeline steps (implementation order)

1. `fetch_nct(nct_id) -> dict`
2. `fields_to_state(record) -> str`
3. `render_questions(state) -> list[Tev1Request]`
4. `score_via_wrapper(req) -> Tev1Response` (HTTP to serve lease)
5. `join_ticker(sponsor) -> Optional[str]`
6. `rollup_company(scores) -> CompanyCard`

See stub signatures in `scripts/render_ctgov_tev1.py`.
