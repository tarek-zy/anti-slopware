#!/usr/bin/env python3
"""Run the same tests against every version of the example and print line counts."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(HERE, "python")
VERSIONS = ["before", "easy", "medium", "hard"]


def main():
    failed = False
    for version in VERSIONS:
        with open(os.path.join(PY, version, "orders.py")) as f:
            lines = sum(1 for _ in f)
        result = subprocess.run(
            [sys.executable, os.path.join(PY, "test_orders.py")],
            env={**os.environ, "ORDERS_VERSION": version},
            capture_output=True,
            text=True,
        )
        status = "pass" if result.returncode == 0 else "FAIL"
        print(f"{version:<7} {lines:>3} lines  tests: {status}")
        if result.returncode != 0:
            failed = True
            print(result.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
