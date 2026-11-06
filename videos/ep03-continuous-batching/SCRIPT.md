# Ep 03 — Voiceover script (Continuous batching, in depth)

Narrator: Kokoro `am_michael` 1.0 (name line 0.95, reused). TTS text in `vo_lines.py`; layout in `vo_layout.json`.

| # | Line | On screen |
| --- | --- | --- |
| 0 | Your GPU might be shipping air. Here's where it hides. | Truck of crates, mostly red padding |
| 1 | Hi, I'm Vinit ("Vineeth"), a senior AI architect and tech lead. | Name card |
| 2 | Last time: three ways to batch. Today, how continuous batching really works. | Static / Dynamic / Continuous mini grids |
| 3 | The goal: more tokens per second, from many prompts at once. | Throughput gauge, 4 parallel streams |
| 4 | The naive batch is a rectangle. Short prompts get padding on the left, and the attention mask hides it. | Left-padded rectangle |
| 5 | Prefill once, then decode token by token. When one prompt ends, its slot keeps working for nothing. | Prefill flash, decode columns, eos, wasted cells |
| 6 | Swap in a waiting prompt? It needs prefill while the others decode, so they all get padded. | New prompt in, others padded (18) |
| 7 | That's n minus one, times B minus one, pads. Eight prompts, a hundred-token newcomer: six hundred ninety-three. | (n−1)×(B−1), B=8, n=100, 693 |
| 8 | CUDA graphs and torch compile need fixed shapes, so we pad to the max. More waste. | Pad to max |
| 9 | The fix: drop the batch axis. Put every prompt end to end, in one long row. | Rows slide into one ragged row |
| 10 | The attention mask keeps them apart. That's ragged batching: no padding. | Block-diagonal causal mask |
| 11 | Fill a budget of M tokens: decoding prompts first, one token each, then prefill chunks. | Budget bar M |
| 12 | When a prompt finishes, it leaves at once, and the next chunk takes its place. | Slot refills |
| 13 | KV cache, chunked prefill, ragged batching, dynamic scheduling: that's continuous batching. | The sum |
| 14 | Next episode: asynchronous batching. Follow so you don't miss it. | Ep 4 · Asynchronous batching |
