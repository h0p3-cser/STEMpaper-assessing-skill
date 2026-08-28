---
name: paper-rubric-review
description: |
  Multi-dimensional paper review with a fixed 10-dimension / 100-point rubric.
  Use when the user asks to "score my paper", "rate this draft", "做论文评分",
  or "evaluate this essay". Each of the 10 dimensions is scored 0-100%, then
  summed with fixed weights into a 0-100 total, plus 5 macro categories
  (Problem / Method / Evidence / Communication / Scholarly) for 5-axis radar,
  and a separate 10-dim radar for fine-grained dim-level diagnosis. Output
  includes 3-5 concrete actionable fixes. Does NOT predict Yau / NeurIPS /
  CCF tier — no calibrated mapping exists, and the skill will say so rather
  than invent one. Includes a Reviewer Discipline module (verify-before-
  deduct, multi-version strict, web-search model names, draft calibration,
  textutil caveat), a Reading Discipline module (.pdf / .docx extraction
  rules, cover-to-cover reading, do-not-let-abstract-set-the-score), and an
  optional empirical reference comparison (YSA-10 STEM, n=12) for
  observation-only comparison. All discipline rules are mandatory and
  grounded in past retraction incidents. Do NOT use for: ad-hoc
  single-sentence feedback, language polishing only (use
  high-school-lrs-paper-revision-coach instead), or generating paper text
  — this skill rates existing prose, it does not write it.
---

# paper-rubric-review

## Inputs to collect
- **Paper text or file path**. Accept .pdf / .docx / .md / .txt. If the user pastes a long draft, do not require re-paste.
- **Venue target** (optional). If the user mentions a target (e.g. 丘成桐, NeurIPS workshop, ACL SRW, EMNLP Findings), bias the tier-mapping commentary to that venue. Default: 丘成桐中学科学奖 (CS track). **This does NOT trigger any tier-prediction output**; the skill has no Yau/NeurIPS/CCF calibration data.
- **Stage** (optional). One of: `outline` / `draft` / `near-final`. This calibrates Dim 8 (Reproducibility) and what counts as a fair deduction — see `references/reviewer-discipline.md` §4.
- **Version** (if multi-versioned paper). When the user provides a v2.1.0 file but is editing from v3, treat the file given as the source of truth; do not carry forward v3-only quotes to the v2.1.0 review. See `references/reviewer-discipline.md` §2.

If a file path is given, read it directly. If the user only describes the paper, ask: "Can you paste the abstract + 1 page of body, or share the file path? I need concrete prose to score, not just the topic."

## Reviewer Discipline (read `references/reviewer-discipline.md` first)

The scoring rubric in `references/rubric.md` defines *what* to score. The discipline file defines *how* to score rigorously. **Both are required** — running the rubric without the discipline has produced 4+ point errors in past reviews. Mandatory rules, in priority order:

1. **Verify before deducting** — `grep` the actual paper for every quote you cite; every deduction needs a line number + exact quote. If you cannot find one, drop the score by one band or drop the criticism.
2. **Multi-version strict** — only quote from the version under review; never carry a v3 quote into a v2.1.0 review. Format cross-version comparison as "v3 had X but v2.1.0 deleted it" — never as "v2.1.0 has X".
3. **Verify unknown model / API / framework names via `web_search`** before flagging them as typos. Models evolve fast; the rubric author's training cutoff is unlikely to cover them.
4. **Draft review calibration** — when the user says "this is a draft" or "I'll add that at final review", do not deduct heavily for things that will be added at final submission (GitHub link, model id, BGE version, etc.).
5. **Textutil / docx-extraction caveat** — when the paper is provided as .docx, formulas (Word equation objects) and figures may be lost in plain-text extraction. If the user says "the formula is in the docx", trust them; do not dock for "missing derivation". Caveat: typos in the surrounding text (e.g., "δ" vs "γ") are still real.
6. **Strict is honest, not punitive** — when the user asks for strict scoring, apply lower bands and show explicit deltas vs the previous version. But do not invent flaws, and do not penalize for things that legitimately exist in the paper.
7. **When the user pushes back, retract cleanly** — if the user provides verifiable evidence (a line number, a web search result), retract the original criticism fully and update the score. Do not defend the original or split the difference.

Full version of these rules, with worked examples from past retraction incidents, is in `references/reviewer-discipline.md`. Read it before delivering any review.

## Reading Discipline (read `references/reading-discipline.md` first)

The reviewer discipline covers how to *score*; the reading discipline covers how to *read the input*. Without reading discipline, the review can systematically mis-score because the input is corrupted (text extraction dropped equations) or partial (LLM read only the abstract).

Two failure modes the reading discipline addresses:

1. **Decoding corruption** — `.docx` formulas / figures / tables / Greek-letter text-side rendering can be lost; `.pdf` formula characters can scramble. The LLM then either docks the paper for "missing" content that was actually there, or misses content that was actually missing. See `references/reading-discipline.md` §"Per-format rules" for the .pdf / .docx / .txt / scan-only rules.

2. **Partial-reading bias** — the LLM reads only the abstract, only the intro, only the first 1-2 pages, and treats that fragment as the whole paper. The review then overweights intro rhetoric and underweights the body of evidence. See `references/reading-discipline.md` §"Partial-reading discipline" for the cover-to-cover, do-not-let-abstract-set-the-score, visit-figures, and last-section-bias rules.

The reading discipline is **prerequisite** to the reviewer discipline: bad reading → bad scoring, no matter how good the rubric.

## Scoring scheme

**Two levels: 10 dimensions → 3 macro categories → 1 total.**

### Level 1 — 10 dimensions, each 0-100%

| # | Dimension | Weight |
|---|-----------|-------:|
| 1 | 选题创新性 Problem originality         | 20% |
| 2 | 方法原创性 Method originality          | 15% |
| 3 | 方法严谨性 Methodological rigor        | 10% |
| 4 | 实验验证 Experimental validation        | 15% |
| 5 | 写作规范性 Writing quality             | 10% |
| 6 | 结构与逻辑 Structure & logic           |  5% |
| 7 | 文献覆盖 Literature coverage           |  5% |
| 8 | 可复现性 Reproducibility               |  5% |
| 9 | 表达与图表 Presentation & figures      |  5% |
| 10 | 潜在价值 Future potential              | 10% |
|   | **Total**                              | **100%** |

### Level 2 — 5 macro categories, each 0-100% (independent scale)

| # | Category | 中文 | Dims | Combined weight |
|---|----------|------|------|----------------:|
| 1 | **问题价值** (Problem)        | 选题原创性 | 1 | 20% |
| 2 | **方法严谨** (Method)         | 方法原创 + 方法严谨 | 2, 3 | 25% |
| 3 | **证据强度** (Evidence)       | 实验验证 | 4 | 15% |
| 4 | **论文表达** (Communication)  | 写作 + 结构 + 图表 | 5, 6, 9 | 20% |
| 5 | **学术价值** (Scholarly)      | 文献 + 可复现 + 未来 | 7, 8, 10 | 20% |

Macro score formula: `macro_X = (Σ dim_i × weight_i for i in X) / (Σ weight_i for i in X) × 100`. The denominator normalizes each macro to 0-100 regardless of the original weight sum, so the 5 macros are directly comparable on the radar chart.

### Level 3 — Total

`Total = Σ (score_i × weight_i)` over all 10 dims, where `weight_i` is from the table above. Total is in [0, 100]. The total is the same value the per-category macros are derived from; it answers "what score would this paper get, full stop?" while the macros answer "which leg is short?".

Why this 3-level scheme:
- 10 dimensions alone gives one number, but a paper with 80% problem / 50% paper / 80% scholarly is very different from 70% across the board. The macro view exposes that.
- 5 macros split the research process into 3 stages (problem / method / evidence) and 2 output dimensions (communication / scholarly value). This is more diagnostic than 3.
- 2 axes = line, 3 = triangle (too coarse for STEM where you want to separate problem/method/evidence), 4 = quadrilateral (loses the "research vs paper" axis distinction), 5 = pentagon (right balance of granularity and readability), 6+ = noisy.

### Radar charts (2 of them)

The skill generates **two radar charts**:

1. **5-macro radar** — high-level diagnostic. Use it to see "which leg is short". Always show.
2. **10-dim radar** — fine-grained diagnostic. Use it to spot a single weak dim that the macro aggregation hides. Optional but recommended when a paper has at least one dim < 50%.

Run `scripts/radar-chart.js` for each:

```bash
# 5-macro
node <skill-dir>/scripts/radar-chart.js '{"问题价值":85,"方法严谨":80,"证据强度":80,"论文表达":60,"学术价值":80}' --title "5-Macro Radar" > /tmp/radar-macro.svg

# 10-dim
node <skill-dir>/scripts/radar-chart.js '{"D1":85,"D2":80,"D3":80,"D4":80,"D5":50,"D6":95,"D7":60,"D8":40,"D9":60,"D10":80}' --title "10-Dim Radar" > /tmp/radar-dim.svg
```

The script accepts any number of axes (3-16) and a JSON object of label→value pairs. Optional flags: `--max <N>` (default 100), `--rings <N>` (default 4), `--title "..."`. No external dependencies; pure Node.js.

Why uniform 0-100% per dimension:
- Cross-paper comparison is fair: a 70% on Dim 8 (reproducibility) is directly comparable to a 70% on Dim 1 (originality).
- LLMs are more reliable at 0-100% scoring than at variable-max scales.
- Per-dimension % makes strengths and weaknesses visually obvious in the output table.

## Procedure
1. **Pre-flight check** (read `references/reviewer-discipline.md` first). Identify paper version, identify any model / API / framework names that need `web_search` verification, confirm submission state (draft / near-final / final). Run the discipline pre-flight checklist.
   Why: catches the most common retraction-causing errors before any scoring happens.
2. Read the rubric in `references/rubric.md` first. The 10 dimensions, 3 macro categories, weights, and percentage bands are fixed; do not rebalance per paper.
   Why: a stable rubric is what makes the score comparable across runs.
3. Score each dimension on the 0-100% scale using the bands in `references/rubric.md`. Cite 1-2 short quoted phrases from the paper per dimension to justify the score; if you can't, drop the score by one band.
   Why: anchoring every score to a quote makes the review falsifiable and the user can argue specific lines.
4. Compute the 3 macro scores using the formulas in `## Scoring scheme` above. Then compute the total. Map the total to a tier using `references/tier-mapping.md`. Always output the total, the 3 macro scores, and the tier label.
5. Generate a radar chart by running the script in `scripts/radar-chart.js` with the 3 macro scores. Reference the resulting SVG in the output.
   Why: a single total hides which leg is short. The radar makes the diagnosis visible at a glance.
6. Pick 3 strengths (highest-scoring dimensions, or strongest sub-evidence) and 3-5 weaknesses (lowest-scoring dimensions, with a specific fix). The "Next-30-min fix" should target the weakest macro category unless the user is explicitly asking about a specific dimension.
7. If the paper is <2 pages or only an abstract, score dimensions with `n/a` rather than guess, halve the total to a "preview" score, and tell the user to share the full draft.
8. **Post-flight check** — before delivering, run the discipline post-flight checklist: every <90% score has a line+quote justification; no model names flagged without web_search verification; no Yau / NeurIPS / venue tier / percentile claims; total = exact weighted sum, 1 decimal place.
9. **(Optional) Empirical reference comparison** — AFTER delivering the review, ask the user ONE question:
   - **"Would you like to see where your paper's scores fall against an empirical reference level (e.g., the distribution of papers accepted to YSA Journal Vol.10 STEM)?"**
   - If the user says **yes**: load the relevant level from `references/calibration-data/levels.json`, run `scripts/compare-calibration.py --level <id> --from-json <review.json>` (or pass scores directly), and append a `## Empirical reference comparison` section to the output.
   - If the user says **no** or doesn't respond: skip Step 9 entirely. Never force this on the user.
   - **Honest framing rules (HARD):**
     - NEVER say "your paper is in tier X" or "this is the Yau accept score".
     - Always say "your paper's N falls within the observed range of M papers that achieved milestone Z" or "your paper is consistent with / above / below the observed range".
     - Always include the noise floor (±8 points) and the selection criteria (e.g., "all 12 STEM papers in Vol.10").
     - Always include the disclaimer that the comparison does NOT predict acceptance, is NOT a threshold, and is NOT a venue mapping.
   - The comparison is observational reference data only. Adding a new level requires scoring n≥5 papers of the same milestone type and adding them to the registry — see `references/calibration-data/README.md`.

## Output contract
A single markdown block with these sections, in this order:

```
# Paper Review — <paper title or "untitled">

**Total: NN.N / 100**
**Stage assumed:** <outline|draft|near-final>
**No tier prediction** — see Score interpretation below.

## Macro scores (3-axis radar)

| Category | Score | Strength / Weakness |
|----------|------:|---------------------|
| 研究本身 Research  | NN.N / 100 | <strong or weak> |
| 论文本身 Paper     | NN.N / 100 | <strong or weak> |
| 课题潜力 Potential | NN.N / 100 | <strong or weak> |

Radar chart: ![radar](<path/to/radar.svg>)  *(or describe in text if SVG rendering unavailable)*

## Per-dimension scores (each scored 0-100%, weighted into total)

| # | Dimension | Weight | Score | Justification (1 quote) |
|---|-----------|-------:|------:|--------------------------|
| 1 | 选题创新性 Problem originality        | 20% |  NN% | "..." |
| 2 | 方法原创性 Method originality         | 15% |  NN% | "..." |
| 3 | 方法严谨性 Methodological rigor       | 10% |  NN% | "..." |
| 4 | 实验验证 Experimental validation       | 15% |  NN% | "..." |
| 5 | 写作规范性 Writing quality            | 10% |  NN% | "..." |
| 6 | 结构与逻辑 Structure & logic          |  5% |  NN% | "..." |
| 7 | 文献覆盖 Literature coverage          |  5% |  NN% | "..." |
| 8 | 可复现性 Reproducibility              |  5% |  NN% | "..." |
| 9 | 表达与图表 Presentation & figures     |  5% |  NN% | "..." |
| 10 | 潜在价值 Future potential             | 10% |  NN% | "..." |
| **Total** |                                  |**100%**|**NN.N**| weighted sum of above |

### Weighted-sum example
If scores are 85, 80, 80, 80, 50, 95, 60, 40, 60, 80, then:

Total = 85·0.20 + 80·0.15 + 80·0.10 + 80·0.15 + 50·0.10 + 95·0.05 + 60·0.05 + 40·0.05 + 60·0.05 + 80·0.10
     = 17.0 + 12.0 + 8.0 + 12.0 + 5.0 + 4.75 + 3.0 + 2.0 + 3.0 + 8.0
     = 74.75

Macro:
- 研究 = (85·0.20 + 80·0.15 + 80·0.10 + 80·0.15) / 0.60 = 49.0 / 0.60 = 81.7
- 论文 = (50·0.10 + 95·0.05 + 60·0.05 + 40·0.05 + 60·0.05) / 0.30 = 17.75 / 0.30 = 59.2
- 潜力 = 80.0

## Score interpretation
Describe what the total and macros mean using the absolute scale in `references/tier-mapping.md` (the "Score interpretation guide"). Do NOT map to Yau tiers, NeurIPS / ICML / CCF, or any external venue. Do NOT cite percentiles against any real submission pool. Examples of acceptable language:
- "69.3 / 100 — mixed; strong research macro, weak paper macro. The paper needs a focused revision pass before submission."
- "82.1 / 100 — strong overall. Research core is solid; remaining issues are polishing-level."

Not acceptable (will be rejected by the rubric author):
- "85+ / 100 → likely 银奖候选"  (no Yau calibration data)
- "Top 20% of NeurIPS submissions"  (no NeurIPS calibration data)
- "Ready for ACL Findings"  (no acceptance-rate data)

## Strengths
1. <dim + score + quote + why it works>
2. ...
3. ...

## Weaknesses (ranked by leverage)
1. <dim + score + quote + 1 concrete fix> — **fix:** <action>
2. ...
3. ...
4. ...
5. ...

## Next-30-min fix
<one specific, executable change the author can do in 30 minutes; target the weakest macro category by default>

## Honest disclaimer
This is an LLM heuristic self-assessment, not a venue verdict. The score
has ~±8 point noise from prompt sensitivity. The skill does NOT predict
acceptance at 丘成桐 / NeurIPS / ICML / ACL / EMNLP / CCF or any other
venue. Use this as a self-reflection tool, not a guarantee.

## Empirical reference comparison (optional, only if user opted in at Step 9)
```
## Empirical reference comparison

**Reference level:** <level_name_zh>  
**n_papers in reference:** <N>  
**Selection:** <how papers were chosen, e.g., "all 12 STEM papers in YSA Vol.10">  
**Noise floor:** ±8 points (per skill documentation)  
**Selection caveat:** This comparison is observational. It does NOT predict acceptance.

### Per-dimension comparison
| # | Dim | You | Min | Q1 | Median | Q3 | Max | Your percentile |
|---|--- |---:|---:|---:|---:|---:|---:|---:|
| 1 | 选题创新性 | NN | NN | NN | NN | NN | NN | NN% |
| ... (rows for all 10 dims, 3 macros, total) |

### Honest interpretation
<the disclaimer from the level JSON + a one-paragraph "what this tells you" — using ONLY observation language: "consistent with / above / below the observed range", never "tier X", "accept score", "Yau gold", etc.>
```

If the user did not opt into Step 9, omit this section entirely.
```

Hard rules:
- Never give a 100. Cap top dimension at 95% even for an apparent strong paper.
- Never inflate scores to be polite. The user's stated goal is "honest, directional feedback"; an inflated score is worse than an honest 65.
- If a quote is not in the paper, the justification column reads "(no on-point quote found, see 'Weaknesses')" — do not paraphrase the abstract as if it were evidence.
- Total = exact weighted sum, not rounded. Show 1 decimal place.
- Do NOT use Yau tier labels (金/银/铜/优胜/半决赛/初审) in the output.
- Do NOT use venue tier labels (NeurIPS / ICML / CCF-A/B/C / etc.) in the output.
- Do NOT cite percentiles against any real submission pool.
- The "Score interpretation" section must use the absolute scale in `references/tier-mapping.md` only.
- **Every score < 90% must have a line number + exact quote justification.** No exceptions. If you cannot produce one, drop the score by one band.
- **Before flagging any model / API / framework name as a typo, run `web_search` to verify.** The rubric author's training cutoff is unlikely to cover recent model releases.
- **No cross-version quote carryover.** A criticism valid for v3 may be wrong for v2.1.0. Re-grep every quote in the current version.

## Failure handling
- User asks "am I going to win?": refuse. The skill does not predict awards. Direct them to real reviewer feedback (mentor, sample reviewer, submission to a low-stakes venue for calibration).
- User asks "where does this stand vs NeurIPS?": refuse and explain. The skill has no NeurIPS calibration data. Direct them to look at actual accepted papers at that venue and compare substance, not scores.
- User asks for just a single number: refuse politely and give the full table — a single number without dimensions is un-actionable.
- Dimension evidence missing: write `n/a` and a one-line reason. If >3 dimensions are n/a, switch to "preview" mode and halve the total.

## Examples

**Example 1** (early outline, NLP direction)
Input: a 1-page outline for "BGE geometric features for LLM hallucination detection", 1 page of methods, no experiments yet.
Output: a `preview` score ~58/100, strengths on problem framing, weaknesses on missing experiments and reproducibility, Next-30-min fix = "write a Table 1 of competing methods with their geometric features used." Score interpretation: "preview only — needs more draft before actionable."

**Example 2** (near-final draft, full paper)
Input: a 12-page draft with results.
Output: full 10-dimension scoring, 3 macro scores, radar chart, score interpretation in absolute terms only (no tier prediction), 3 strengths + 5 weaknesses + 30-min fix.

## References
- `references/rubric.md` — 10 dimensions, 5 macro categories, weights, 0-100% bands, what to look for, common weaknesses (STEM-general, sub-field aware)
- `references/tier-mapping.md` — score interpretation guide (absolute scale only, no external venue prediction)
- `references/winning-papers-context.md` — 2020-2024 丘成桐 CS winners (context only, NOT for tier calibration)
- `references/output-template.md` — the full output template as a copy-pasteable skeleton
- `references/reviewer-discipline.md` — **mandatory** judgment-layer discipline: verify-before-deduct, multi-version strict, web_search model verification, draft calibration, textutil caveat.
- `references/reading-discipline.md` — **mandatory** input-layer discipline: .pdf / .docx / .txt / scan-only extraction rules, cover-to-cover reading, do-not-let-abstract-set-the-score, visit-figures, last-section-bias. **Read this before reading the paper** to avoid decoding-corruption and partial-reading bias.
- `references/calibration-data/` — empirical reference levels (observational comparison data, NOT tier predictions). Currently includes `ysa10-stem` (n=12, YSA Yuanpei Young Scholars Journal Vol.10 STEM, scored 2026-08-27, median total 65.5 / IQR [59.0, 70.3]). See `references/calibration-data/README.md` for how to add new levels and the honest-framing rules.
- `scripts/radar-chart.js` — pure-Node.js SVG radar chart generator (3-16 axes, 0-100 scale, supports arbitrary category labels in any language)
- `scripts/compare-calibration.py` — compare a scored paper against a reference level. Used in Step 9 (optional empirical reference comparison).

## Skill scripts

This skill bundles three scripts:

- `scripts/radar-chart.js` — accepts any JSON object `{label: 0-100, ...}` (3-16 keys), writes an SVG radar chart to stdout. Optional flags: `--max <N>`, `--rings <N>`, `--title "..."`. No external dependencies. Examples:
  ```bash
  # 5-macro radar
  node <skill-dir>/scripts/radar-chart.js '{"问题价值":85,"方法严谨":80,"证据强度":80,"论文表达":60,"学术价值":80}' --title "5-Macro Radar"
  
  # 10-dim radar
  node <skill-dir>/scripts/radar-chart.js '{"D1":85,"D2":80,"D3":80,"D4":80,"D5":50,"D6":95,"D7":60,"D8":40,"D9":60,"D10":80}' --title "10-Dim Radar"
  ```
- `scripts/compare-calibration.py` — Python 3 (stdlib only). Used at Step 9. Takes `--level <level_id>` plus either `--scores "d1,d2,..." --macros "R,P,Pot"` or `--from-json <review.json>`. Emits a markdown table comparing the user's scores against the level's distribution with observation language (not threshold language). Example:
  ```bash
  python3 scripts/compare-calibration.py --level ysa10-stem --from-json path/to/review.json
  ```

## Windows (win32) platform notes

This skill is platform-agnostic (pure Node.js, no shell-only commands). On Windows:

- `node` ships with the standard Node.js LTS install. Get it from https://nodejs.org if missing.
- File paths in the radar-chart command work the same; use forward slashes or escaped backslashes.
- The `> file.svg` redirect is supported in both PowerShell and cmd.exe.
- If you want to embed the SVG inline in markdown instead of as a file, open the SVG in any browser, copy the rendered text, and paste it into the markdown between `<svg>...</svg>` fences.
