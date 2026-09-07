# 3. Prompt injection in, secrets out

The moment your prompt includes text you didn't write — a web page, a support ticket, a PDF, a tool result — you have an injection surface. That text can carry instructions, and the model, being helpful, may follow them instead of you. "Ignore your previous instructions and…" is the toy version; the real ones hide in retrieved documents and look nothing like an attack.

The mirror image is just as bad: the model *emitting* something it shouldn't — an API key that wandered into context, a customer's email, a chunk of another tenant's data. Injection is the inbound risk; leakage is the outbound one. You need to think about both directions.

## The pattern

Treat the model like a browser rendering untrusted input: **filter on the way in, filter on the way out.**

**Inbound**
- Keep a hard boundary between *instructions* (yours, trusted) and *data* (everything else). Never concatenate untrusted text into the instruction block.
- Scan retrieved/user content for known injection shapes before it reaches the model. You won't catch everything, but the obvious 80% is cheap.
- Assume some injection gets through anyway — which is why the outbound filter and real authorization (see [agent guardrails](07-agent-guardrails.md)) exist.

**Outbound**
- Redact secrets and PII from responses before they're logged, returned, or shown. API keys, tokens, emails, card-shaped numbers — pattern-match and mask.
- Log the *fact* that you redacted, not the secret. A redaction you can't audit is a rumor.

## The gotcha

Don't try to win with one giant regex — you'll get false positives that mangle legitimate output and false negatives that miss the creative attacks. Layer it: cheap deterministic filters for the known-bad, plus a real trust boundary so a miss isn't catastrophic. Defense in depth, because any single layer will fail eventually.

## The tool

**[prompt-shield](https://github.com/parag-labs/prompt-shield)** is a firewall for LLM apps: block prompt injection inbound, redact PII and secrets outbound. It's the layer that assumes your input is hostile and your output is quotable — because both are true.

See [`examples/prompt_injection_filter.py`](../examples/prompt_injection_filter.py) for the inbound half, boiled down.
