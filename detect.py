import json
import yaml

def load_rule(path):
    with open(path) as f:
        return yaml.safe_load(f)

def load_events(path):
    events = []
    with open(path) as f:
        for line in f:
            events.append(json.loads(line))
    return events

def matches(event, rule):
    d = rule["detection"]
    if d["process_contains"] not in event["process"]:
        return False
    if d["command_contains"] not in event["command"]:
        return False
    return True