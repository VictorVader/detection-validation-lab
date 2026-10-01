import json

def load_events(path):
    events = []
    with open(path) as f:
        for line in f:
            events.append(json.loads(line))
    return events