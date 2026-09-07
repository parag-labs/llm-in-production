# 2. Evals in CI: stop finding regressions from users

Prompts are code. We just don't treat them like code, because they live in a triple-quoted string and there's no red X when you break one.

Here's the failure mode. Someone tweaks a system prompt to fix one annoying case. It ships. It also quietly made three other cases worse, but nothing failed — the output was still plausible-looking text. You find out days later when a user complains, and now you're bisecting prompt history trying to remember which "small wording fix" did it.

## The pattern

Put a quality gate in CI that fails the build when a change regresses the outputs you care about.

1. **Build a small eval set** of inputs with a notion of "good." Start with 15–20 cases pulled from real traffic and past bugs. It does not need to be big; it needs to be *representative and honest*.
2. **Pick a grader per case.** Not everything needs an LLM judge. Exact match, regex, JSON-schema validity, "contains the required disclaimer," "does *not* contain a competitor's name" — cheap deterministic graders catch most regressions and never flake. Reserve model-graded scoring for the genuinely fuzzy stuff.
3. **Gate on the aggregate.** Set a pass threshold (say 90% of cases) and fail CI below it. Print which cases regressed so the diff is obvious.

## The gotcha

Two of them. First, **flaky graders are worse than no graders** — if the gate goes red at random, people learn to ignore red, and then it's decoration. Prefer deterministic graders; sample the model-graded ones and allow a margin. Second, **evals rot**. When a real bug slips through, the fix is one line of prompt *and* one new eval case, so the same bug can never come back silently.

## The tool

**[eval-forge](https://github.com/parag-labs/eval-forge)** is an eval-driven CI gate for exactly this: define cases and graders, run them, fail the build when a prompt or model change drops below your bar. The point isn't a fancy score — it's turning "we should really check that" into "the build fails if we don't."

A stripped-down version you can run right now is in [`examples/eval_gate.py`](../examples/eval_gate.py).
