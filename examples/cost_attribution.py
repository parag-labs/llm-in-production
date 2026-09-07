#!/usr/bin/env python3
"""
Cost attribution — the two-minute version.

Idea (see notes/01-cost-attribution.md): every model call already knows who it's
for. Log a tiny record next to each call, turn tokens into dollars with a price
table, then group by whatever dimension the question is about. Add a budget gate
so CI goes red when a window blows the budget.

The real tool (feature/tenant/model attribution, anomaly + creep detection,
OpenTelemetry ingest, three languages) lives at:
    https://github.com/parag-labs/token-lens

This file is standard-library only. Run it:
    python examples/cost_attribution.py
"""

from __future__ import annotations

import sys
from collections import defaultdict
from dataclasses import dataclass

# USD per 1,000,000 tokens. In real life this belongs in version control, not code.
PRICES = {
    "gpt-4o":      {"in": 2.50, "out": 10.00},
    "gpt-4o-mini": {"in": 0.15, "out": 0.60},
    "claude-3.5":  {"in": 3.00, "out": 15.00},
}


@dataclass(frozen=True)
class Call:
    feature: str
    tenant: str
    model: str
    prompt_tokens: int
    completion_tokens: int

    def cost_usd(self) -> float:
        p = PRICES[self.model]
        return (self.prompt_tokens * p["in"] + self.completion_tokens * p["out"]) / 1_000_000


# A stand-in for your usage log. In production this is one structured line per call.
USAGE = [
    Call("summarize",  "acme",    "gpt-4o",      12_000, 1_800),
    Call("summarize",  "globex",  "gpt-4o",      30_000, 4_000),
    Call("autocomplete", "acme",  "gpt-4o-mini", 2_000,    400),
    Call("autocomplete", "initech","gpt-4o-mini", 90_000, 12_000),
    Call("chat",       "globex",  "claude-3.5",  8_000,   2_400),
    Call("chat",       "acme",    "claude-3.5",  6_000,   1_500),
    Call("report-gen", "initech", "gpt-4o",      40_000,  9_000),
]

BUDGET_USD = 1.00  # for the window represented by USAGE


def report(calls: list[Call], dimension: str) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    for c in calls:
        totals[getattr(c, dimension)] += c.cost_usd()
    return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))


def main() -> int:
    total = sum(c.cost_usd() for c in USAGE)

    print(f"LLM cost report  -  {len(USAGE)} calls, ${total:.4f} total\n")
    for dimension in ("feature", "tenant", "model"):
        print(f"by {dimension}:")
        for name, cost in report(USAGE, dimension).items():
            share = 100 * cost / total if total else 0
            print(f"  {name:<14} ${cost:0.4f}  ({share:4.1f}%)")
        print()

    # Budget gate: this is the line you actually put in CI.
    if total > BUDGET_USD:
        over = total - BUDGET_USD
        print(f"OVER BUDGET by ${over:.4f} (budget ${BUDGET_USD:.2f}) — failing.")
        return 1
    print(f"within budget (${total:.4f} <= ${BUDGET_USD:.2f}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
