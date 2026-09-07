# 6. Rate limits and quotas

Model APIs are a shared, expensive, rate-limited resource, and by default your service treats them like an infinite one. That gap is where the 2am incident lives.

Two shapes, same root cause. One tenant runs a bulk job and consumes the whole provider rate limit, so every other tenant starts getting 429s and timeouts — a noisy neighbor. Or a retry loop, a bad deploy, or an abusive client quietly runs up thousands of dollars before anyone notices, because nothing was counting. You need to bound both *how fast* and *how much*.

## The pattern

Put a budget in front of the provider, scoped to who's spending.

1. **Count the right thing.** For LLMs that's usually *tokens*, not requests — one request can be 100 tokens or 100,000. Budget the resource that actually costs money and consumes the rate limit.
2. **Sliding windows, not fixed buckets.** Fixed calendar windows let someone spend the whole allowance at 11:59 and the whole next one at 12:01 — a 2× burst across a boundary. A sliding window smooths that.
3. **Scope per tenant/user**, so one caller's budget can't starve another's. Global-only limits protect the provider from you but don't protect your tenants from each other.
4. **Reserve, then reconcile.** You don't know the exact token cost until the response comes back, so reserve an estimate up front and settle the real number after. It keeps the accounting honest under concurrency without a lock on the hot path.

## The gotcha

A limiter that fails *closed* on its own errors is a self-inflicted outage — if the accounting store hiccups and every call gets denied, you've turned a dependency wobble into a full stop. Decide the failure mode deliberately (usually: fail open with a loud alert), and make the limit observable so people can see how close to the ceiling they're running *before* they hit it.

## The tool

**[quota-gate](https://github.com/parag-labs/quota-gate)** is a rate limiter built for LLM traffic: per-model token and request budgets across sliding windows, scoped per tenant/user, with the reserve-then-reconcile pattern so concurrent calls account correctly. Three languages, with a design doc and benchmarks against the naive approaches.
