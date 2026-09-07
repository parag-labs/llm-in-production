# Pre-launch checklist

The list I run through before pointing real traffic at anything with a model in the hot path. It's opinionated and it's not exhaustive — it's the set of questions that have each, at some point, saved me from an avoidable bad day. If I can't answer one of these, it's not ready.

Copy it, cut what doesn't apply, add your own scars.

## Cost
- [ ] Every model call is logged with enough context to answer "whose spend is this?" — at minimum `feature`, `tenant`, `model`, and token counts. → [note](notes/01-cost-attribution.md) · [token-lens](https://github.com/parag-labs/token-lens)
- [ ] There's a **budget gate** somewhere automated (CI or a nightly job), not just a dashboard someone might look at.
- [ ] I'd find out about a slow cost *creep* from an alert, not from the invoice.

## Quality
- [ ] There's an eval set of real, representative cases with graders, and it **fails CI** below a threshold. → [note](notes/02-evals-in-ci.md) · [eval-forge](https://github.com/parag-labs/eval-forge)
- [ ] Most graders are deterministic; the model-graded ones have a margin so they don't flake red.
- [ ] Our process is "fix the bug *and* add the eval case," so regressions can't come back silently.

## Security
- [ ] Untrusted text (retrieved docs, user input, tool results) is never concatenated into the instruction block. → [note](notes/03-prompt-injection.md) · [prompt-shield](https://github.com/parag-labs/prompt-shield)
- [ ] Inbound content is scanned for the obvious injection shapes.
- [ ] Outbound responses are scrubbed for secrets/PII **before** they're logged, returned, or displayed — and the redaction is auditable.

## Agents (if the model can call tools)
- [ ] Tools are an explicit **allowlist**; everything else is denied by the runtime, not discouraged by the prompt. → [note](notes/07-agent-guardrails.md) · [agent-guard](https://github.com/parag-labs/agent-guard)
- [ ] Every tool call goes through a policy check and lands in a signed audit log.
- [ ] I've enumerated tools by *what an adversary could do with them*, and sandboxed the side effects.

## Load & fairness
- [ ] There's a per-tenant/user budget on **tokens** across a sliding window, so one caller can't starve the rest. → [note](notes/06-rate-limits-and-quotas.md) · [quota-gate](https://github.com/parag-labs/quota-gate)
- [ ] The limiter's failure mode is deliberate (usually fail-open + loud alert), not accidental.
- [ ] Headroom to the provider's rate limit is observable *before* we hit it.

## Drift & monitoring
- [ ] Input distributions are watched (PSI / KL), not just averages and error rates — drift is a leading indicator. → [note](notes/04-data-drift.md) · [drift-watch](https://github.com/parag-labs/drift-watch)
- [ ] Alerts name *which* feature moved, weighted by importance, so they're actionable at 2am.

## Grounding (if it's RAG)
- [ ] Answers carry their evidence as part of the response contract — no evidence, no answer. → [note](notes/05-retrieval-you-can-trust.md) · [ledger-rag](https://github.com/parag-labs/ledger-rag)
- [ ] Grounding is verifiable (tamper-evident), not "trust the server."

## Operability
- [ ] I can see what a given run actually did — time, tokens, money, tool calls — and diff two runs. → [agent-trace](https://github.com/parag-labs/agent-trace)
- [ ] There's a tested rollback for the prompt/model, not just for the code.
- [ ] Someone who isn't me could read the runbook and handle the first hour of an incident.

---

If most of these are checked, you're in far better shape than most things I've seen go live. If none are, that's not a failure — it's just the to-do list.
