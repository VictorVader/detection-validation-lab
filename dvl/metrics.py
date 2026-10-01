# Turn evaluate_case() results into precision/recall and a readable summary

def precision(tp, fp):
    """Of everything flagged, what fraction was actually an attack?"""
    return tp / (tp + fp) if (tp + fp) else 0.0

def recall(tp, fn):
    """Of all real attacks, what fraction did the rule catch?"""
    return tp / (tp + fn) if (tp + fn) else 0.0

def summarize(results):
    """results: list of evaluate_case() dicts"""
    lines = []
    for r in results:
        p = precision(r["tp"], r["fp"])
        rec = recall(r["tp"], r["fn"])
        status = "PASS" if r["passed"] else "FAIL"
        lines.append(
            f"[{status}] {r['rule']:<35} "
            f"TP={r['tp']} FP={r['fp']} FN={r['fn']} "
            f"precision={p:.2f} recall={rec:.2f}"
        )
    return "\n".join(lines)