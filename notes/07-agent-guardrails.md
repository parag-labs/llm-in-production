# 7. Agent guardrails

A chatbot that says something wrong is embarrassing. An *agent* — a model with tools — that *does* something wrong is an incident. The moment you hand a model the ability to call functions, hit APIs, run code, or touch a filesystem, "the model hallucinated" stops being a quality bug and becomes a security one.

And you can't prompt your way out of this. "Please don't delete anything important" is not an access-control policy. Injection (see [note 3](03-prompt-injection.md)) makes it worse: if untrusted text can reach the model, untrusted text can try to steer the tools. The instruction layer is exactly the layer you can't trust to enforce its own limits.

## The pattern

Put the guardrails **outside** the model, in the layer that runs the tools.

1. **Least privilege, enforced in code.** The agent gets an explicit allowlist of tools and arguments. Everything else is denied by default — not discouraged by the prompt, *denied* by the runtime. If it's not on the list, the call never happens.
2. **Mediate every tool call.** Route calls through a policy check that can see the tool, the arguments, and the context, and can say no. The model *requests*; your code *decides*.
3. **Sign the audit log.** Record every tool call and every allow/deny decision in a tamper-evident log. When something does go wrong (it will), you need to reconstruct exactly what the agent tried, not guess.
4. **Contain the blast radius.** Sandbox side effects. Scope credentials to the minimum. Assume any single tool call could be adversarial and design so that one bad call can't take down the house.

## The gotcha

The dangerous tools are rarely the obvious ones. Everyone guards "delete database." Fewer people guard the tool that writes a file whose path the model controls, or the "fetch this URL" that becomes an SSRF into your metadata endpoint. Enumerate tools by *what an adversary could do with them*, not by how scary they sound.

## The tool

**[agent-guard](https://github.com/parag-labs/agent-guard)** is a zero-trust runtime sandbox for tool-calling agents: a least-privilege policy that mediates every tool call plus a signed audit log, so the guardrails live in the runtime where they can actually be enforced — not in a prompt the model is free to ignore.

For seeing what an agent actually did — where it spent time, tokens, and money — pair it with [agent-trace](https://github.com/parag-labs/agent-trace).
