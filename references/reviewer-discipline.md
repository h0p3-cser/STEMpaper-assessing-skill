# Reviewer Discipline — How to Do a Rigorous Paper Review

This file is the **meta-workflow** for the paper-rubric-review skill. The rubric (`rubric.md`) defines *what* to score; this file defines *how* to do the scoring rigorously. Every hard rule in this file is grounded in a real mistake the skill author made during a multi-version paper review and had to retract.

## Why this file exists

The author of this skill (Mavis) once ran paper-rubric-review on a v2.1.0 paper draft, and produced a review that:
- flagged two DeepSeek model names (V4 Pro / V4 Flash) as a typo — wrong, both are real models released 2026-04
- claimed 2.2M parameter derivation was missing — wrong, it was at line 397 in a formula image that textutil did not extract
- claimed §6.1 Case Study was empty — wrong, it was an intentional reminder placeholder
- claimed "haven't been tested by any other research in the world" was in §8 — wrong, that phrase was in v3 (原始版本) but had been deleted in v2.1.0
- heavily penalized no GitHub repo — wrong calibration, this was a draft review

That review docked 4+ points on errors. The user caught every one. The lessons from those mistakes are encoded below.

## Hard rules (in priority order)

### 1. Verify before deducting — `grep` for every quote, every claim

Before any score < 90% on a dim, before any sentence-level criticism, **grep the actual paper text** for the phrase you are about to cite. Format every deduction as:

> **Dim N — M%**: "exact quoted phrase" (line 412 of `paper.txt`)

If you cannot produce a line number + exact quote, your deduction is not grounded. Either:
- (a) drop the score by one band (e.g., 60% → 50%) and mark the justification as "(no on-point quote found, see 'Weaknesses')"
- (b) re-read the paper more carefully and find the quote
- (c) drop the criticism entirely

Never paraphrase the abstract as if it were evidence. Never cite a phrase from a different version of the paper. Never claim something is missing without first grep'ing for it.

### 2. Multi-version strict rules

When reviewing a paper that has multiple versions (e.g., v3, v2.1.0, v2.3.1, v2.2.6), the default is that the **latest version is what is being reviewed**. Older versions are background context only.

- Do not carry forward criticisms from an older version to a newer one without re-grepping in the newer version.
- When the user asks about a specific version (e.g., "v2.1.0 帮我打个分"), score that version only.
- When comparing versions, format as: "v3 had `<phrase>` but v2.1.0 deleted it" — never "v2.1.0 has `<phrase>`" if the phrase is actually from v3.
- If a quote appears in the user's working file but not in the latest, flag this as "the user may have already fixed this" rather than re-docking the score.

This rule was learned the hard way: in a review of v2.1.0, the author claimed "haven't been tested" was at §8. It was not. It had been in v3 原始版本 but the user had deleted it in v2.1.0. The author docked the score on a non-existent error.

### 3. Verify unknown model / API / framework / benchmark names via `web_search`

Before claiming a model name is a typo, a placeholder, or a fabrication, **web search** the name. Models and APIs evolve quickly; the author's training cutoff is unlikely to cover them.

- Models that require verification (as of 2026-08): DeepSeek V4 series (V4-Pro, V4-Flash, V4-Flash-0731), GPT-5.x, Claude 4.x, Gemini 2.5/3.x, Qwen 3, Llama 4, Kimi K2/K3, GLM-4/5.
- API names that may have changed: openai `deepseek-chat` may be deprecated → `deepseek-v4-flash`; old Anthropic model ids may be removed.
- Benchmarks that may have updated: MMLU, MMLU-Pro, LongBench, HumanEval, LiveCodeBench, SWE-bench, FrontierMath.

Format: `"DeepSeek V4 Pro (Preview)" — verified via web_search 2026-08, real model released 2026-04 (1.6T total / 49B activated / 1M context).`

If the model genuinely does not exist in any search result, then the criticism is valid: "Model name `<X>` not found in DeepSeek / OpenAI / Anthropic / Google public model catalogs as of `<date>`. Please verify spelling or specify if this is an internal/private model."

This rule was learned the hard way: the author flagged "Deepseek V4 Pro" and "Deepseek V4 Flash" as a typo pair. Both are real models. The user pushed back; web search confirmed the V4 series.

### 4. Draft review calibration

When the user says "this is a draft" or "I'll add that at final review", do not penalize for normal draft limitations. Specifically:

- **No code / data / GitHub link in draft**: do not deduct heavily from "Reproducibility" dim. The promise "code and data will be released upon publication" is a reasonable draft statement. Mark as "deferred to final submission" rather than docking.
- **No exact BGE / model version id**: do not deduct heavily. The user is aware. Mark as "specify at final" rather than docking.
- **Empty section headers as placeholders** (e.g., `§6.1 Case Study` with no content): do not dock for "incomplete structure". Check with the user first; the placeholder may be intentional ("I'll fill this in after the experiments are done").
- **Typos in draft that the user has flagged as "I'll fix this"**: do not re-dock. Just note them as known issues.

The Reproducibility dim (Dim 8) should be calibrated for **draft** state by default: 35-50% is reasonable for a draft; 70%+ is reasonable for a final submission with full artifacts. Adjust the calibration band based on what the user has told you about submission state.

This rule was learned the hard way: the author docked -10 on Dim 8 for missing GitHub link during a draft review; the user pointed out that the repo would be created at final submission. -10 was unfair.

### 5. Textutil / docx-extraction caveats

When reviewing a paper provided as `.docx`, the conversion to plain text via `textutil -convert txt` (or similar) may lose information:

- **Math formulas** rendered as LaTeX in the docx may be replaced by empty space or `()` placeholders in the text. The actual equation (e.g., `v_center = 0 × V_policy + 0.7 × V_depth=1 + 0.3 × V_depth=2`) is in the docx as a Word equation object, but textutil flattens it.
- **Greek letters** may be replaced by placeholder names: "α" becomes "a", "γ" becomes "y", "δ" becomes "d" (which is why the user might write "δ should be γ" — actually the formula uses γ, the text uses δ by mistake).
- **Figures** may be referenced as "Figure N" with the actual image lost.
- **Tables** may be flattened to plain text with tab/space alignment that loses the visual structure.

When a formula, figure, or table is referenced in the text but appears missing or garbled in the extracted text:
- (a) Do not dock for "missing derivation" if the math may be in a Word equation object.
- (b) Ask the user: "The formula `<X>` appears to be lost in text extraction — is it in the docx as an equation object?"
- (c) If the user confirms the math is in the docx, retract the criticism and dock only for **text-level typos** (e.g., "δ" vs "γ" inconsistency in the explanatory paragraph).

This rule was learned the hard way: the author docked "2.2M parameters not derived" — the derivation was at line 397 in a Word equation. textutil had flattened it.

### 6. Strict scoring discipline

When the user explicitly says "give me a strict score" or "所有的评分往严格来给":

- Apply the lower band of each scoring range, not the upper.
- For every dim, find 1-2 real flaws (do not invent flaws; if you cannot find any, the dim is genuinely strong and the score should reflect that).
- For each flaw, anchor to a quote + line number.
- For each dim, compute the delta vs the previous version explicitly. Show the user exactly which improvements earned points and which new errors lost points.
- Do not soften with phrases like "modest improvement" or "reasonable growth"; the user asked for strict, give strict.
- Cap top dim at 95%, never 100%.

But: strict does not mean unfair. If a quote does not exist in the current version, the deduction is invalid — retract it. If the user defers an issue to final review, do not penalize. Strict is honest, not punitive.

### 7. When the user pushes back, retract cleanly

If the user corrects you with verifiable evidence (a file, a grep, a line number, a web search result), retract the original criticism fully and update the score. Do not defend the original criticism. Do not split the difference. Do not say "well, it's still partially valid". Either it is grounded in the text or it is not.

When retracting, be explicit:
- "I retract the `<X>` criticism. `<Y>` is in fact at line N. Score adjusts from A to B."

This applies to both:
- The user (when they correct a wrong claim)
- The author (when they re-read the paper and realize they made an error)

## Pre-flight checklist before submitting a review

Before delivering any paper review, run this checklist:

- [ ] Identified the exact version of the paper being reviewed (v1, v2.1.0, v2.3.1, etc.)
- [ ] Asked the user about submission state (draft / final / for-arxiv / for-venue) to calibrate Dim 8
- [ ] Asked the user about venue target (Yau, NeurIPS, ACL, etc.) to calibrate tier-mapping commentary — but remember the skill does NOT predict tier
- [ ] Verified any model / API / framework names that look unfamiliar via web_search
- [ ] For every dim score < 90%, written a 1-line quote + line number as justification
- [ ] For every weakness, written a concrete fix (not "improve writing")
- [ ] Re-grepped the paper for any "famous error" quotes I planned to cite (e.g., "For my apology") to confirm they are still in the current version
- [ ] Computed the weighted sum exactly, shown 1 decimal place
- [ ] Computed the 3 macro scores via normalized weighted average
- [ ] If user asked for radar chart, run `scripts/radar-chart.js` and reference the SVG
- [ ] If user asked for strict scoring, applied lower bands and showed explicit deltas vs previous version
- [ ] Output does NOT include any Yau tier / venue tier / percentile claims

## What the skill explicitly does NOT do

This skill is a self-reflection tool, not a venue predictor. The author has no calibration data linking scores to actual Yau / NeurIPS / ICML / ACL / CCF committee decisions. Stating the rubric's score does not predict acceptance.

- No "this would get silver" claims.
- No "top 20% of NeurIPS submissions" claims.
- No "calibrated against past winners" claims.
- No invented sub-tier labels (e.g., 候选 / 稳健 / 强 / 金边缘 / 金 are rubric-defined; anything else is fabricated).

If the user asks for a prediction, refuse and explain. The honest answer is "I have no calibration data; get mentor feedback or sample reviewer feedback instead."
