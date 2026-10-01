# Load telemetry events from JSONL files or folders of JSONL files

import json
import os

def load_events(path):
    # Read one .jsonl file into a list of event dicts, one dict per line
    events = []
    with open(path) as f:
        for line in f:
            events.append(json.loads(line))
    return events

def load_dataset(path):
    # Load a single .jsonl file, or every .jsonl file in a directory.

    # This is the one place that knows what "telemetry" looks like on disk.
    # Everything downstream just works with plain dicts.
    
    if os.path.isdir(path):
        events = []
        for name in os.listdir(path):
            if name.endswith(".jsonl"):
                events.extend(load_events(os.path.join(path, name)))
        return events
    return load_events(path)