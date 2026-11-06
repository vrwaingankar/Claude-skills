# Ep 06 — Voiceover script (KV caching)

Source: Bala Priya C, "The Complete Guide to Inference Caching in LLMs" (Machine Learning Mastery), KV caching section, paraphrased.
Narrator: Kokoro `am_michael` 1.0 (name line 0.95, reused). TTS text in `vo_lines.py`; layout in `vo_layout.json`.

| # | Line | On screen |
| --- | --- | --- |
| 0 | To write token one hundred, does your model re-read the first ninety-nine? | 99 tokens + token 100 |
| 1 | Hi, I'm Vinit ("Vineeth"), a senior AI architect and tech lead. | Name card |
| 2 | Last time: three layers of caching. Today, the bottom one: KV caching. | Building, floor 1 lights |
| 3 | Every token gets three vectors. A query: what it's looking for. A key: what it offers. A value: what it carries. | Q, K, V |
| 4 | Attention compares each token's query with the keys of all earlier tokens, and uses those scores to weigh their values. | Query × keys → scores → weighted values |
| 5 | And the model writes one token at a time. | Tokens one by one |
| 6 | Without a cache, token one hundred means recomputing keys and values for tokens one to ninety-nine. And it compounds, every step. | 99 recomputed; work per step (illustrative) |
| 7 | With KV caching, those keys and values are saved in GPU memory, the first time they're computed. | GPU memory fills |
| 8 | Each new step looks them up, and only the newest token is computed fresh. | Load, don't recompute |
| 9 | Token one hundred: load ninety-nine, compute one. | Without vs with KV |
| 10 | It works inside a single request, and it's automatic: every inference framework turns it on by default. | One request; switch on |
| 11 | And it's the foundation for the next layer: sharing these states across requests. | Building: prefix next |
| 12 | Next episode: prefix caching. Follow so you don't miss it. | Ep 7 · Prefix caching |
