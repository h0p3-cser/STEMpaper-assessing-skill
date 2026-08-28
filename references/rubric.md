# Paper Rubric — 10 dimensions / 100% per dim / weighted total

A fixed rubric for paper review. All 10 dimensions are scored on the same 0-100% scale. The total is a weighted sum using the weights below. Do not rebalance per paper; if the paper is in an area where one dimension seems irrelevant, score it `n/a` and explain.

## Weight table (fixed)

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

**Total = Σ (score_i × weight_i)** with weights in decimal (0.20, 0.15, ..., 0.10). Total is in [0, 100].

## Macro categories (5-axis radar)

The 10 dimensions collapse into **5 macro categories** (used for the 5-axis radar chart). Each macro is computed as a **normalized weighted average** of its member dimensions, so all 5 macros share a 0-100 scale.

| # | Macro | 中文 | Member dims | Sum of dim weights | Normalized formula |
|---|-------|------|-------------|-------------------:|--------------------|
| 1 | **问题价值** (Problem)    | 选题原创性 | 1 | 0.20 | `score_1` |
| 2 | **方法严谨** (Method)     | 方法原创 + 方法严谨 | 2, 3 | 0.25 | `(score_2×0.15 + score_3×0.10) / 0.25` |
| 3 | **证据强度** (Evidence)   | 实验验证 | 4 | 0.15 | `score_4` |
| 4 | **论文表达** (Communication) | 写作 + 结构 + 图表 | 5, 6, 9 | 0.20 | `(score_5×0.10 + score_6×0.05 + score_9×0.05) / 0.20` |
| 5 | **学术价值** (Scholarly)  | 文献 + 可复现 + 未来 | 7, 8, 10 | 0.20 | `(score_7×0.05 + score_8×0.05 + score_10×0.10) / 0.20` |

Why this 5-way split:
- **问题 vs 方法 vs 证据** splits the research process into 3 distinct stages: framing, design, and validation. A paper can be strong on one and weak on another; the radar makes it visible.
- **论文表达 vs 学术价值** separates "how well is this paper written and presented" (Communication) from "how does it sit in the scholarly ecosystem" (Scholarly — lit positioning, reproducibility, future direction).
- 5 axes is the right count for a radar. 2 = line, 3 = triangle (too coarse for STEM where you want to separate problem/method/evidence), 4 = quadrilateral, 6+ = hard to read at a glance.
- The next-30-min fix should target the lowest macro, not necessarily the lowest single dimension. (Example: a paper at 问题 85% / 方法 50% needs method work first, even if one specific 论文 dim like 写作 is at 40% — the macro is the unit of action.)

### Per-dimension radar (10-axis)

In addition to the 5-macro radar, generate a 10-dimension radar that shows every dim independently. Use it when you want to spot a single weak dim that the macro aggregation hides. Example: a paper with 论文表达 70% (looking healthy) might be hiding 可复现性 at 30% — the 10-dim radar makes this visible.

## Score bands (uniform across all dimensions)

| Band | Range | What it means |
|---|---|---|
| **Top** | 90-100% | Genuinely excellent; would be a strength even in a gold-tier paper. Cap at 95% — never give 100. |
| **Upper** | 75-89% | Strong with minor issues. Standard publishable in most venues. |
| **Middle** | 60-74% | Acceptable; several fixable issues. Reviewer would request revisions, not reject. |
| **Lower** | 40-59% | Significant issues that need a real revision pass. |
| **Weak** | 20-39% | Missing core elements or fundamentally flawed on this dimension. |
| **Bottom** | 0-19% | Absent or actively misleading. |

When you cannot find a quote to anchor the score, drop one band. When the paper has both an exceptional strength and a notable weakness on the same dimension, score the average and call out the split in the justification.

## Coverage map — how this rubric aligns with known review systems

This rubric is designed to be **STEM-general**. The 10 dimensions and 5 macros map to standard review frameworks:

| This rubric dim | 丘成桐 5 official | NeurIPS 4 | NIH scientific rigor | Field-specific reporting standards |
|---|---|---|---|---|
| 1. 选题创新性 | 选题及解决问题方法的创新性 | Originality | (Significance) | — |
| 2. 方法原创性 | 解决问题方法的创新性 + 研究思路原创性 | Originality | Approach | — |
| 3. 方法严谨性 | 学术规范性、严谨性 | Soundness | Rigor (strict application of the scientific method) | CONSORT / PRISMA / ARRIVE / MIAME / STROBE / STARD |
| 4. 实验验证 | (implicit under 严谨性) | Empirical rigor | Robust unbiased design | CONSORT / STROBE / field-specific |
| 5. 写作规范性 | 论文写作的学术规范性、严谨性 | Clarity | Reporting completeness | — |
| 6. 结构与逻辑 | 论文写作的学术规范性、严谨性 | Clarity | Logical organization | — |
| 7. 文献覆盖 | (implicit) | (NeurIPS doesn't grade) | Contextual placement | — |
| 8. 可复现性 | (implicit under 严谨性) | Reproducibility | Reproducibility (NAS 2019 definition) | — |
| 9. 表达与图表 | 论文写作的学术规范性 | Clarity | Data presentation integrity | — |
| 10. 潜在价值 | 对未来科学发展的潜在价值 | Significance | Future directions | — |

丘成桐 official criterion #4 (团队协作) is not reviewable from a paper alone; flag it in the disclaimer.

---

## Dimension 1 — 选题创新性 (Problem Originality) — weight 20%

What to look for:
- Is the problem genuinely under-addressed, or a re-run of well-trodden work with new data?
- Does the framing expose a new angle, a new constraint, or a new evaluation lens?
- For 丘成桐 CS: does the topic feel "competition-worthy" — i.e., would an undergraduate researcher find it interesting?

Scoring bands:
- **90-95%** — Topic is novel AND the framing is non-obvious. Reviewers would say "interesting question".
- **75-89%** — Topic is a known sub-problem but the framing adds something. Standard publishable.
- **60-74%** — Topic is well-trodden, framing is mostly standard.
- **40-59%** — Topic is largely a replication of X with minor variation.
- **20-39%** — Topic is a class assignment, no research question.
- **0-19%** — Topic is missing or incoherent.

Common weaknesses:
- "We are the first to study X" but X is a slight variant of an existing dataset / task definition.
- Problem is interesting but the paper does not state a falsifiable research question.
- Problem statement is too broad; "improve LLM reasoning" is a topic, not a question.

---

## Dimension 2 — 方法原创性 (Method Originality) — weight 15%

What to look for (universal across STEM):
- Is the contribution a new **method** — algorithm, model, theorem, experimental setup, instrument, derivation, or analytical framework — or a recombination of existing pieces?
- If recombination, is the combination itself non-obvious and well-motivated?
- For empirical work: is the experimental design itself a contribution (new probe, new benchmark, new measurement)?

By sub-field:
- **ML / AI / systems**: new algorithm, loss, architecture, protocol, framework.
- **Theoretical math / CS**: new theorem, proof technique, complexity bound, construction.
- **Experimental physics / chemistry / biology**: new apparatus, measurement procedure, sample preparation, experimental design.
- **Algorithms / applied CS**: new data structure, algorithm, optimization, system design.

Scoring bands:
- **90-95%** — Method has at least one genuinely new piece AND it's well-motivated.
- **75-89%** — Combination of known techniques, but the combination is the contribution.
- **60-74%** — Standard pipeline + one new component.
- **40-59%** — Pure application of an existing method to a new problem or dataset.
- **20-39%** — Method is unclear or no method section.
- **0-19%** — Method is missing or contradicts the rest of the paper.

Common weaknesses:
- "We propose a novel method" but the method is just `embed(X) → MLP → classify` with no justification for *why* this captures the phenomenon.
- Method is a thin wrapper around an existing tool; the paper reads like a usage tutorial.
- Method has many components but no ablation / no isolation of which piece matters.
- For theory: "by similar argument" handwaving in place of full proofs.
- For experiments: using a standard instrument without calibrating it or explaining why it fits the question.

---

## Dimension 3 — 方法严谨性 (Methodological Rigor) — weight 10%

**Universal principle** (NIH definition): "the strict application of the scientific method to ensure robust and unbiased experimental design, methodology, analysis, interpretation and reporting of results."

What to look for, by sub-field:

**ML / AI / systems**:
- Math / proofs / derivations correct, no handwaving.
- Training procedure fully specified (hyperparameters, seeds, compute, software versions).
- All design choices justified.

**Theoretical math / CS**:
- Theorem statements precise, assumptions listed.
- Proofs complete, key lemmas expanded.
- Cited prior work accurate; standard facts referenced rather than re-proved.
- Counterexamples (where applicable) explicit.

**Experimental physics / chemistry / biology**:
- Positive and negative controls present.
- Adequate sample size, randomization, blinding where appropriate.
- Calibration procedure described.
- Bias limitation measures stated.

**Algorithms / applied CS**:
- Pseudocode or implementation detail for the core method.
- Computational complexity analyzed.
- Convergence tests performed and documented.
- Benchmarked against known analytical or experimental results.

**Universal elements (any STEM)**:
- Statistical methods appropriate and clearly explained.
- Sample size justified (power analysis for hypothesis-testing studies).
- Multiple testing correction applied where applicable.
- Confidence intervals or effect sizes reported alongside p-values.
- Assumptions of methods stated and tested.
- Limitations of the method acknowledged.

Scoring bands:
- **90-95%** — Method fully specified, derivations / procedures clean, no obvious gaps.
- **75-89%** — Mostly specified, 1-2 unspecified choices (e.g., "we tuned on dev" without grid).
- **60-74%** — Several important details missing or handwaved.
- **40-59%** — Method description is a black box.
- **20-39%** — Method contradicts itself or relies on undefined terms.
- **0-19%** — No method description.

Common weaknesses:
- Hyperparameters / model versions / configuration stated in prose but not in a table.
- "We tried several configurations and report the best" without disclosing the rest.
- Definitions in the method section don't match the math in the appendix.
- For experiments: no controls, no randomization, or no blinding where appropriate.
- For computational: convergence criteria, basis sets / k-points, or system size not documented.
- Reporting standards (CONSORT, PRISMA, ARRIVE, MIAME, STROBE, STARD — by sub-field) not followed.

---

## Dimension 4 — 实验验证 (Experimental Validation) — weight 15%

What to look for (universal across STEM):
- Are there sufficient **comparisons** to evaluate the claim?
- Is the **evidence** appropriate to the claim being made (statistical, theoretical, empirical)?
- Are controls present and adequate?
- Is uncertainty quantified (error bars, confidence intervals, statistical / systematic errors)?
- Is the work **replicated** (technical replicates, biological replicates, repeated runs)?

By sub-field:
- **ML / AI / systems**: baselines (incl. SOTA) + meaningful ablations + multiple datasets / multiple models.
- **Theoretical math / CS**: independent verification via proof or numerical example; comparison with prior bounds.
- **Experimental physics / chemistry / biology**: comparison with prior measurements; replication; control groups; uncertainty quantification (statistical and systematic errors distinguished).
- **Algorithms / applied CS**: comparison with prior algorithms on standard benchmarks; complexity analysis validated by experiment.

Scoring bands:
- **90-95%** — Strong comparisons, multiple evidence sources, meaningful isolation of design choices, uncertainty properly quantified.
- **75-89%** — Decent comparisons but missing SOTA / prior work; or one dataset; or no ablation.
- **60-74%** — Minimal comparisons, single evidence source, vague "we also tried X".
- **40-59%** — No real comparison, only cherry-picked examples.
- **20-39%** — Experiments exist but don't support the claims.
- **0-19%** — No experiments or experiments are broken.

Common weaknesses:
- "We outperform prior work" but the comparison is against weaker baselines / outdated methods.
- Ablation table exists but the variants are not informative (e.g., removing two things at once).
- No uncertainty quantification, even when it's free (multiple runs).
- No analysis section: error breakdown, case study, qualitative examples.
- For experiments: no replication; for theory: no example / numerical check.
- Selective reporting: only the successful trials, only the best hyperparameters.

---

## Dimension 5 — 写作规范性 (Writing Quality) — weight 10%

What to look for:
- Sentence-level: grammar, tense, jargon discipline (don't use "novel" 14 times).
- Paragraph-level: one claim per paragraph, clear topic sentence.
- Voice: active where possible, no unnecessary nominalizations ("the utilization of" → "use").
- Citations: every cited claim has a real reference; every reference is cited in body.
- Math notation: consistent, defined on first use, no symbol collisions.

Scoring bands:
- **90-95%** — Reads as a near-publishable paper, with at most 1-2 sentence-level fixes.
- **75-89%** — Generally well-written but a recurring grammar/usage pattern drags the score.
- **60-74%** — Several grammar / style issues; reviewer would underline sentences.
- **40-59%** — Reads like a rough first draft, not yet at submission quality.
- **20-39%** — Multiple sentences are incomprehensible.
- **0-19%** — Writing prevents understanding the content.

Common weaknesses:
- "we haven't explain" / "For my apology" / "The model can predict well because it can" — surface grammar.
- Mixing tenses: "We propose X. The model was trained on Y. We will show..."
- Acronyms undefined on first use.
- "Significant" used loosely (statistical vs. practical).

---

## Dimension 6 — 结构与逻辑 (Structure & Logic) — weight 5%

What to look for:
- Does the abstract preview the contribution honestly, or oversell?
- Is the introduction structured as: hook → problem → gap → contribution → outline?
- Does each section end with a "what this section established" sentence, and does the next section open from it?
- Is the conclusion a summary of evidence, or a sales pitch?

Scoring bands:
- **90-95%** — Reader can extract the contribution in 30 seconds from the abstract, and the body delivers exactly that.
- **75-89%** — Structure is mostly there but one section drifts from the central claim.
- **60-74%** — Sections feel like a list of things the author did, not an argument.
- **40-59%** — No recognizable structure; introduction, method, experiments could be reordered.
- **20-39%** — Structure actively misleads.
- **0-19%** — No structure.

Common weaknesses:
- Abstract oversells: "We propose a novel framework" when the paper actually evaluates an existing one.
- Method section introduces a component the introduction didn't motivate.
- Conclusion repeats the abstract verbatim.

---

## Dimension 7 — 文献覆盖 (Literature Coverage) — weight 5%

What to look for:
- Are the top 5-10 most-cited papers in the sub-field all cited?
- Are there 1-2 recent (last 18 months) citations, or does the paper read like a 2020 survey?
- Are the cited papers actually relevant, or are they name-dropped?
- For 丘成桐: does the paper cite at least one prior 丘成桐 winner in a similar vein, if such a paper exists?

Scoring bands:
- **90-95%** — Comprehensive, recent, accurate, every reference earns its citation.
- **75-89%** — Most key works cited, 1-2 noticeable gaps.
- **60-74%** — A reviewer would say "you missed X, Y, Z".
- **40-59%** — Citations are sparse or irrelevant.
- **20-39%** — Almost no citations.
- **0-19%** — No references section.

Common weaknesses:
- Citing only the original transformer paper in 2026.
- Citing a paper for a claim the paper doesn't make.
- No self-citation of the lab's own prior work (a real reviewer would notice this either way).

---

## Dimension 8 — 可复现性 (Reproducibility) — weight 5%

**Universal principle (across STEM)**: "看完这篇文章，读者能不能脑补出整个实验/方法流程和一些关键细节？"—按信息的完整度给分。**不要按单一领域（ML）的标准打分**。

What to look for — varies by sub-field, but the principle is the same: **enough information to reconstruct the procedure**.

**ML / AI / systems**:
- Code link / repository, or a clear statement of intent to release.
- Data public, or procedure to obtain it.
- Random seeds, hyperparameters, training compute specified.
- For LLM papers: model version, prompt template, decoding hyperparams stated.

**Theoretical math / theoretical CS**:
- Theorem statements are precise; assumptions listed.
- Proofs complete; key lemmas expanded (not just "by similar argument").
- Cited prior work accurate; standard facts (e.g., a well-known inequality) referenced rather than re-proved.
- Counterexamples (where applicable) explicit.

**Experimental physics / chemistry / biochemistry**:
- Apparatus / instrument model and configuration stated.
- Reagent / sample source and purity stated.
- Measurement protocol detailed enough to repeat (steps, conditions).
- Environmental conditions (temperature, pressure, humidity, etc.) stated.
- Calibration procedure specified.

**Algorithms / systems / applied CS**:
- Pseudocode or implementation detail for the core method.
- Compute environment (CPU/GPU, memory, OS, key library versions) stated.
- Input data / benchmark source + size stated.
- Baseline implementation source + configuration stated.

**Universal elements (any STEM)**:
- Key quantitative parameters (values, units, error bounds) present.
- Necessary controls / comparison groups present.
- Data / figures shown completely (not selectively cropped).
- Replication count / sample size stated.
- Limitations / failure cases acknowledged.

Scoring bands (universal):
- **90-95%** — All key artifacts public, all key parameters explicit, third party can fully reproduce.
- **75-89%** — Key artifacts accessible, key parameters explicit, third party can mostly reproduce.
- **60-74%** — Core steps present but missing some key details; third party can reproduce the main line but small details need guessing.
- **40-59%** — Important parameters missing; third party needs significant guessing.
- **20-39%** — Only headline result is verifiable; most of the procedure is missing.
- **0-19%** — Reproduction is impossible from the paper.

Common weaknesses:
- "Available on request" (a reviewer will read this as "no").
- "We use standard methods" (which standard? what configuration?).
- Closed model (GPT-4, Claude, etc.) used without disclosing version + date.
- Reporting accuracy / result on a private test set.
- Missing apparatus schematic, reagent source, or sample purity.
- Missing pseudocode for the core algorithm.
- Selective display of data (only successful runs, only best hyperparameters).

---

## Dimension 9 — 表达与图表 (Presentation & Figures) — weight 5%

What to look for (universal across STEM):
- **Figures**: legible axis labels with units, readable font size at print resolution, colorblind-friendly palettes, no decorative-only images.
- **Tables**: aligned, caption consistent (above or below), not duplicating figures.
- **Captions**: self-contained (a reader can understand the figure without reading the body).
- **Data integrity**: error bars / uncertainty shown when relevant, scale bars shown for microscopy / imaging, no sign of selective cropping or manipulation.
- **Color**: colorblind-friendly where it matters; not used to convey ordinal vs categorical confusions.

By sub-field:
- **Computational / data**: rainbow colormaps for ordinal data, double-y axes, truncated axes without flagging.
- **Experimental imaging**: scale bars, exposure consistency, no apparent image manipulation.
- **Schematics / diagrams**: clear labels, legend for symbols, not used to fill space.

Scoring bands:
- **90-95%** — Figures and tables each earn their space; captions are self-contained; data integrity preserved.
- **75-89%** — Mostly good, 1-2 figures that need rework.
- **60-74%** — Several figures that are decorative, unreadable, or missing uncertainty.
- **40-59%** — Figures mislead more than they inform.
- **20-39%** — Almost no usable figures.
- **0-19%** — No figures.

Common weaknesses:
- Bar / line charts without error bars / confidence intervals on results that have variance.
- Heatmap with a diverging colormap for non-diverging data, or vice versa.
- Truncated y-axis without flagging, exaggerating small effects.
- Figure 1 is the model architecture / apparatus diagram at a size where text inside is unreadable.
- No scale bar on microscopy / imaging figures.
- Apparent image manipulation (splicing, duplications) — flag for editorial review.

---

## Dimension 10 — 潜在价值 (Future Potential) — weight 10%

What to look for (Yau-specific):
- Does the paper open 2-3 concrete future directions, or is the conclusion a dead end?
- Could the method / data / insight be applied to another domain?
- Is the contribution generalizable, or only to the specific dataset / model studied?
- For 丘成桐: would the work be a credible basis for a follow-up paper at a real venue?

Scoring bands:
- **90-95%** — Multiple concrete future directions, each with a sentence on how.
- **75-89%** — One or two directions stated at a high level.
- **60-74%** — "Future work could explore..." with no specifics.
- **40-59%** — No future-work section; or future-work is a single sentence.
- **20-39%** — Conclusion is a sales pitch, not a forward look.
- **0-19%** — No future direction at all.

Common weaknesses:
- Future-work section is a single sentence: "We leave this for future work."
- Future directions are obvious (e.g., "apply to more datasets") without saying what would change.
- No discussion of limitations, which signals low future-thinking.
