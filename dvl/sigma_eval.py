import yaml

def load_rule(path):
    with open(path) as f:
        return yaml.safe_load(f)

def matches(event, rule):
    d = rule["detection"]
    if d["process_contains"] not in event["process"]:
        return False
    if d["command_contains"] not in event["command"]:
        return False
    return True