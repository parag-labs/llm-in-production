# 1. Cost attribution: whose spend is that?

The first time an LLM feature is a hit, the second thing that happens (right after the celebration) is someone in finance asking why the model bill tripled. And you won't be able to answer.

The reason is structural. You send tokens to a provider; they send back one number a month later. The bill has no idea that half of it came from one over-eager summarization feature, or that a single enterprise tenant on a flat plan is quietly unprofitable. All of that context — *feature*, *tenant*, *model*, *request* — lives in your app and gets thrown away at the API boundary.

## The pattern

Attribute cost **where you have the context**, at call time, not from the invoice.

1. Every model call already knows who it's for. Log a small record next to it: `{feature, tenant, model, prompt_tokens, completion_tokens}`. One line, structured.
2. Turn tokens into dollars with a per-model price table (USD per million tokens). Prices change, so keep the table in version control, not in code.
3. Roll up by whatever dimension the question is about. "Which *feature* 3×'d this week?" is a group-by, not a mystery.

Once the data is shaped like that, the useful gates fall out cheaply:

- **Budget gate** — sum the window, exit non-zero if it's over. Drop it in CI or a nightly job.
- **Anomaly** — flag any dimension spending far more than the median of its peers *right now*.
- **Creep** — compare a recent window's cost *rate* against an earlier baseline, so you catch the thing slowly ramping up before it's the biggest line on the bill.

## The gotcha

Attribution is only as good as your tags. If everything is logged as `feature=default`, you've built a very precise way to learn nothing. Decide the two or three dimensions that map to a real decision (kill a feature, reprice a tenant, downgrade a model) and make them required fields, not optional.

## The tool

I built **[token-lens](https://github.com/parag-labs/token-lens)** for exactly this — it takes a usage log and attributes cost and latency by feature/tenant/model, with the budget, anomaly, and creep gates ready to wire into CI. It also ingests OpenTelemetry `gen_ai.*` spans, so if you're already tracing you don't have to hand-write the log. Same core in Python, C#, and Java.

The two-minute version is in [`examples/cost_attribution.py`](../examples/cost_attribution.py).
