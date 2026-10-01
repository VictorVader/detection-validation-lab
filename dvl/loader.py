import json
import os

def load_events(path):
    events = []
    with open(path) as f:
        for line in f:
            events.append(json.loads(line))
    return events

def load_dataset(path):
    """Load one .jsonl file, or every .jsonl file in a directory."""
    if os.path.isdir(path):
        events = []
        for name in os.listdir(path):
            if name.endswith(".jsonl"):
                events.extend(load_events(os.path.join(path, name)))
        return events
    return load_events(path)