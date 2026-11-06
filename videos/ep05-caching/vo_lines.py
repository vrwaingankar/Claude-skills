LINES = [
 "Same order, made from scratch, every single time. That's how most LLM apps run.",
 "Hi, I'm [Vineeth](/vɪnˈiθ/), a senior AI architect and tech lead.",
 "Last time: asynchronous batching kept the GPU busy. Today: caching, the first of four episodes.",
 "Calling a model at scale is slow and expensive, and much of that cost is repeated work.",
 "The same system prompt, reprocessed on every request. The same questions, answered as if new.",
 "Inference caching stores that work and reuses it, in three layers.",
 "At the bottom, KV caching. Inside one request, it keeps the attention keys and values, so new tokens skip recomputing the past. Always on.",
 "In the middle, prefix caching. A shared prefix, like a system prompt or a document, is computed once, and reused across requests.",
 "On top, semantic caching. If a new question means the same as an old one, the stored answer comes back, and the model is never called.",
 "So: every app gets KV caching. Long shared prompts, RAG and agents get prefix caching. High volume with paraphrased questions gets semantic.",
 "They're not alternatives. Layer them, and start with prefix caching: the biggest win for most apps.",
 "Next episode: KV caching, up close. Follow so you don't miss it.",
]
