from detect import load_rule, load_events, matches

rule = load_rule("rules/encoded_powershell.yml")

def check_file(path):
    print(f"--- {path} ---")
    for event in load_events(path):
        if matches(event, rule):
            print("ALERT:", rule["title"], "-", event)
        else:
            print("ok:   ", event)

check_file("data/events.jsonl")
check_file("data/benign_events.jsonl")