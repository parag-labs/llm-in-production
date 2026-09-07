# 5. Retrieval you can trust

RAG demos beautifully and rots quietly. The demo works because you know the answer is in there. Production is different: someone asks a question, the system returns a confident paragraph, and nobody — not the user, not you, not the auditor six months later — can prove which source it came from, or whether it came from a source at all.

For a chatbot that recommends recipes, fine. For anything where a wrong-and-confident answer has consequences (finance, compliance, health, legal), "trust me" is not an acceptable grounding story.

## The pattern

Make every answer **carry its own proof.**

1. **Bind the answer to its evidence.** Return the retrieved chunks that support it, not as a nice-to-have citation but as a required part of the response contract. No evidence, no answer.
2. **Make the evidence tamper-evident.** If your grounding can be edited after the fact without anyone noticing, it isn't grounding, it's a claim. A cryptographic ledger (hash chain / Merkle structure) over the indexed corpus lets you *prove* that the chunk the answer cites is the chunk that was actually indexed, unaltered.
3. **Ship the proof with the answer.** Then "is this grounded?" stops being a matter of faith and becomes something you verify — offline, later, by anyone, without trusting the server that produced it.

## The gotcha

Citations that don't actually support the claim are worse than none, because they *look* rigorous. It's entirely possible to retrieve the right document and still generate a sentence it doesn't support. Grounding-that-you-can-check has to verify the link between claim and evidence — not just staple a source URL to the bottom and call it cited.

## The tool

**[ledger-rag](https://github.com/parag-labs/ledger-rag)** is verifiable RAG with a tamper-evident cryptographic ledger: every answer ships a proof that ties it to unaltered indexed content, so grounding is something you can check rather than something you're asked to believe. The core is written three times — Python, C#, Java — because a Merkle proof is a plain algorithm and porting it keeps the logic honest.
