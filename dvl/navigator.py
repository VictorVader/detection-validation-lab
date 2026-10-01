# Export rule results as an ATT&CK Navigator layer (a heatmap JSON file)

# Upload the output at https://mitre-attack.github.io/attack-navigator/
# to see which techniques are covered by passing rules

import json
from dvl.sigma_eval import load_rule

def build_layer(results, name="Detection Validation Lab"):
    # Build the Navigator layer dict: one scored entry per rule's technique
    # Score 100 (green) = rule's test case passes. Score 50 (amber) = it doesn't

    techniques = []
    for r in results:
        rule = load_rule(r["rule"])
        technique_id = rule["technique"]
        score = 100 if r["passed"] else 50  # green if tests pass, else amber
        techniques.append({
            "techniqueID": technique_id,
            "score": score,
            "comment": f"rule: {r['rule']}",
        })

    return {
        "name": name,
        "versions": {"attack": "19", "navigator": "4.9.0", "layer": "4.5"},
        "domain": "enterprise-attack",
        "description": "Techniques covered by validated Sigma rules",
        "gradient": {
            "colors": ["#f8b0b0", "#8ec843"],
            "minValue": 0,
            "maxValue": 100,
        },
        "techniques": techniques,
    }

def write_layer(results, path="reports/navigator_layer.json"):
    # Write the Navigator layer to disk, creating reports/ if needed
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(build_layer(results), f, indent=2)