# Empirical Reference Comparison

**Reference level:** YSA 元培青年学者期刊 第 10 期 (2026 年 4 月) — STEM 方向
**Reference (EN):** YSA Yuanpei Young Scholars Journal Vol.10 (April 2026) — STEM papers
**Source:** https://www.yuanpeiyoungscholars.com/pdf/Young_Scholars_Academic_Journal_10th
**n_papers in level:** 12
**Noise floor:** ±8 points per paper from prompt sensitivity (per skill's documented noise estimate)

---

## Per-dimension comparison

| # | Dim | You | Min | Q1 | Median | Q3 | Max | Percentile |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 选题创新性 | 80.0 | 60 | 62.8 | 65.0 | 72.0 | 78 | 100.0 |
| 2 | 方法原创性 | 75.0 | 50 | 51.2 | 55.0 | 67.2 | 70 | 100.0 |
| 3 | 方法严谨性 | 72.0 | 55 | 62.8 | 67.5 | 78.0 | 80 | 66.7 |
| 4 | 实验验证 | 85.0 | 40 | 46.2 | 55.0 | 71.0 | 82 | 100.0 |
| 5 | 写作规范性 | 60.0 | 55 | 64.0 | 72.0 | 77.2 | 80 | 12.5 |
| 6 | 结构与逻辑 | 90.0 | 68 | 72.0 | 80.0 | 81.5 | 82 | 100.0 |
| 7 | 文献覆盖 | 75.0 | 45 | 50.5 | 66.0 | 78.0 | 82 | 66.7 |
| 8 | 可复现性 | 48.0 | 30 | 35.0 | 52.5 | 70.0 | 88 | 37.5 |
| 9 | 表达与图表 | 63.0 | 50 | 62.8 | 73.0 | 80.0 | 80 | 25.0 |
| 10 | 潜在价值 | 82.0 | 60 | 68.0 | 75.0 | 80.0 | 85 | 87.5 |

## Macro comparison

| Macro | You | Min | Q1 | Median | Q3 | Max | Percentile |
|---|---:|---:|---:|---:|---:|---:|---:|
| 研究本身 | 80.0 | 54.6 | 56.0 | 62.9 | 67.7 | 73.8 | 100.0 |
| 论文本身 | 73.8 | 54.8 | 61.4 | 68.0 | 72.2 | 81.7 | 83.3 |
| 课题潜力 | 85.0 | 60.0 | 68.0 | 75.0 | 80.0 | 85.0 | 95.8 |

## Total

- **Your total:** 75.2
- **Reference range:** [56.5, 76.4] | Q1-Q3: [59.0, 70.3] | Median: 65.5 | Mean: 65.4 | σ: 6.4
- **Your percentile within this level:** 91.7

---

## Honest interpretation

This is an empirical LLM self-assessment of 12 papers accepted to YSA Vol.10. It is NOT a tier prediction, NOT a Yau/NeurIPS/CCF mapping, NOT a percentile against any real submission pool, NOT a threshold for acceptance. The 'YSA-10 STEM level' here means 'the empirical distribution of LLM self-scores for n=12 accepted papers in this specific volume'. Any future paper scoring within or above this distribution is *consistent with* — not *sufficient for* — acceptance at this venue. The skill author (Mavis) explicitly does not predict acceptance at any venue.

**What this comparison tells you:**
- Your paper's 75.2 falls within the observed range of 12 accepted papers in this volume (range [56.5, 76.4]).
- With ~±8 noise on both sides, the comparison is ±~8 in either direction.
- Being 'within the IQR' is consistent with — not sufficient for — acceptance. The IQR shows where the middle 50% of accepted papers fell on LLM self-scoring, not a threshold.

