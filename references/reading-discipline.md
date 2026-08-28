# Reading Discipline — How to Read a Paper Without Decoding Corruption or Partial-Reading Bias

This file is the **input-handling discipline** for the paper-rubric-review skill. The reviewer-discipline file (`reviewer-discipline.md`) covers how to *score* rigorously. This file covers how to *read* the paper text rigorously — i.e., the input that the scoring will operate on. The two work together: bad reading → bad scoring, no matter how good the rubric.

The lessons here are extracted from the `pdf` and `docx` skills' operational rules, with adaptations for paper-review context.

## The two failure modes

When reading a paper as input to a review, two failure modes matter most:

1. **Decoding corruption** — the file-to-text conversion silently drops content (equations, figures, table structure, accents). The review then operates on a stripped-down text and either docks the paper for "missing" content that was actually there, or misses content that was actually missing.
2. **Partial-reading bias** — the LLM reads only the first 1-2 pages, or only the abstract, or only the sections that match keywords, and treats that fragment as the whole paper. The review then overweights intro rhetoric and underweights the body of evidence.

Both are easy to fall into, especially with long PDFs (50+ pages). Both produce reviews that feel "specific" (with quoted phrases) but are systematically off.

## Per-format rules

### `.pdf` papers

Three thresholds, all enforced together:

| Threshold | Rule |
|---|---|
| **≤ 20 pages** | Direct text extraction is fine. Use `pdftotext` or `pypdf`. Re-rasterize only the chart / table / formula pages for visual confirmation. |
| **> 20 pages AND user wants a specific datum (not the whole document)** | **Build a heading index first** (pypdf outline → printed TOC → keyword grep). Do NOT run `pdftotext` over every page and grep blindly. |
| **> 200 pages** | Always build the heading index up-front, even before the first grep. At this size 6-8 blind greps balloon into 30+ shell calls. |

**Charts, info-graphics, and complex financial / multi-level tables** (per `pdf` skill operational rule 3): MUST be read visually, **one page per call, never a range**. `pdfplumber` returns scrambled fragments on these layouts even when the PDF is text-native. Rasterize that single page to PNG and read the PNG directly. Critical for paper review because:
- Bar charts without error bars (Dim 9 weak)
- Heatmap with wrong colormap (Dim 9 weak)
- Architecture diagrams at unreadable text size (Dim 9 weak)
- t-SNE / UMAP projections (Dim 4 evidence)
- Confusion matrices, attention visualizations (Dim 4 evidence)

**Never suppress stderr** (`2>/dev/null`) in `pdftotext`, `pdfinfo`, or `pdfimages`. On failure, stderr is the only signal that explains why. If output is too noisy, redirect to a log file and grep on demand.

**PDF text extraction can scramble formula characters** (e.g., `v_center` becomes `v 푝표푙 푐`). When a formula seems garbled, **re-rasterize the page as PNG and read visually** — the human reader saw a proper formula; your text extractor didn't.

### `.docx` papers

`textutil -convert txt` (macOS) or `pandoc` can convert .docx to plain text, but:

- **Word equation objects flatten to nothing** (or to empty placeholders). A paper that has `v_center = 0 × V_policy + 0.7 × V_depth=1 + 0.3 × V_depth=2` as a Word equation will, in the extracted text, show as `v_center = ( )` or just `v_center` with empty parentheses.
- **Embedded images (figures) become filename references** or are lost entirely. The text may say "Figure 8: Macro-F1 heatmap" but the actual heatmap is gone.
- **Tables flatten to tab / space alignment** that loses visual structure. Multi-row headers, merged cells, footnotes all become indistinguishable.
- **Greek letters** may be replaced by placeholder names: α→"a", γ→"y", δ→"d" (so a paragraph saying "α, β and δ are the weights" with the formula using γ actually has a typo, but the text-side rendering makes it look like α, β, δ in both places).
- **Section numbering may be lost or scrambled** if the docx uses styles with custom numbering.

**When you suspect extraction loss** (formula looks missing, figure caption is there but no figure, table is just whitespace, Greek letter context seems off):
- (a) Do NOT dock for "missing derivation" / "missing figure" / etc. — the content may be in the docx as a non-text object.
- (b) Ask the user: "The formula `<X>` appears to be lost in text extraction — is it in the docx as an equation object? Can you paste it inline or share the page as image?"
- (c) If the user confirms the content is in the docx, retract any deduction that relied on its absence.
- (d) If the user cannot confirm, mark the dimension as "evidence unavailable due to extraction" rather than docking.

**For .docx input, default extraction tool on macOS**: `textutil -convert txt -output /tmp/out.txt /path/to/file.docx`. On Linux/Windows: `pandoc -f docx -t plain -o /tmp/out.txt /path/to/file.docx`. Do not try to use `python-docx` for full-text extraction — it works but is slower and gives the same lossy result.

### `.txt` or `.md` papers (already plain text)

Generally safe, but check for:
- **Timestamps in headers** that may have been inserted by a chat client and not be part of the paper.
- **Markdown artifacts** (`#`, `**`, code fences) — strip these before scoring if they appear in the text.
- **Truncation** — the text file may be a partial extract. Check the line count and look for "..." or `[truncated]` markers.

### `.pdf` with scan-only / image-only content (no text layer)

If `pdftotext` returns empty or only headers, the PDF is a scan. Use OCR (`tesseract`) or, preferred, rasterize all pages to PNG and read visually with the `Read` tool. This is slower but the only way to handle scan-only PDFs.

For paper review, scan-only PDFs are uncommon (papers are usually text-native), but it happens for old or arXiv-rejected re-formatted versions.

## Partial-reading discipline

The other failure mode is **reading the first 1-2 pages and calling it done**. The review then quotes intro rhetoric and never engages with the body of evidence. Counter-rules:

### The "cover-to-cover" rule

Before scoring, the LLM must read the **entire paper text once** in sequence. Not the abstract. Not just the intro and conclusion. The body sections (3-7 in most STEM papers) carry the actual evidence — figures, tables, equations, ablations. Skipping them is the most common cause of "specific-sounding but wrong" reviews.

For a 12-page paper, this means reading ~12 pages of text + visiting the figures / tables. For a 50-page paper, this means reading 50 pages of text. The cost is real but the alternative (partial-read review) is worse.

### The "do not let the abstract set the score" rule

The abstract is a sales pitch. The body is the substance. A paper that says "we achieve 91.63% accuracy" in the abstract may have a footnote in §3.3.4 saying "human inter-rater agreement is 92.1%, suggesting the LLM judge is replicating human labels, not real causality." A review that scores Dim 4 at 85% from the abstract alone, without reading §3.3.4, will miss this.

Discipline: for each dim, the cited quote should come from the **body** of the paper, not the abstract or introduction. Abstract quotes are acceptable only when the abstract itself contains a substantive claim (e.g., "we define progressive semantic drift").

### The "visit the figures and tables" rule

For Dim 4 (Evidence) and Dim 9 (Presentation), the figures and tables ARE the evidence. Reading the text-only description of "Figure 8 shows a heatmap" without seeing the heatmap is half a review. Use visual reading (rasterize + Read) for at least the key figures and tables.

Rule of thumb: any figure or table that the text explicitly references ("see Figure N", "as shown in Table N") MUST be visually inspected at least once during the review.

### The "last-section bias" rule

The most under-read section of a paper is often the **last substantive section before the conclusion** — e.g., §7 Limitations in the user's v2.1.0 paper, or the "Discussion" section in biomedical papers. These sections contain the authors' own self-criticism, which is the most valuable signal for a reviewer.

For paper review, the LLM should specifically:
- Find the Limitations / Discussion / Future Work section
- Read it carefully
- Use it to inform Dim 3 (Rigor) and Dim 10 (Potential) scoring — a paper that has good self-criticism is a different kind of strong than a paper that doesn't

## Anti-patterns to avoid

These are failure modes that have caused real retraction incidents in past reviews:

- **"I read the abstract and skimmed the intro"** → overweights intro rhetoric, misses experimental caveats. Solution: cover-to-cover.
- **"The text had no formula, so the paper has no derivation"** → extraction loss, not paper deficiency. Solution: ask user, do not dock.
- **"The figure was missing in the text extract"** → extraction loss, not paper deficiency. Solution: rasterize + visual, or ask user.
- **"The Greek letters are inconsistent between text and formula"** → text-side rendering issue, may not be a real paper bug. Solution: check before docking.
- **"The author claims X in the abstract but I can't find X in the body"** → could be:
  - (a) Author over-claimed (legitimate Dim 1 issue)
  - (b) The body uses different terminology and X is implicit (false positive)
  - (c) Extraction truncated the section where X is detailed
  - Solution: do not assume (a) — search for related terms, check the conclusion for restatements, ask user if still ambiguous.
- **"The reference list has 30 entries but most are old"** → possible Dim 7 weak, but also possible the field is mature and old references are appropriate. Solution: check field norms before docking.
- **"The methods section is short"** → possible Dim 3 weak, but also possible the paper has a long appendix with the full method. Solution: check the appendix before docking.

## Pre-flight check for input

Before reading a paper for review, run this checklist:

- [ ] File format identified (PDF / DOCX / TXT / MD).
- [ ] Page count estimated (for PDFs, run `pdfinfo` if available; for DOCX, use `textutil` then count).
- [ ] If > 20 pages: build a heading index first (outline / TOC / grep).
- [ ] If .docx: warn the user about possible extraction loss of equations / figures / tables; offer to use rasterized visual reading for those pages.
- [ ] If .pdf with charts/tables: identify which pages contain figures and tables; plan to read those visually.
- [ ] If multi-version: confirm which version is being reviewed.
- [ ] If scan-only PDF: plan to use OCR or full rasterization.

## Post-read check

After reading the paper, before scoring:

- [ ] Read every section, including the Limitations / Discussion / Future Work / Appendix.
- [ ] Visually inspected every figure / table explicitly referenced in the text.
- [ ] Verified the formula (if any) is actually in the paper (not in your imagination from prose).
- [ ] For .docx, asked the user about any "missing" formula / figure / table that extraction may have lost.
- [ ] Identified the paper version (v1, v2.1.0, v2.3.1, etc.) and any "draft" / "for-comment" / "submitted" notes.

## What this file does NOT cover

- **The scoring rubric itself** — see `rubric.md`.
- **The reviewer discipline** (cite quotes, no tier prediction, retract cleanly) — see `reviewer-discipline.md`.
- **The output format** — see `output-template.md`.
- **How to use the calibration data** — see `calibration-data/README.md`.

Reading discipline is the **input** layer. Reviewer discipline is the **judgment** layer. Scoring rubric is the **structure** layer. Calibration is the **reference** layer. All four are required.
