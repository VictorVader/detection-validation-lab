# Command-line entrypoint: python -m dvl <run|validate|report|respond>

import argparse
import os

from dvl.loader import load_dataset
from dvl.sigma_eval import load_rule, matches
from dvl.validate import load_case, evaluate_case
from dvl.metrics import summarize
from dvl.navigator import write_layer
from dvl.respond import build_case, write_case


def load_all_rules(folder="rules"):
    # Load every rule YAML file in a folder
    rules = []
    for name in os.listdir(folder):
        if name.endswith(".yml"):
            rules.append(load_rule(os.path.join(folder, name)))
    return rules


def cmd_run(args):
    # Fire every rule at a dataset and print alerts/ok lines
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
    # Run every test case, print a pass/fail summary, exit nonzero on failure
    results = []
    for name in os.listdir(args.cases):
        if name.endswith(".yml"):
            case = load_case(os.path.join(args.cases, name))
            results.append(evaluate_case(case))
    print(summarize(results))
    if not all(r["passed"] for r in results):
        exit(1)  # non-zero exit = CI fails if any rule is broken


def cmd_report(args):
    # Write the ATT&CK Navigator layer from current test case results
    results = []
    for name in os.listdir(args.cases):
        if name.endswith(".yml"):
            case = load_case(os.path.join(args.cases, name))
            results.append(evaluate_case(case))
    write_layer(results)
    print("wrote reports/navigator_layer.json")


def cmd_respond(args):
    # Fire rules at a dataset and write a case file for each alert
    rules = load_all_rules()
    for event in load_dataset(args.data):
        for rule in rules:
            if matches(event, rule):
                case = build_case(rule, event)
                path = write_case(case)
                print("wrote", path)


def main():
    parser = argparse.ArgumentParser(prog="dvl")
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="run rules against telemetry")
    run_p.add_argument("--data", default="datasets/malicious")
    run_p.set_defaults(func=cmd_run)

    val_p = sub.add_parser("validate", help="run detection test cases")
    val_p.add_argument("--cases", default="tests/cases")
    val_p.set_defaults(func=cmd_validate)

    rep_p = sub.add_parser("report", help="write ATT&CK Navigator layer")
    rep_p.add_argument("--cases", default="tests/cases")
    rep_p.set_defaults(func=cmd_report)

    res_p = sub.add_parser("respond", help="turn alerts into case files")
    res_p.add_argument("--data", default="datasets/malicious")
    res_p.set_defaults(func=cmd_respond)

    args = parser.parse_args()
    args.func(args)