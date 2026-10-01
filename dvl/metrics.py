def precision(tp, fp):
    return tp / (tp + fp) if (tp + fp) else 0.0

def recall(tp, fn):
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