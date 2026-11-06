# Ep 05 — Voiceover script (Caching: the three layers)

Source: Bala Priya C, "The Complete Guide to Inference Caching in LLMs" (Machine Learning Mastery), paraphrased.
Narrator: Kokoro `am_michael` 1.0 (name line 0.95, reused). TTS text in `vo_lines.py`; layout in `vo_layout.json`.

| # | Line | On screen |
| --- | --- | --- |
| 0 | Same order, made from scratch, every single time. That's how most LLM apps run. | Four cups, each "from scratch" |
| 1 | Hi, I'm Vinit ("Vineeth"), a senior AI architect and tech lead. | Name card |
| 2 | Last time: asynchronous batching kept the GPU busy. Today: caching, the first of four episodes. | Ep 4 lanes; Ep 5–8 plan |
| 3 | Calling a model at scale is slow and expensive, and much of that cost is repeated work. | Token bill (illustrative), red = repeated |
| 4 | The same system prompt, reprocessed on every request. The same questions, answered as if new. | Recomputed prompts; two paraphrased questions |
| 5 | Inference caching stores that work and reuses it, in three layers. | compute → store → reuse; 3-floor building |
| 6 | At the bottom, KV caching. Inside one request, it keeps the attention keys and values, so new tokens skip recomputing the past. Always on. | Floor 1 |
| 7 | In the middle, prefix caching. A shared prefix, like a system prompt or a document, is computed once, and reused across requests. | Floor 2 |
| 8 | On top, semantic caching. If a new question means the same as an old one, the stored answer comes back, and the model is never called. | Floor 3 |
| 9 | So: every app gets KV caching. Long shared prompts, RAG and agents get prefix caching. High volume with paraphrased questions gets semantic. | Use case → layer table |
| 10 | They're not alternatives. Layer them, and start with prefix caching: the biggest win for most apps. | Stack, "start here" on prefix |
| 11 | Next episode: KV caching, up close. Follow so you don't miss it. | Ep 6 · KV caching |
