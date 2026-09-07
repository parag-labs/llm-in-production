# LLM in Production

**Field notes on shipping LLM features you can actually trust — and the small tools I built to keep them honest.**

I've spent the last couple of years putting LLM-backed features in front of real users at work, and then most of my nights and weekends building small, single-purpose tools to fix the things that kept biting me. This repo is the connective tissue: the *why* behind each of those tools, written the way I'd explain it to a teammate over coffee, with the reusable pattern pulled out so you don't have to relearn it the hard way.

It is not a framework. There's nothing to `pip install` here. It's notes plus a few tiny, runnable examples — and links to the actual libraries where each idea is implemented properly, with tests and benchmarks.

> If you only read one thing, read [`checklist.md`](checklist.md) — the pre-launch checklist I run through before pointing production traffic at anything that calls a model.

---

## The seven things that will bite you

Almost every LLM-in-production headache I've hit falls into one of these buckets. Each note is short on purpose: the problem, why it's worse than it looks, the pattern that fixed it, and the tool I built so I never have to think about it again.

| # | The problem | Note | The tool I built for it |
|---|-------------|------|-------------------------|
| 1 | Your bill is a black box — nobody can say which feature or tenant is burning the money | [Cost attribution](notes/01-cost-attribution.md) | [token-lens](https://github.com/parag-labs/token-lens) |
| 2 | A prompt tweak silently regresses quality and you find out from users | [Evals in CI](notes/02-evals-in-ci.md) | [eval-forge](https://github.com/parag-labs/eval-forge) |
| 3 | Prompt injection in, PII/secrets out | [Prompt injection & leaks](notes/03-prompt-injection.md) | [prompt-shield](https://github.com/parag-labs/prompt-shield) |
| 4 | The world drifts away from the data your model expects | [Data drift](notes/04-data-drift.md) | [drift-watch](https://github.com/parag-labs/drift-watch) |
| 5 | RAG answers that you can't prove are grounded in anything real | [Retrieval you can trust](notes/05-retrieval-you-can-trust.md) | [ledger-rag](https://github.com/parag-labs/ledger-rag) |
| 6 | One tenant hammers the API and everyone else's latency falls over | [Rate limits & quotas](notes/06-rate-limits-and-quotas.md) | [quota-gate](https://github.com/parag-labs/quota-gate) |
| 7 | A tool-calling agent does something you very much did not intend | [Agent guardrails](notes/07-agent-guardrails.md) | [agent-guard](https://github.com/parag-labs/agent-guard) |

There are a few more tools past these seven — resilience gates, schema-change detection, point-in-time feature joins, run tracing — listed at the [bottom](#the-rest-of-the-toolbox).

## Try the examples

The `examples/` folder has three tiny, dependency-free Python scripts — the *idea* behind three of the tools, stripped down to something you can read in one sitting and run right now. Standard library only, no install:

```bash
git clone https://github.com/parag-labs/llm-in-production
cd llm-in-production

python examples/cost_attribution.py         # who spent the money?
python examples/eval_gate.py                # fail CI when quality drops
python examples/prompt_injection_filter.py  # catch the obvious attacks
```

Each one prints a short, readable report and exits non-zero when something's wrong — the same shape you'd wire into CI. They're deliberately naive; the real tools handle the edge cases. Think of these as the two-minute version.

## How this repo is laid out

```
llm-in-production/
├── README.md         you are here — the map
├── checklist.md      the pre-launch checklist I actually run through
├── notes/            one short chapter per production problem
│   ├── 01-cost-attribution.md
│   ├── 02-evals-in-ci.md
│   ├── 03-prompt-injection.md
│   ├── 04-data-drift.md
│   ├── 05-retrieval-you-can-trust.md
│   ├── 06-rate-limits-and-quotas.md
│   └── 07-agent-guardrails.md
└── examples/         runnable, standard-library-only sketches of three ideas
    ├── cost_attribution.py
    ├── eval_gate.py
    └── prompt_injection_filter.py
```

## Who I am, and why to trust any of this

I'm Parag — a software engineer who's spent years shipping backend and platform systems, lately the kind with a model in the hot path. The opinions here are mine and they're earned, but they're still opinions: your traffic, your model, and your risk tolerance are different from mine. Take what's useful, argue with the rest.

Everything I claim is backed by code you can read. The tools aren't slideware — each has a real test suite, most have a `DESIGN.md` where the trade-offs are argued out, and several ship `BENCHMARKS.md` with reproducible numbers.

## The rest of the toolbox

The same "small, focused, actually tested" idea, for problems past the core seven:

- **[schema-guard](https://github.com/parag-labs/schema-guard)** — catch breaking API/schema changes at the pull request, not in production.
- **[chaos-mesh-lite](https://github.com/parag-labs/chaos-mesh-lite)** — resilience testing as a CI/SLO gate: inject faults, assert the SLO still holds.
- **[feature-vault](https://github.com/parag-labs/feature-vault)** — a mini feature store with point-in-time-correct joins that never leak the future.
- **[agent-trace](https://github.com/parag-labs/agent-trace)** — a visual timeline and replay for agent runs: see where a run spent time, tokens, and money, then diff two runs.
- **[deploy-kit](https://github.com/parag-labs/deploy-kit)** — one command to deploy an LLM app into any cloud or on-prem, secure by default.

And when I need to blow off steam, [gpu-flock](https://github.com/parag-labs/gpu-flock) — a few thousand boids flocking entirely on the GPU. Not production anything; just fun.

## License

[MIT](LICENSE). Copy the ideas, copy the code, no attribution needed. If a note saves you an outage, that's payment enough.
