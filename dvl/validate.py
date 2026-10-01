import yaml
from dvl.loader import load_dataset
from dvl.sigma_eval import load_rule, matches

def load_case(path):
    with open(path) as f:
        return yaml.safe_load(f)

def evaluate_case(case):
    rule = load_rule(case["rule"])

    false_negatives = []
    for dataset_path in case.get("should_alert", []):
        events = load_dataset(dataset_path)
        if not any(matches(e, rule) for e in events):
            false_negatives.append(dataset_path)

    false_positives = []
    for dataset_path in case.get("should_not_alert", []):
        events = load_dataset(dataset_path)
        false_positives.extend(e for e in events if matches(e, rule))

    return {
        "rule": case["rule"],
        "false_negatives": false_negatives,
        "false_positives": false_positives,
        "passed": not false_negatives and not false_positives,
    }