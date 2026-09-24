from detect import load_rule, load_events, matches

def test_encoded_powershell_detects_attack():
    rule = load_rule("rules/encoded_powershell.yml")
    events = load_events("data/events.jsonl")
    alerts = [e for e in events if matches(e, rule)]
    assert len(alerts) == 1
    assert "-enc" in alerts[0]["command"]

def test_encoded_powershell_ignores_benign():
    rule = load_rule("rules/encoded_powershell.yml")
    events = load_events("data/benign_events.jsonl")
    alerts = [e for e in events if matches(e, rule)]
    assert len(alerts) == 0