#!/usr/bin/env python3
"""
compare-calibration.py — Compare a scored paper against an empirical reference level.

Usage:
  python3 compare-calibration.py --level ysa10-stem --scores "62,68,55,60,72,80,50,40,70,75" --macros "62,65,72"
  python3 compare-calibration.py --level ysa10-stem --from-json <path_to_paper_review_json>

Output: a markdown table showing the user's score vs the reference level's
distribution (min, q1, median, q3, max, percentile rank), with an honest
disclaimer.

This script does NOT predict acceptance. It is an empirical comparison.
"""
import argparse
import json
import os
import sys
from pathlib import Path

CALIBRATION_DIR = Path(__file__).parent.parent / "references" / "calibration-data"

DIM_KEYS = [
    ("D1", "problem_originality", "选题创新性"),
    ("D2", "method_originality", "方法原创性"),
    ("D3", "method_rigor", "方法严谨性"),
    ("D4", "experimental_validation", "实验验证"),
    ("D5", "writing_quality", "写作规范性"),
    ("D6", "structure_logic", "结构与逻辑"),
    ("D7", "literature_coverage", "文献覆盖"),
    ("D8", "reproducibility", "可复现性"),
    ("D9", "presentation_figures", "表达与图表"),
    ("D10", "future_potential", "潜在价值"),
]

MACRO_KEYS = [
    ("R", "research", "研究本身"),
    ("P", "paper", "论文本身"),
    ("Pot", "potential", "课题潜力"),
]


def load_level(level_id: str) -> dict:
    """Load a calibration level JSON by id (e.g., 'ysa10-stem')."""
    # Read registry
    with open(CALIBRATION_DIR / "levels.json") as f:
        registry = json.load(f)
    level_meta = next((l for l in registry["levels"] if l["level_id"] == level_id), None)
    if not level_meta:
        raise ValueError(f"Level '{level_id}' not in registry. Available: {[l['level_id'] for l in registry['levels']]}")
    with open(CALIBRATION_DIR / level_meta["data_file"]) as f:
        return json.load(f)


def percentile_rank(value: float, all_values: list) -> float:
    """Compute approximate percentile rank of `value` within `all_values`."""
    all_values = sorted(all_values)
    n = len(all_values)
    below = sum(1 for v in all_values if v < value)
    equal = sum(1 for v in all_values if v == value)
    return round(100 * (below + 0.5 * equal) / n, 1)


def compare(level_data: dict, user_scores: dict) -> str:
    """Build a markdown comparison table."""
    lines = []
    metrics = level_data["metrics"]

    lines.append(f"# Empirical Reference Comparison")
    lines.append("")
    lines.append(f"**Reference level:** {level_data['level_name_zh']}")
    lines.append(f"**Reference (EN):** {level_data['level_name']}")
    lines.append(f"**Source:** {level_data['venue']['url']}")
    lines.append(f"**n_papers in level:** {level_data['data_provenance']['n_papers']}")
    lines.append(f"**Noise floor:** {level_data['data_provenance']['noise_floor']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Per-dimension table
    lines.append("## Per-dimension comparison")
    lines.append("")
    lines.append("| # | Dim | You | Min | Q1 | Median | Q3 | Max | Percentile |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")

    for code, key, label in DIM_KEYS:
        idx = next(i for i, (c, k, _) in enumerate(DIM_KEYS) if k == key) + 1
        m = metrics[f"dim_{idx}_{key}"]
        v = user_scores["dims"].get(key, "—")
        all_papers = level_data.get("papers_in_dataset", [])
        if all_papers:
            dim_key_in_papers = f"dim_{idx}"
            dist = [p[dim_key_in_papers] for p in all_papers]
            pct = percentile_rank(v, dist) if v != "—" else "—"
        else:
            pct = "—"
        lines.append(f"| {code[1:]} | {label} | {v} | {m['min']} | {m['q1']} | {m['median']} | {m['q3']} | {m['max']} | {pct} |")

    lines.append("")

    # Macro table
    lines.append("## Macro comparison")
    lines.append("")
    lines.append("| Macro | You | Min | Q1 | Median | Q3 | Max | Percentile |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for code, key, label in MACRO_KEYS:
        m = metrics[f"macro_{key}"]
        v = user_scores["macros"].get(key, "—")
        all_papers = level_data.get("papers_in_dataset", [])
        if all_papers:
            dist = [p[f"macro_{key}"] for p in all_papers]
            pct = percentile_rank(v, dist) if v != "—" else "—"
        else:
            pct = "—"
        lines.append(f"| {label} | {v} | {m['min']} | {m['q1']} | {m['median']} | {m['q3']} | {m['max']} | {pct} |")

    lines.append("")

    # Total
    t = metrics["total"]
    user_total = user_scores.get("total", "—")
    all_papers = level_data.get("papers_in_dataset", [])
    if all_papers:
        dist = [p["total"] for p in all_papers]
        pct = percentile_rank(user_total, dist) if user_total != "—" else "—"
    else:
        pct = "—"

    lines.append("## Total")
    lines.append("")
    lines.append(f"- **Your total:** {user_total}")
    lines.append(f"- **Reference range:** [{t['min']}, {t['max']}] | Q1-Q3: [{t['q1']}, {t['q3']}] | Median: {t['median']} | Mean: {t['mean']} | σ: {t['std']}")
    lines.append(f"- **Your percentile within this level:** {pct}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Honest interpretation
    lines.append("## Honest interpretation")
    lines.append("")
    lines.append(level_data.get("honest_disclaimer", "This is an LLM heuristic self-assessment with ~±8 point noise. NOT a venue verdict."))
    lines.append("")
    lines.append("**What this comparison tells you:**")
    lines.append(f"- Your paper's {user_total} falls {'within' if isinstance(user_total,(int,float)) and t['min'] <= user_total <= t['max'] else 'outside'} the observed range of {level_data['data_provenance']['n_papers']} accepted papers in this volume (range [{t['min']}, {t['max']}]).")
    lines.append(f"- With ~±8 noise on both sides, the comparison is ±~8 in either direction.")
    lines.append(f"- Being 'within the IQR' is consistent with — not sufficient for — acceptance. The IQR shows where the middle 50% of accepted papers fell on LLM self-scoring, not a threshold.")
    lines.append("")

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--level", required=True, help="Level id, e.g. ysa10-stem")
    p.add_argument("--scores", help='Comma-separated dim scores, e.g. "62,68,55,60,72,80,50,40,70,75"')
    p.add_argument("--macros", help='Comma-separated macros R,P,Pot, e.g. "62,65,72"')
    p.add_argument("--from-json", help="Path to a paper-rubric-review JSON output")
    args = p.parse_args()

    level_data = load_level(args.level)

    if args.from_json:
        with open(args.from_json) as f:
            user_data = json.load(f)
        # Try to extract scores from various JSON shapes
        # Case 1: our combined.json shape
        if "papers" in user_data:
            paper = user_data["papers"][0]
            dim_keys_eng = ["problem_originality","method_originality","method_rigor",
                            "experimental_validation","writing_quality","structure_logic",
                            "literature_coverage","reproducibility","presentation_figures","future_potential"]
            user_scores = {
                "dims": {k: paper["dims"][k] for k in dim_keys_eng},
                "macros": paper["macro"],
                "total": paper["total"]
            }
        else:
            user_scores = user_data
    elif args.scores and args.macros:
        dim_keys_eng = [k for _, k, _ in DIM_KEYS]
        scores = [float(s) for s in args.scores.split(",")]
        macros_list = [float(s) for s in args.macros.split(",")]
        user_scores = {
            "dims": dict(zip(dim_keys_eng, scores)),
            "macros": dict(zip(["research", "paper", "potential"], macros_list)),
            "total": sum(scores[i] * [0.20, 0.15, 0.10, 0.15, 0.10, 0.05, 0.05, 0.05, 0.05, 0.10][i] for i in range(10))
        }
    else:
        print("Provide either --scores+--macros or --from-json", file=sys.stderr)
        sys.exit(1)

    print(compare(level_data, user_scores))


if __name__ == "__main__":
    main()
