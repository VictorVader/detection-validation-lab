import argparse
import os

from dvl.loader import load_dataset
from dvl.sigma_eval import load_rule, matches
from dvl.validate import load_case, evaluate_case
from dvl.metrics import summarize


def load_all_rules(folder="rules"):
    rules = []
    for name in os.listdir(folder):
        if name.endswith(".yml"):
            rules.append(load_rule(os.path.join(folder, name)))
    return rules


def cmd_run(args):
    rules = load_all_rules()
    for event in load_dataset(args.data):
        hit = False
        for rule in rules:
            if matches(event, rule):
                print("ALERT:", rule["title"], "-", event)
                hit = True
        if not hit:
            print("ok:   ", event)


def cmd_validate(args):
    results = []
    for name in os.listdir(args.cases):
        if name.endswith(".yml"):
            case = load_case(os.path.join(args.cases, name))
            results.append(evaluate_case(case))
    print(summarize(results))
    if not all(r["passed"] for r in results):
        exit(1)  # non-zero exit = CI fails if any rule is broken


def main():
    parser = argparse.ArgumentParser(prog="dvl")
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="run rules against telemetry")
    run_p.add_argument("--data", default="datasets/malicious")
    run_p.set_defaults(func=cmd_run)

    val_p = sub.add_parser("validate", help="run detection test cases")
    val_p.add_argument("--cases", default="tests/cases")
    val_p.set_defaults(func=cmd_validate)

    args = parser.parse_args()
    args.func(args)