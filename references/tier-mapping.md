# Score Interpretation Guide (was: Tier Mapping)

## Status: REWRITTEN 2026-08-16

**The previous version of this file contained tier labels (金 / 银 / 铜 / 优胜 for 丘成桐, NeurIPS / ICML / CCF-A / etc. for academic venues, "top 20-30% of recent Yau CS submissions" percentile language) that were not grounded in any actual Yau committee scoring data or systematic comparison against accepted papers.**

That content is removed. The skill no longer makes any tier or venue prediction.

## What the score means (in absolute terms)

The total is a 0-100 weighted sum of 10 per-dimension percentages. Treat the bands below as descriptions of the *score itself*, not as predictions of any external decision.

| Total | Description |
|---:|---|
| 90-100 | Exceptional across all dimensions. Few real papers reach this; even strong published work usually has at least one weak dimension. |
| 75-89 | Strong overall. Research core is solid; remaining issues are polishing-level. |
| 60-74 | Mixed. Some real strengths alongside real weaknesses; the paper needs a focused revision pass. |
| 45-59 | Below average for a submission-ready paper. Significant issues that need structural work, not just polish. |
| 30-44 | Major problems. Multiple dimensions are weak; consider whether the research is ready to be written up. |
| 0-29 | Not a paper yet. |

## What the macro scores mean

- **研究本身 (Research)**: original problem framing, original method, methodological rigor, experimental validation. *The core contribution.*
- **论文本身 (Paper)**: writing, structure, literature coverage, reproducibility, presentation. *How the contribution is communicated and made usable.*
- **课题潜力 (Potential)**: future work and significance. *Where this could go.*

A high Research macro with low Paper macro = "the work is good, the writeup needs work". A high Paper macro with low Research macro = "the writeup is polished but the substance is thin". These two failure modes need different fixes; the radar chart makes them visible.

## What the score does NOT predict

- It does **not** predict acceptance at 丘成桐 / NeurIPS / ICML / ACL / EMNLP / CCF-A / any other venue or award. The skill has no empirical data linking scores to actual committee decisions.
- It does **not** predict percentile rank against any real submission pool. Statements like "top 20% of Yau submissions" are removed.
- It does **not** mean the paper is correct. A paper can score 85 and still have an undiscovered error.
- It does **not** replace human review. It is one LLM's structured opinion, with ±8 points of noise from prompt sensitivity.

## What the score CAN tell you

- **Relative strength within a single paper**: which dimensions are the paper's strongest, which are weakest. This is reliable because it is anchored to quotes from your paper text.
- **Macro shape**: which leg of the research/paper/potential triangle is short. This is reliable for the same reason.
- **Specific, actionable fixes**: the weakest dimensions usually have well-known mechanical fixes (version-pinning, grammar pass, lit addition, etc.).
- **Trajectory under revision**: if you fix the listed weaknesses and re-run, the score will move in predictable ways (each dim is independent).

If you need a prediction of Yau / NeurIPS / etc. accept probability, you need either: (a) real calibration data (scored winners / accepted papers against the rubric), or (b) actual committee feedback. The skill provides neither.
