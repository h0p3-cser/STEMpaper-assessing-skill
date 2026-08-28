# Output Template — copy-paste skeleton

The skill's output contract is defined in `SKILL.md`; this file is the literal copy-paste version for the LLM to fill in.

Each dimension is scored 0-100%, the 5 macro scores are normalized weighted averages of their member dimensions, and the total is the full weighted sum. Show 1 decimal place.

**The output does NOT include any Yau / NeurIPS / CCF tier prediction.** The "Score interpretation" section uses the absolute scale in `tier-mapping.md` only.

```markdown
# Paper Review — <paper title or "untitled">

**Total: NN.N / 100**
**Stage assumed:** <outline | draft | near-final>
**No tier prediction** — see Score interpretation below.

## Macro scores (5-axis radar)

| Category                    | Score    | Note |
|-----------------------------|---------:|------|
| 问题价值 Problem             | NN.N / 100 | <strong / weak / balanced> |
| 方法严谨 Method              | NN.N / 100 | <strong / weak / balanced> |
| 证据强度 Evidence            | NN.N / 100 | <strong / weak / balanced> |
| 论文表达 Communication       | NN.N / 100 | <strong / weak / balanced> |
| 学术价值 Scholarly           | NN.N / 100 | <strong / weak / balanced> |

Radar chart: ![5-macro radar](<path/to/radar-macro.svg>)

## Per-dimension scores (each scored 0-100%, weighted into total)

| # | Dimension | Weight | Score | Justification (1 quote + line) |
|---|-----------|-------:|------:|-------------------------------|
| 1 | 选题创新性 Problem originality        | 20% |  NN% | "..." (line N) |
| 2 | 方法原创性 Method originality         | 15% |  NN% | "..." (line N) |
| 3 | 方法严谨性 Methodological rigor       | 10% |  NN% | "..." (line N) |
| 4 | 实验验证 Experimental validation       | 15% |  NN% | "..." (line N) |
| 5 | 写作规范性 Writing quality            | 10% |  NN% | "..." (line N) |
| 6 | 结构与逻辑 Structure & logic          |  5% |  NN% | "..." (line N) |
| 7 | 文献覆盖 Literature coverage          |  5% |  NN% | "..." (line N) |
| 8 | 可复现性 Reproducibility              |  5% |  NN% | "..." (line N) |
| 9 | 表达与图表 Presentation & figures     |  5% |  NN% | "..." (line N) |
| 10 | 潜在价值 Future potential             | 10% |  NN% | "..." (line N) |
| **Total** |                                  |**100%**|**NN.N**| weighted sum of above |

### Weighted-sum and macro example

If scores are 85, 80, 80, 80, 50, 95, 60, 40, 60, 80, then:

```
Total = 85·0.20 + 80·0.15 + 80·0.10 + 80·0.15 + 50·0.10
      + 95·0.05 + 60·0.05 + 40·0.05 + 60·0.05 + 80·0.10
     = 17.00 + 12.00 + 8.00 + 12.00 + 5.00
      + 4.75 + 3.00 + 2.00 + 3.00 + 8.00
     = 74.75 → 74.8

问题价值 macro = score_1                                  = 85.0
方法严谨 macro = (80·0.15 + 80·0.10) / 0.25              = 18.0/0.25 = 72.0
证据强度 macro = score_4                                  = 80.0
论文表达 macro = (50·0.10 + 95·0.05 + 60·0.05) / 0.20    = 13.25/0.20 = 66.3
学术价值 macro = (60·0.05 + 40·0.05 + 80·0.10) / 0.20    = 11.0/0.20 = 55.0
```

## Per-dimension radar (10-axis)

Use the 10-dim radar to spot single-dim weaknesses the macro aggregation hides.

Radar chart: ![10-dim radar](<path/to/radar-dim.svg>)

## Score interpretation

Use the absolute scale in `references/tier-mapping.md`. Examples of acceptable phrasings:

- "69.3 / 100 — mixed; strong research macro, weak paper macro. The paper needs a focused revision pass before submission."
- "82.1 / 100 — strong overall. Research core is solid; remaining issues are polishing-level."
- "45.0 / 100 — below average for a submission-ready paper; significant issues that need structural work, not just polish."

**Not acceptable** (these will be rejected by the rubric author):
- Yau tier labels (金/银/铜/优胜/半决赛/初审)
- Academic venue labels (NeurIPS / ICML / ACL / CCF-A/B/C)
- Percentile claims against any real submission pool ("top 20% of recent Yau submissions")
- Predictions of acceptance at any venue

## Strengths

1. <dimension name> — <NN%> — "<quoted phrase>" (line N) — why it works.
2. ...
3. ...

## Weaknesses (ranked by leverage)

1. <dimension name> — <NN%> — "<quoted phrase>" (line N) — **fix:** <concrete action>.
2. ...
3. ...
4. ...
5. ...

## Next-30-min fix

<one specific, executable change the author can do in 30 minutes; target the weakest macro category by default>

## Honest disclaimer

This is an LLM heuristic self-assessment, not a venue verdict. The score
has roughly ±8 point noise from prompt sensitivity. The skill does NOT
predict acceptance at 丘成桐 / NeurIPS / ICML / ACL / EMNLP / CCF or any
other venue. Use this as a self-reflection tool, not a guarantee.
```

## Optional appendix the LLM may add

- A "scoring rationale" paragraph per dimension (1-2 sentences) when the user asks for explanations.
- A "before / after" suggestion block for the top weakness (original sentence + rewritten version).
- A "submission-readiness verdict" at the end, in absolute terms only.

Do not add these by default — only when the user asks.

## How to generate the two radar charts

The skill bundles `scripts/radar-chart.js` (pure Node.js, no deps; supports 3-16 axes).

```bash
SKILL_DIR=<skill-dir>

# 5-macro radar
node "$SKILL_DIR/scripts/radar-chart.js" '{"问题价值":85,"方法严谨":72,"证据强度":80,"论文表达":66.3,"学术价值":55}' --title "5-Macro Radar" > /tmp/paper-review-radar-macro.svg

# 10-dim radar
node "$SKILL_DIR/scripts/radar-chart.js" '{"D1":85,"D2":80,"D3":80,"D4":80,"D5":50,"D6":95,"D7":60,"D8":40,"D9":60,"D10":80}' --title "10-Dim Radar" > /tmp/paper-review-radar-dim.svg
```

Then reference the SVG paths in the markdown under "Macro scores" and "Per-dimension radar" with `![caption](<path>)`.

Optional flags: `--max <N>` (default 100), `--rings <N>` (default 4), `--title "..."`.
