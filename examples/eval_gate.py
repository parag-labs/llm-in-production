#!/usr/bin/env python3
"""
Eval gate — the two-minute version.

Idea (see notes/02-evals-in-ci.md): prompts are code, so give them a red X. Keep
a small set of representative cases, attach a *deterministic* grader to each
(exact match, regex, JSON validity, "must/must not contain"), run them against
your current system, and fail CI when the pass rate drops below a threshold.

Cheap deterministic graders catch most regressions and never flake. Reserve
model-graded scoring for the genuinely fuzzy cases.

The real tool (case/grader definitions, model-graded scoring with margins,
CI wiring) lives at:
    https://github.com/parag-labs/eval-forge

Standard-library only. Run it:
    python examples/eval_gate.py
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from typing import Callable

PASS_THRESHOLD = 0.90  # fail CI below 90% of cases passing


# --- graders: each returns True if the output is acceptable -------------------

def contains(substr: str) -> Callable[[str], bool]:
    return lambda out: substr.lower() in out.lower()


def excludes(substr: str) -> Callable[[str], bool]:
    return lambda out: substr.lower() not in out.lower()


def matches(pattern: str) -> Callable[[str], bool]:
    rx = re.compile(pattern)
    return lambda out: rx.search(out) is not None


def is_json_with_keys(*keys: str) -> Callable[[str], bool]:
    def grader(out: str) -> bool:
        try:
            obj = json.loads(out)
        except (ValueError, TypeError):
            return False
        return all(k in obj for k in keys)
    return grader


@dataclass
class Case:
    name: str
    grade: Callable[[str], bool]


# --- your "system under test" -------------------------------------------------
# Swap this for a real call to your prompt/model. Kept as a lookup so the example
# is deterministic and offline. Flip one value to see the gate go red.

def system_under_test(case_name: str) -> str:
    responses = {
        "refusal_disclaimer":  "I can't help with that. This is not financial advice.",
        "no_competitor":       "Our plan covers everything you need.",
        "json_shape":          '{"answer": "42", "confidence": 0.9}',
        "greeting_language":   "Hola, ¿en qué puedo ayudarte?",
        "cites_source":        "The revenue was $4.2M [source: 2025-Q4.pdf].",
    }
    return responses.get(case_name, "")


CASES = [
    Case("refusal_disclaimer", contains("not financial advice")),
    Case("no_competitor",      excludes("Globex")),          # must NOT name a competitor
    Case("json_shape",         is_json_with_keys("answer", "confidence")),
    Case("greeting_language",  matches(r"[¿¡]")),             # replied in Spanish
    Case("cites_source",       matches(r"\[source: .+\]")),  # answer carries a citation
]


def main() -> int:
    passed = 0
    print(f"Running {len(CASES)} eval cases (threshold {PASS_THRESHOLD:.0%})\n")
    for case in CASES:
        out = system_under_test(case.name)
        ok = case.grade(out)
        passed += ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {case.name}")
        if not ok:
            print(f"         got: {out!r}")

    rate = passed / len(CASES)
    print(f"\n{passed}/{len(CASES)} passed  ({rate:.0%})")
    if rate < PASS_THRESHOLD:
        print(f"below threshold {PASS_THRESHOLD:.0%} — failing the build.")
        return 1
    print("quality gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
