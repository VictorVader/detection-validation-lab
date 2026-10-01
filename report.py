import os
from dvl.validate import load_case, evaluate_case
from dvl.metrics import summarize

CASE_DIR = "tests/cases"
results = []
for name in os.listdir(CASE_DIR):
    if name.endswith(".yml"):
        case = load_case(os.path.join(CASE_DIR, name))
        results.append(evaluate_case(case))

print(summarize(results))