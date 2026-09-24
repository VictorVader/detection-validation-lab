import json

def is_encoded_powershell(event):
    return "powershell" in event["process"] and "-enc" in event["command"]

with open("data/events.jsonl") as f:
    for line in f:
        event = json.loads(line)
        if is_encoded_powershell(event):
            print("ALERT:", event)
        else:
            print("ok:   ", event)