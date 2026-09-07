# 4. Data drift: the world moves, your model doesn't

Nothing in your code changed. Metrics were green. And quality still degraded over three weeks. This is the one that erodes trust in monitoring, because there's no deploy to point at.

The cause is drift: the live inputs slowly stop resembling what the model was built and evaluated on. A new customer segment onboards. A product launches and the vocabulary shifts. An upstream service starts formatting a field differently. The model didn't get worse at its job — its job quietly changed underneath it.

## The pattern

Watch the **distribution of your inputs (and outputs)**, not just averages and error rates.

1. **Snapshot a reference.** The feature distribution from training, or from a known-good window. That's your baseline.
2. **Compare the live window against it** with a proper distributional statistic, not a mean. Two go a long way:
   - **PSI** (Population Stability Index) — a bucketed, symmetric "how far has this shifted" score with rules of thumb everyone already trusts (>0.2 = investigate).
   - **KL divergence** — when you want a sharper, information-theoretic read on how one distribution diverges from another.
3. **Alert on the drift score**, well before it shows up in your quality metrics. Drift is a leading indicator; a satisfaction-score dip is a lagging one.

## The gotcha

Not all drift matters, and crying wolf is how you get monitoring switched off. A shift in a feature the model barely uses is noise; a shift in a load-bearing one is a page. Weight by importance, set thresholds from the reference's own natural week-to-week variation, and make the alert say *which* feature moved — "something drifted" is not actionable at 2am.

## The tool

**[drift-watch](https://github.com/parag-labs/drift-watch)** does PSI and KL-divergence drift detection for ML monitoring, implemented the same way in three languages so the number means the number regardless of where your pipeline runs. Point it at a reference and a live window; it tells you what moved and how much.
