# Load Sigma-style detection rules from YAML and check events against them

# Supports a small subset of real Sigma syntax:
#   - a `selection` block: dict of `Field|modifier: value` pairs, ANDed together
#   - modifiers: contains, startswith, endswith (case-insensitive); no modifier = exact
#   - condition: "selection", "selection and not filter", or "selection and filter"

import yaml

def load_rule(path):
    # Load one rule YAML file into a dict
    with open(path) as f:
        return yaml.safe_load(f)

def get_technique(rule):
    # Pull the ATT&CK technique ID out of tags: [attack.t1059.001, ...]
    for tag in rule.get("tags", []):
        if tag.lower().startswith("attack.t"):
            return tag.split(".", 1)[1].upper()
    return None


def _match_value(event_value, pattern, modifier):
    # Compare one event field to one pattern, case-insensitively

    # The modifier (contains/startswith/endswith) picks the comparison
    # No modifier means exact match. A missing field never matches
    
    if event_value is None:
        return False
    text = str(event_value).lower()
    pat = str(pattern).lower()
    if modifier == "contains":
        return pat in text
    if modifier == "startswith":
        return text.startswith(pat)
    if modifier == "endswith":
        return text.endswith(pat)
    return text == pat


def _match_selection(event, selection):
    # Return True if every `Field|modifier: value` pair in a selection matches.
    # Pairs are ANDed: one failed field fails the whole selection.

    for key, pattern in selection.items():
        field, _, modifier = key.partition("|")
        if not _match_value(event.get(field), pattern, modifier or None):
            return False
    return True


def _eval_condition(condition, results):
    # Combine selection results according to the rule's `condition` string.

    # `results` maps selection names to True/False. Only handles `x`,
    # `x and y`, and `x and not y` (the documented subset).

    condition = condition.strip()
    if " and not " in condition:
        left, right = condition.split(" and not ")
        return results[left.strip()] and not results[right.strip()]
    if " and " in condition:
        left, right = condition.split(" and ")
        return results[left.strip()] and results[right.strip()]
    return results[condition]


def matches(event, rule):
    # Return True if `event` satisfies the rule's detection condition
    
    detection = rule["detection"]
    results = {
        name: _match_selection(event, block)
        for name, block in detection.items()
        if name != "condition"
    }
    return _eval_condition(detection["condition"], results)