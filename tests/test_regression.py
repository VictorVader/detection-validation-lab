# Regression suite: run every YAML test case in tests/cases/ through pytest

# If a rule edit reintroduces a false positive or false negative that was
# already fixed, this fails instead of relying on someone noticing

import os
import pytest
from dvl.validate import load_case, evaluate_case

CASE_DIR = "tests/cases"
case_files = [f for f in os.listdir(CASE_DIR) if f.endswith(".yml")]

@pytest.mark.parametrize("case_file", case_files)
def test_rule_case(case_file):
    case = load_case(os.path.join(CASE_DIR, case_file))
    result = evaluate_case(case)
    assert result["passed"], result