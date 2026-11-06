# Caching mini-series (Ep 05–08)

Source: Bala Priya C, "The Complete Guide to Inference Caching in LLMs", Machine Learning Mastery (Apr 18 2026), paraphrased.

| Ep | Title | Covers |
| --- | --- | --- |
| **05** | **Caching: the three layers** (high level) | why caching (cost and latency of repeated work), KV / prefix / semantic as complementary layers, the decision table, "layer them" |
| 06 | KV caching | Q / K / V, autoregressive decode, recompute 1–99 vs load 1–99, always on, the base for the rest |
| 07 | Prefix caching | shared system prompt computed once; exact byte-for-byte match; static first, dynamic last; stable JSON key order; Anthropic `cache_control`, OpenAI automatic over 1024 tokens, Gemini context caching billed for storage, vLLM / SGLang automatic |
| 08 | Semantic caching | embed → vector search → cosine threshold → hit returns the answer or miss calls the LLM and stores the result; Pinecone / Weaviate / pgvector; TTL; the overhead only pays off at high volume with paraphrased repeats (FAQ, support bots) |

Every episode: hook → Vinit's name card → recap of the previous episode → topic → end card pointing to the next one in this table.

---

# Ep 05 — Caching: the three layers

**The one thing:** caching is three layers, not one trick. KV caching is always on, prefix caching is the biggest win to add, and semantic caching sits on top when volume justifies it.

**Facts (from the article):**
- Calling an LLM at scale is expensive and slow, and much of the cost is repeated work: the same system prompt processed from scratch every request, and the same common questions answered as if new.
- Inference caching stores the results of that computation and reuses them when an equivalent request arrives.
- **KV caching** stores the attention key/value pairs inside one request so each decode step doesn't recompute them. It's automatic and always on.
- **Prefix caching** (also called prompt caching or context caching) reuses the KV states of a shared leading prefix (system prompt, reference document, few-shot examples) across requests.
- **Semantic caching** is application-side: it stores whole input/output pairs and returns a stored answer when a new query is similar enough, skipping the model call entirely.
- They're complementary layers, not alternatives. Prefix caching is "the highest-leverage optimization you can add to most production applications".
- Decision table: all apps → KV (nothing to configure). A long shared system prompt, RAG with large shared documents, or agents with a large stable context → prefix. High volume where users paraphrase the same questions → semantic.

## A. Three floors (recommended: one picture that maps the whole mini-series)
**Device:** the object is the explanation · **Form:** one frame that rebuilds
One building is the request path, and each floor is a cache layer. The ground floor, KV, is lit from the start ("always on"). The middle floor, prefix, lights up as a long system-prompt block gets stamped "computed once" and many requests reuse it. The top floor, semantic, catches a paraphrased question and answers it without ever reaching the model. Then the decision table drops in as floor plates, one use case per floor, and the building pulls back to "layer them".
- **First 2 s:** the same system-prompt block being recomputed again and again (a stack of identical blocks, each with "computed again" in red), with the line "You keep paying for the same tokens."
- **Beats:** hook → intro → recap (async, Ep 4) → why: repeated work → floor 1 KV → floor 2 prefix → floor 3 semantic → decision table → layer them, prefix first → end card "Ep 6 — KV caching"
- **Look:** series look; the building in navy line art, lit floors green-outlined, red only for recomputed work.

## B. The coffee shop
**Device:** a metaphor made literal · **Form:** object-to-object chain
A barista remembers your half-made drink mid-order (KV), keeps a batch of the house base ready for everyone (prefix), and hands over a ready cup when you ask for "the usual" in different words (semantic). It then flips into the real stack diagram.
- **First 2 s:** a barista grinding beans from scratch for every identical order, with the line "Same order. Made from scratch. Every time."

## C. The bill (the bold one)
**Device:** a number lands · **Form:** split screen to one
A running token bill on the left and a timer on the right. Each layer switches on and visibly stops part of the meter: KV stops recomputing inside a request, prefix stops re-reading the shared prompt, semantic skips whole calls. The article gives no numbers, so the meters are labelled illustrative.
- **First 2 s:** a token meter spinning, with the line "Most of these tokens are repeats."

**Assumptions:** 60–85 s, same voice, no invented numbers (the only figure in the article is OpenAI's 1024-token threshold, which belongs in Ep 7).
