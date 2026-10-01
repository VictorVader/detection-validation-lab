import yaml
from dvl.loader import load_dataset
from dvl.sigma_eval import load_rule, matches

def load_case(path):
    with open(path) as f:
        return yaml.safe_load(f)

def evaluate_case(case):
    rule = load_rule(case["rule"])

    tp = 0
    fn = 0
    false_negatives = []
    for dataset_path in case.get("should_alert", []):
        events = load_dataset(dataset_path)
        for e in events:
            if matches(e, rule):
                tp += 1
            else:
                fn += 1
                false_negatives.append(dataset_path)

    fp = 0
    tn = 0
    false_positives = []
    for dataset_path in case.get("should_not_alert", []):
        events = load_dataset(dataset_path)
        for e in events:
            if matches(e, rule):
                fp += 1
                false_positives.append(e)
            else:
                tn += 1

    return {
        "rule": case["rule"],
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "false_negatives": false_negatives,
        "false_positives": false_positives,
        "passed": not false_negatives and not false_positives,
    }