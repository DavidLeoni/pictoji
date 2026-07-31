"""CLI:  python -m pictoji_algebra check pictoji-test-algebra.md

Exit code is nonzero when a canary trips or an assertion fails, so this can be
a real CI gate - unlike the existing workflow, which runs the token counter
with `|| true` and therefore cannot fail.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .diagnose import bisect_report, check
from .engine import Budget
from .report import render
from .rules import RuleSet
from .specload import load


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pictoji_algebra",
        description="Check the Pictoji algebra for consistency on its own test cases.")
    p.add_argument("command", choices=["check", "rules", "normalize", "prove"])
    p.add_argument("args", nargs="*", help="spec file, or expressions for normalize/prove")
    p.add_argument("--spec", default="pictoji-test-algebra.md",
                   help="spec markdown to load (default: %(default)s)")
    p.add_argument("--disable", action="append", default=[], metavar="SEL",
                   help="disable rules by id, tag, or glob (repeatable)")
    p.add_argument("--enable-only", action="append", default=[], metavar="SEL",
                   help="keep only rules matching these selectors (repeatable)")
    p.add_argument("--bisect", action="store_true",
                   help="delta-debug each tripped canary to a minimal axiom set")
    p.add_argument("--no-confluence", action="store_true",
                   help="skip the multi-normal-form check (it is the slow part)")
    p.add_argument("--verbose", "-v", action="store_true", help="show every derivation")
    p.add_argument("--max-depth", type=int, default=6)
    p.add_argument("--max-nodes", type=int, default=4000)
    p.add_argument("--max-size", type=int, default=60)
    return p


def select(rules: RuleSet, args) -> RuleSet:
    unresolved = rules.unresolved_selectors(list(args.disable) + list(args.enable_only))
    if unresolved:
        # A typo'd selector silently selecting nothing would quietly change what
        # was tested, which is the last thing a bisection tool should do.
        sys.stderr.write("error: selectors match no rule: %s\n" % ", ".join(unresolved))
        sys.stderr.write("available tags: %s\n" % ", ".join(sorted(rules.tags)))
        raise SystemExit(2)
    if args.enable_only:
        rules = rules.enable_only(args.enable_only)
    if args.disable:
        rules = rules.disable(args.disable)
    return rules


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    spec_path = Path(args.args[0]) if args.args and args.command == "check" else Path(args.spec)
    if not spec_path.exists():
        sys.stderr.write("error: spec file not found: %s\n" % spec_path)
        return 2

    spec = load(spec_path)
    rules = select(spec.rules, args)
    budget = Budget(max_nodes=args.max_nodes, max_depth=args.max_depth,
                    max_size=args.max_size)

    if args.command == "rules":
        for r in rules:
            print(r.describe())
        print("\n%d rules, tags: %s" % (len(rules), ", ".join(sorted(rules.tags))))
        return 0

    if args.command == "normalize":
        from .parser import parse
        from .engine import normalize
        for src in args.args:
            norm = normalize(parse(src), rules, budget)
            print(norm.render())
            if norm.cycle:
                print("  !! cycle of %d terms" % len(norm.cycle))
            print()
        return 0

    if args.command == "prove":
        from .parser import parse
        from .engine import prove
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
