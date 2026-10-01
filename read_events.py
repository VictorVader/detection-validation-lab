import os
from dvl.loader import load_dataset
from dvl.sigma_eval import load_rule, matches

def load_all_rules(folder):
    rules = []
    for name in os.listdir(folder):
        if name.endswith(".yml"):
            rules.append(load_rule(os.path.join(folder, name)))
    return rules

rules = load_all_rules("rules")

def check_file(label, path):
    print(f"--- {label} ---")
    for event in load_dataset(path):
        hit = False
        for rule in rules:
            if matches(event, rule):
                print("ALERT:", rule["title"], "-", event)
                hit = True
        if not hit:
            print("ok:   ", event)

check_file("malicious", "datasets/malicious")
check_file("benign", "datasets/benign")