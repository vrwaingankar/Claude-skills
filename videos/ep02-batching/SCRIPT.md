# Ep 02 — Voiceover script (Batching)

Narrator: Kokoro `am_michael` 1.0 (name line 0.95). TTS text in `vo_lines.py`; line layout in `vo_layout.json`.

| # | Line | On screen |
| --- | --- | --- |
| 0 | Your GPU is probably sitting idle. Here's why. | GPU as a bus: 1 rider, 3 idle seats |
| 1 | Hi, I'm Vinit ("Vineeth"), a senior AI architect and tech lead. | Name card |
| 2 | Last time: three layers and six techniques. Today, the first one: batching. | Previously · Ep 1: the stack; Batching chip lights |
| 3 | Batching groups requests, so each GPU step does more work, and tokens cost less. | Requests → one batch → GPU; work ↑ cost ↓ |
| 4 | But LLMs write token by token, with a KV cache, and lengths vary: fifty tokens here, five hundred there. | Tokens append, KV cache fills, 50 vs 500 bars |
| 5 | Static batching waits for the longest request. Short ones finish, and their slots sit idle. | Grid: rows end, idle hatched cells, GPU busy drops |
| 6 | Dynamic batching starts when the batch fills, or a timer runs out. Better, but still waiting. | Batch tray + timeout ring, next requests wait |
| 7 | Continuous batching works token by token. When one request finishes, a new one takes its slot. | Same grid: queue refills slots, GPU busy full |
| 8 | No idle slots, much higher throughput. vLLM and TGI made it popular. | Throughput gauge, vLLM · TGI |
| 9 | Offline jobs, like millions of support tickets, want throughput and low cost. | Split: Offline (tickets, throughput, cost) |
| 10 | Live chat wants speed: time to first token, and the gap between tokens. | Split: Online (chat, two stopwatches) |
| 11 | Next episode: continuous batching, in depth. Follow so you don't miss it. | Ep 3 · Continuous batching |
