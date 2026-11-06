# Ep 04 — Voiceover script (Asynchronous batching)

Source: huggingface.co/blog/continuous_async (paraphrased). Narrator: Kokoro `am_michael` 1.0 (name line 0.95, reused).
TTS text in `vo_lines.py`; layout in `vo_layout.json`.

| # | Line | On screen |
| --- | --- | --- |
| 0 | Your GPU spends almost a quarter of its time waiting for your CPU. | Kitchen: prep cook chops, stove idle (~24%) |
| 1 | Hi, I'm Vinit ("Vineeth"), a senior AI architect and tech lead. | Name card |
| 2 | Last time: continuous batching. Today, we make it asynchronous. | Ragged row + "+ async" |
| 3 | The loop is synchronous: the GPU computes while the CPU waits, then the CPU preps while the GPU waits. | CPU/GPU lanes taking turns, red waits |
| 4 | In one profile: three hundred seconds, and the GPU sat idle for twenty-four percent of it. | 8B · batch 32 · 8K tokens · 300.6 s · 24% idle · ~228 s |
| 5 | The fix: prep batch N plus one on the CPU, while the GPU runs batch N. | Overlapped lanes |
| 6 | CUDA streams split the work: inputs in, compute, outputs out. | H2D / compute / D2H lanes |
| 7 | Launch them freely, and results come back instantly, and wrong. | All start together → "wrong" |
| 8 | CUDA events fix the order, and the CPU blocks only once per step. | record → wait links |
| 9 | Two input slots, A and B, take turns, so the CPU never overwrites what the GPU is reading. | Slots A/B swap; ~2× I/O memory |
| 10 | Each slot gets its own captured graph, in one shared memory pool. | CUDA graphs + shared pool |
| 11 | And tokens batch N hasn't made yet? A zero placeholder, then a carry-over mask swaps in the real one, on the GPU. | 0 placeholder, mask [−1, −1, 2, −1] |
| 12 | The result: the GPU is busy ninety-nine point four percent of the time, up from seventy-six. Twenty-two percent faster. | 300.6 s vs 234.5 s, 76.0% vs 99.4%, 22% (ceiling 24%) |
| 13 | It ships in Hugging Face transformers, built for long generations. | transformers · ContinuousBatchingAsyncIOs · 16K+ tokens |
| 14 | Next episode: caching. Follow so you don't miss it. | Ep 5 · Caching |
