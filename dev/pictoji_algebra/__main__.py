"""CLI:  python -m pictoji_algebra check pictoji-test-algebra.md

Exit code is nonzero when a canary trips or an assertion fails, so this can be a
CI gate - unlike the existing workflow, which runs its analysis with `|| true`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .engine import Budget, normalize, prove
from .spec import bisect_report, check, load, render
from .terms import parse


def build_parser():
    p = argparse.ArgumentParser(
        prog="pictoji_algebra",
        description="Check the Pictoji algebra for consistency on its own test cases.")
    p.add_argument("command", choices=["check", "rules", "normalize", "prove"])
    p.add_argument("args", nargs="*", help="spec file, or expressions")
    p.add_argument("--spec", default="pictoji-test-algebra.md")
    p.add_argument("--disable", action="append", default=[], metavar="SEL")
    p.add_argument("--enable-only", action="append", default=[], metavar="SEL")
    p.add_argument("--bisect", action="store_true",
                   help="delta-debug each tripped canary to a minimal axiom set")
    p.add_argument("--no-confluence", action="store_true")
    p.add_argument("--verbose", "-v", action="store_true")
    p.add_argument("--max-depth", type=int, default=6)
    p.add_argument("--max-nodes", type=int, default=4000)
    p.add_argument("--max-size", type=int, default=60)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    path = Path(args.args[0]) if args.args and args.command == "check" else Path(args.spec)
    if not path.exists():
        sys.stderr.write("error: spec file not found: %s\n" % path)
        return 2

    spec = load(path)
    rules = spec.rules
    selectors = list(args.disable) + list(args.enable_only)
    unresolved = rules.unresolved(selectors)
    if unresolved:
        # A typo'd selector silently selecting nothing would quietly change what
        # was tested - the last thing a bisection tool should do.
        sys.stderr.write("error: selectors match no rule: %s\n" % ", ".join(unresolved))
        sys.stderr.write("available tags: %s\n" % ", ".join(sorted(rules.tags)))
        return 2
    if args.enable_only:
        rules = rules.enable_only(args.enable_only)
    if args.disable:
        rules = rules.disable(args.disable)

    budget = Budget(max_nodes=args.max_nodes, max_depth=args.max_depth,
                    max_size=args.max_size)

    if args.command == "rules":
        for r in rules:
            print(r.describe())
        print("\n%d rules, tags: %s" % (len(rules), ", ".join(sorted(rules.tags))))
        return 0

    if args.command == "normalize":
        for src in args.args:
            norm = normalize(parse(src), rules, budget)
            print(norm.render())
            if norm.cycle:
                print("  !! cycle of %d terms" % len(norm.cycle))
            print()
        return 0

    if args.command == "prove":
        if len(args.args) != 2:
            sys.stderr.write("error: prove needs exactly two expressions\n")
            return 2
        proof = prove(parse(args.args[0]), parse(args.args[1]), rules, budget)
        print(proof.render())
        return 0 if proof.proved else 1

    report = check(spec, rules, budget, confluence=not args.no_confluence)
    if args.bisect:
        bisect_report(report, spec, rules, budget)
    print(render(report, rules, verbose=args.verbose))
    return 1 if (report.failed or report.canaries) else 0


if __name__ == "__main__":
    sys.exit(main())
