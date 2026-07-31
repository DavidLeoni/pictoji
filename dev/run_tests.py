#!/usr/bin/env python3
"""Run the test suite without pytest installed.

    python3 run_tests.py [pattern]

The tests under `pictoji_algebra/tests/` are written for pytest and should be
run with it wherever it is available:

    python3 -m pytest pictoji_algebra/tests -v

But `pytest` is only listed in pyproject's `dev` extra and is absent from some
environments (including CI containers with no package index), and a test suite
you cannot execute is not a test suite.  So this module installs a minimal
stand-in for the handful of pytest APIs the tests actually use - `fixture`,
`mark.parametrize`, `raises`, `importorskip`, `skip` - and runs them.

It is a fallback, not a replacement: pytest remains the reference runner.
"""

from __future__ import annotations

import importlib
import inspect
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))


class Skipped(Exception):
    pass


class _Raises:
    def __init__(self, expected):
        self.expected = expected
        self.value = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            raise AssertionError("DID NOT RAISE %s" % (self.expected,))
        if not issubclass(exc_type, self.expected):
            return False
        self.value = exc
        return True


class _Mark:
    @staticmethod
    def parametrize(argnames, argvalues):
        names = [n.strip() for n in argnames.split(",")] if isinstance(argnames, str) \
            else list(argnames)

        def deco(fn):
            cases = []
            for value in argvalues:
                row = value if isinstance(value, (tuple, list)) else (value,)
                cases.append(dict(zip(names, row)))
            fn._parametrized = cases
            return fn
        return deco

    def __getattr__(self, _name):            # unknown marks are no-ops
        return lambda *a, **k: (lambda fn: fn)


class _Pytest:
    """Just enough pytest to run this suite."""
    mark = _Mark()
    raises = _Raises

    @staticmethod
    def fixture(*args, **kwargs):
        def deco(fn):
            fn._fixture = True
            return fn
        if args and callable(args[0]):
            return deco(args[0])
        return deco

    @staticmethod
    def skip(reason=""):
        raise Skipped(reason)

    @staticmethod
    def importorskip(name, reason=""):
        try:
            return importlib.import_module(name)
        except ImportError:
            raise Skipped(reason or ("missing module %s" % name))


def install_shim() -> bool:
    """Return True if the shim was installed (i.e. real pytest is absent)."""
    try:
        import pytest  # noqa: F401
        return False
    except ImportError:
        sys.modules["pytest"] = _Pytest()  # type: ignore[assignment]
        return True


def run(pattern: str = "") -> int:
    shimmed = install_shim()
    modules = sorted((HERE / "pictoji_algebra" / "tests").glob("test_*.py"))

    passed = failed = skipped = 0
    failures = []

    for path in modules:
        mod = importlib.import_module("pictoji_algebra.tests.%s" % path.stem)
        fixtures = {n: f for n, f in vars(mod).items()
                    if callable(f) and getattr(f, "_fixture", False)}
        cache: dict = {}

        def resolve(name):
            if name not in cache:
                fn = fixtures[name]
                kwargs = {p: resolve(p) for p in inspect.signature(fn).parameters}
                cache[name] = fn(**kwargs)
            return cache[name]

        tests = [(n, f) for n, f in vars(mod).items()
                 if n.startswith("test_") and callable(f)]
        tests.sort(key=lambda pair: inspect.getsourcelines(pair[1])[1])

        for name, fn in tests:
            if pattern and pattern not in name and pattern not in path.stem:
                continue
            params = inspect.signature(fn).parameters
            cases = getattr(fn, "_parametrized", [{}])
            for case in cases:
                label = "%s::%s%s" % (path.stem, name,
                                      ("[%s]" % ",".join(map(repr, case.values()))) if case else "")
                try:
                    kwargs = dict(case)
                    for p in params:
                        if p not in kwargs:
                            kwargs[p] = resolve(p)
                    fn(**kwargs)
                    passed += 1
                except Skipped as exc:
                    skipped += 1
                    print("s %s  (%s)" % (label, exc))
                except Exception:
                    failed += 1
                    failures.append((label, traceback.format_exc()))
                    print("F %s" % label)

    for label, tb in failures:
        print("\n" + "=" * 74)
        print("FAILED %s" % label)
        print("-" * 74)
        print(tb)

    note = "  (pytest shim)" if shimmed else "  (real pytest importable)"
    print("\n%d passed, %d failed, %d skipped%s" % (passed, failed, skipped, note))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else ""))
