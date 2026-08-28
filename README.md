# paper-rubric-review

> English | [中文版](./README.zh.md)

A 10-dimension scoring rubric for STEM papers, with two radar charts and a self-review workflow that has been stress-tested against the rubric's own past mistakes.

## What this is

A scoring framework for paper review. Each paper gets:

- 10 per-dimension scores (0-100%)
- A weighted total (0-100)
- 5 macro scores (problem / method / evidence / communication / scholarly) at the same 0-100 scale
- Two SVG radar charts (one macro, one per-dim)
- Optionally: a comparison against an empirical reference distribution of papers accepted to a real journal

The output is one markdown block with a per-dim table, the two radars, 3-5 strengths, 3-5 weaknesses with concrete fixes, and a "next 30 minutes" action.

The rubric is STEM-general, not ML-specific. ML-only checks (baselines, SOTA, ablations) are sub-bullets under the universal principle of "comparisons / evidence / uncertainty / replication". Theory papers, experimental physics, biochemistry, and algorithm papers all use the same 10 dimensions with different sub-field-aware "what to look for" lists.

## The 10 dimensions

| # | Dimension | Weight |
|---|-----------|-------:|
| 1 | 选题创新性 Problem originality | 20% |
| 2 | 方法原创性 Method originality | 15% |
| 3 | 方法严谨性 Methodological rigor | 10% |
| 4 | 实验验证 Experimental validation | 15% |
| 5 | 写作规范性 Writing quality | 10% |
| 6 | 结构与逻辑 Structure & logic | 5% |
| 7 | 文献覆盖 Literature coverage | 5% |
| 8 | 可复现性 Reproducibility | 5% |
| 9 | 表达与图表 Presentation & figures | 5% |
| 10 | 潜在价值 Future potential | 10% |

Total = Σ (score × weight). Each dim is scored 0-100% on the same scale, then weighted. The weights sum to 1.0.

For each dim, the scoring bands are:

- 90-95% — genuinely excellent, would be a strength in a gold-tier paper (cap at 95%, never 100)
- 75-89% — strong, standard publishable
- 60-74% — acceptable, several fixable issues
- 40-59% — significant issues, needs a real revision pass
- 20-39% — missing core elements
- 0-19% — absent or actively misleading

If you cannot find a quote in the paper to anchor a score, drop one band. The full band descriptions for each dim are in `references/rubric.md`.

## The 5 macros

The 10 dims collapse into 5 macro categories, each normalized to 0-100:

- **问题价值** (Problem) — Dim 1
- **方法严谨** (Method) — Dims 2+3
- **证据强度** (Evidence) — Dim 4
- **论文表达** (Communication) — Dims 5+6+9
- **学术价值** (Scholarly) — Dims 7+8+10

The macro radar uses these 5 axes. The 10-dim radar uses all 10 dims independently. Both use the same 0-100 scale so they're directly comparable.

The next-30-min fix should target the lowest macro, not necessarily the lowest single dim. A paper at 证据 85 / 表达 50 needs writing work first, even if 可复现性 is the single weakest dim.

## What this is NOT

This skill does not predict Yau Award / NeurIPS / ICML / ACL / CCF acceptance. The earlier version of this skill had a "tier mapping" that claimed to map scores to gold / silver / bronze. That claim was a heuristic without any calibration data, and was deliberately stripped out. A scoring rubric gives a self-reflection view, not a committee verdict.

There is one empirical reference: a distribution of LLM self-scores for n=12 STEM papers accepted to a published journal (YSA Yuanpei Young Scholars Journal Vol.10). See `references/calibration-data/README.md` for the honest-framing rules around that data. It is observation, not a threshold.

## A real example

This is the v2.3.1 strict review of an LLM hallucination paper. Real numbers, real output format.

| # | Dim | Score |
|---|-----|------:|
| 1 | Problem originality | 80% |
| 2 | Method originality | 75% |
| 3 | Methodological rigor | 72% |
| 4 | Experimental validation | 85% |
| 5 | Writing quality | 60% |
| 6 | Structure & logic | 90% |
| 7 | Literature coverage | 75% |
| 8 | Reproducibility | 48% |
| 9 | Presentation & figures | 63% |
| 10 | Future potential | 82% |
| | **Total** | **75.2** |

Macros: 问题价值 80, 方法严谨 73.8, 证据强度 85, 论文表达 68.3, 学术价值 71.8.

Score interpretation in absolute terms: 75.2 / 100. Strong overall. Research core is solid; remaining issues are polishing-level.

Empirical comparison vs YSA-10 STEM (n=12):

- Total 75.2 places at 91.7 percentile of the YSA-10 distribution (median 65.5, IQR [59.0, 70.3])
- The 论文表达 68.3 and 学术价值 71.8 sit in the lower half — writing and reproducibility are the actual gaps
- The 研究 side (问题 / 方法 / 证据) is at or above the IQR

Radar charts: see `examples/radar-5macro.svg` and `examples/radar-10dim.svg`. The full empirical comparison is in `examples/calibration-comparison.md`.

The 5-macro radar shows a healthy pentagon skewed toward research; the 10-dim radar makes the single weak dims (Dim 5 写作 at 60% and Dim 8 可复现 at 48%) visible. That is the whole point of running two radars: the macro view tells you which leg is short, the per-dim view tells you which single dim to fix first.

## Files

```
paper-rubric-review/
├── SKILL.md                                 main entry point, scoring scheme, procedure, output contract
├── references/
│   ├── rubric.md                            10-dim scoring details, sub-field aware
│   ├── reviewer-discipline.md               7 hard rules for scoring rigorously
│   ├── reading-discipline.md                input-layer rules (.pdf / .docx extraction)
│   ├── tier-mapping.md                       absolute score interpretation
│   ├── output-template.md                   copy-paste review template
│   ├── winning-papers-context.md            2020-2024 丘成桐 CS winners (context only)
│   └── calibration-data/                    YSA-10 STEM (n=12) empirical reference
├── scripts/
│   ├── radar-chart.js                       3-16 axis SVG radar (pure Node, no deps)
│   └── compare-calibration.py               empirical reference comparison
├── examples/                                sample radar + calibration output
├── LICENSE                                  MIT
└── .gitignore
```

## How to use this

The skill is a markdown-driven procedure. The LLM (or a human reviewer following the procedure) reads the paper, applies the rubric, and emits the output markdown.

To generate a radar chart from inline scores:

```bash
# 5-macro radar
node scripts/radar-chart.js '{"问题价值":80,"方法严谨":73.8,"证据强度":85,"论文表达":68.3,"学术价值":71.8}' --title "5-Macro Radar"

# 10-dim radar
node scripts/radar-chart.js '{"D1 选题":80,"D2 方法":75,"D3 严谨":72,"D4 实验":85,"D5 写作":60,"D6 结构":90,"D7 文献":75,"D8 可复现":48,"D9 图表":63,"D10 潜力":82}' --title "10-Dim Radar"
```

To compare against the YSA-10 reference:

```bash
python3 scripts/compare-calibration.py --level ysa10-stem \
  --scores "80,75,72,85,60,90,75,48,63,82" \
  --macros "80,73.8,85,68.3,71.8"
```

## Caveats

- ±8 point noise per score. LLM self-scoring has prompt sensitivity. If you re-run the same review on the same paper, expect 3-5 point variance on any dim. This is a known floor, not a bug.
- The YSA-10 STEM calibration is n=12, observation only. It is what 12 published STEM papers scored like under this rubric. It is not a threshold for acceptance.
- The reading discipline assumes the input has either text content or images that can be rasterized. Scan-only PDFs need OCR. Equations in Word .docx files often need to be re-typed or screenshotted because text extraction flattens them.

## Where the discipline came from

The 7 hard rules in `reviewer-discipline.md` are not theoretical. They are all lessons from the rubric's own past retraction incidents:

- Flagging DeepSeek V4 Pro / V4 Flash as a typo. They are real models (released April 2026).
- Claiming a v3 quote was missing from a v2.1.0 review. The quote was in v3 only; v2.1.0 had deleted it.
- Saying 2.2M parameters were not derived. The derivation was at line 397 in a Word equation object that text extraction had flattened.
- Calling §6.1 "Case Study" an empty section. It was an intentional placeholder.

The reading discipline comes from the same place: .docx equations flatten, .pdf formula characters scramble, partial reading overweights intro rhetoric. Both files exist because the cost of ignoring them was retracting reviews in front of the user.

## Why I built this

I built this for a specific job: review a high school student's STEM papers across multiple versions, give honest scores, surface the actual weak legs, and resist the temptation to inflate scores to be polite. The hard rules exist because the first version of the rubric failed at that job. The empirical reference exists because "I made up tier labels" was rightly called out.

If you want a tier-prediction rubric, this is not it. If you want a structured framework that scores a paper honestly and tells you which dim to fix next, this works.

## License

MIT, see LICENSE.
