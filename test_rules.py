from dvl.loader import load_dataset
from dvl.sigma_eval import load_rule, matches

def test_encoded_powershell_detects_attack():
    rule = load_rule("rules/encoded_powershell.yml")
    events = load_dataset("datasets/malicious/T1059.001_encoded_powershell.jsonl")
    alerts = [e for e in events if matches(e, rule)]
    assert len(alerts) == 1

def test_encoded_powershell_ignores_benign():
    rule = load_rule("rules/encoded_powershell.yml")
    events = load_dataset("datasets/benign")
    alerts = [e for e in events if matches(e, rule)]
    assert len(alerts) == 0

def test_lsass_dump_detects_attack():
    rule = load_rule("rules/lsass_dump.yml")
    events = load_dataset("datasets/malicious/T1003.001_lsass_dump.jsonl")
    alerts = [e for e in events if matches(e, rule)]
    assert len(alerts) == 1

def test_lsass_dump_ignores_benign():
    rule = load_rule("rules/lsass_dump.yml")
    events = load_dataset("datasets/benign")
    alerts = [e for e in events if matches(e, rule)]
    assert len(alerts) == 0