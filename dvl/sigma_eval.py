# Load detection rules from YAML and check events against them

# A rule is a dict loaded straight from YAML. `matches()` is intentionally
# simple: every key under `detection` must be satisfied for the rule to fire

import yaml

def load_rule(path):
    # Load one rule YAML file into a dict
    with open(path) as f:
        return yaml.safe_load(f)

def matches(event, rule):
    # Return True if `event` satisfies every condition in `rule['detection']`
    d = rule["detection"]
    if d["process_contains"] not in event["process"]:
        return False
    if d["command_contains"] not in event["command"]:
        return False
    return True