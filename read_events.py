import json

with open("data/events.jsonl") as f:
    for line in f:
        event = json.loads(line)
        print(event)