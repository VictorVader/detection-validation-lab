import os
from detect import load_rule, load_events, matches

def load_all_rules(folder):
    rules = []
    for name in os.listdir(folder):
        if name.endswith(".yml"):
            rules.append(load_rule(os.path.join(folder, name)))
    return rules

rules = load_all_rules("rules")

def check_file(path):
    print(f"--- {path} ---")
    for event in load_events(path):
        hit = False
        for rule in rules:
            if matches(event, rule):
                print("ALERT:", rule["title"], "-", event)
                hit = True
        if not hit:
            print("ok:   ", event)

check_file("data/events.jsonl")
check_file("data/benign_events.jsonl")