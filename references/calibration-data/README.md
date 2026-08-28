# Calibration Data — Empirical Reference Levels

This directory stores **empirical reference levels** for the `paper-rubric-review` skill. Each level contains the score distribution of papers that hit a specific external milestone (e.g., accepted to a journal volume).

## What this is NOT

- ❌ NOT a Yau / NeurIPS / CCF tier prediction
- ❌ NOT a calibration of "what score gets accepted at venue X"
- ❌ NOT a percentile against any real submission pool
- ❌ NOT a guarantee that scoring in the band means acceptance

## What this IS

- ✅ An empirical distribution of LLM self-scores for **n observed papers** that share a specific external milestone
- ✅ A reference distribution so a newly-scored paper can be compared against "where accepted papers in this reference set fell"
- ✅ A starting point for building a more reliable baseline as more papers are added

## Honest framing rules (must be followed when using)

1. **Always use observation language**, not threshold language:
   - ✅ "Your paper's total of 62 falls within the observed range of n=12 accepted papers in YSA Vol.10"
   - ❌ "Your paper got a YSA Vol.10 accept score"
2. **Always disclose the noise floor** (±8 points per skill documentation)
3. **Always disclose selection criteria** (e.g., "all 12 STEM papers in volume" — never "top STEM papers")
4. **Always include the disclaimer** in any output that uses this data

## Files

| File | Purpose |
|---|---|
| `levels.json` | Registry of all available levels. Read by the skill to list options. |
| `ysa10-stem.json` | YSA Vol.10 (April 2026) STEM papers, n=12, full per-dim and macro stats. |
| `ysa10-stem_summary.csv` | Same as above in CSV format for easy viewing in Excel. |
| `ysa10-stem_papers.csv` | Per-paper scores (12 rows × 18 columns). |
| `README.md` | This file. |

## How to use (programmatic)

```bash
# Compare a scored paper against the YSA-10 STEM level
python3 scripts/compare-calibration.py --level ysa10-stem --scores "75,65,50,55,60,80,45,30,70,70" --macros "63.3,57.5,70"

# Or from a JSON output of paper-rubric-review
python3 scripts/compare-calibration.py --level ysa10-stem --from-json path/to/paper_review.json
```

The output is a markdown table with per-dimension and macro percentile ranks, plus an honest interpretation.

## How to add a new level

1. **Score n≥5 papers** that share a specific external milestone using `paper-rubric-review`. Document the protocol version.
2. **Compute per-dimension statistics** (min, Q1, median, mean, Q3, max, std) for all 10 dims + 3 macros + total.
3. **Save as JSON** following the schema in `ysa10-stem.json`. Use a clear, dated filename.
4. **Add an entry to `levels.json`** with: level_id, level_name (EN), level_name_zh, n_papers, milestone_type, summary, added_on, added_by_session.
5. **Document provenance**: scoring protocol version, who scored, when, noise estimate, selection criteria.

**Recommended minimum n:**
- n≥5 for any usable IQR
- n≥10 for stable medians
- n≥20 for cross-year stability
- n<5 → do not include (insufficient for a usable band)

## Current levels

| Level ID | n | Median Total | IQR | Source |
|---|---:|---:|---|---|
| `ysa10-stem` | 12 | 65.5 | [59.0, 70.3] | YSA Yuanpei Young Scholars Journal Vol.10 (April 2026), STEM papers, scored 2026-08-27 |

## What "YSA-10 STEM level" means in plain language

It means: "The empirical distribution of LLM self-scores for the 12 STEM-track papers that were accepted to YSA Journal Vol.10." It does NOT mean:
- "Papers scoring ≥ 60 in this level will be accepted to YSA Vol.11" (unproven)
- "The 65.5 median is the YSA accept threshold" (no — the actual committee uses a different rubric)
- "This is calibrated against winners" (no — it's calibrated against observed accepted papers only)

If you submit a paper to YSA Vol.11 and your rubric-review total is 65.5, the comparison tells you "this is consistent with the empirical middle of Vol.10 STEM acceptances" — that's all it can honestly say.
