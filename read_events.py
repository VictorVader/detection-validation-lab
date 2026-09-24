import json
import yaml

with open("rules/encoded_powershell.yml") as f:
    rule = yaml.safe_load(f)

def matches(event, rule):
    d = rule["detection"]
    if d["process_contains"] not in event["process"]:
        return False
    if d["command_contains"] not in event["command"]:
        return False
    return True

with open("data/events.jsonl") as f:
    for line in f:
        event = json.loads(line)
        if matches(event, rule):
            print("ALERT:", rule["title"], "-", event)
        else:
            print("ok:   ", event)