# Ep 04 — Asynchronous batching

Instagram Reel · 1080×1920 · 30 fps · 70–85 s · Kokoro `am_michael` · series look
Opening (series rule): hook → Vinit's name card → 2–3 s recap of Ep 3 → topic.
Source: Hugging Face blog "continuous_async" (paraphrased).
End card: "Next: Ep 5 — Caching", the next technique in the series order. Vinit can change it.

**The one thing:** in a synchronous loop the CPU and GPU take turns, so one always waits. Async batching overlaps them: the CPU builds batch N+1 while the GPU runs batch N.

**Facts from the source** (paraphrased; numbers exactly as stated):
- Continuous batching packs batches tightly, but the standard loop is synchronous: the GPU computes while the CPU waits, then the CPU prepares the next batch while the GPU waits. "The two never overlap."
- Profile: 8K generated tokens, batch size 32, an 8B model. Total **300.6 s**, of which **24%** had the GPU idle. With zero CPU overhead it would be about **228 s**, roughly a 24% speedup with no kernel or model changes.
- **CUDA streams**: ordered queues of GPU work; different streams can run concurrently. The default stream synchronizes everything, while non-default streams return control to the CPU at once. Three streams: **H2D** (inputs in), **compute** (forward pass), **D2H** (outputs out).
- Streams alone gave results almost instantly, and they were wrong: compute ran before the inputs arrived, and outputs were copied before compute finished.
- **CUDA events**: `record` marks a point in a stream and `wait` holds another stream until that point is reached, without blocking the CPU. The chain is H2D done → compute → compute done → D2H. The CPU blocks only once per step, on D2H done.
- **Double buffering**: two input/output slots, A and B. Batch N uses A while the CPU fills B, and they alternate. This costs about 2× the RAM/VRAM for I/O tensors, which is acceptable with FlashAttention because there's no attention-mask tensor.
- **CUDA graphs**: one graph per slot, both sharing one memory pool. That's safe because they never run at the same time, and the pool is capped at the largest graph.
- **Carry-over**: when a request is in both N and N+1, its newest token doesn't exist yet when N+1 is built. A placeholder 0 goes in, and a carry-over mask (destination position, or −1) adds the real token on the GPU just before N+1 runs. It's cheap and captured in the graph.
- **Loop**: step 0 has no overlap. From then on, while the GPU runs N, the CPU evicts finished requests, admits new ones, updates the KV-cache table, builds the carry-over mask and prepares N+1, then waits on N's outputs. This holds as long as CPU prep finishes before GPU compute does.
- **Results**: GPU active **76.0% → 99.4%**, total time **300.6 s → 234.5 s**, a **22%** speedup against the 24% ceiling. The gap is the one unavoidable sync point.
- It ships in Hugging Face `transformers`, aimed at long generations (16K+ tokens, e.g. RL). The source lists next steps as request offloading, decode-specific kernels and fine-grained compilation.

---

## A. Two clocks, one lane (recommended: a timeline everyone reads instantly)
**Device:** life before and after · **Form:** one frame that rebuilds
A two-lane timeline: CPU on top, GPU below.
- **Synchronous:** the blocks alternate like a relay, and every gap in the GPU lane is painted red (24% idle). A clock reads 300.6 s.
- **Rebuild:** the lanes split into three GPU streams (H2D, compute, D2H). First they fire with no ordering and the results come out wrong, stamped "wrong". Then event links snap between them as arrows.
- **Slots A and B** flip under the lanes.
- **Carry-over:** a "0" placeholder token is patched by an arrow from batch N's output.
- **Async:** the timeline replays with the CPU block for N+1 sliding under GPU block N, the red disappears, the GPU meter climbs 76 → 99.4%, and the clock reads 234.5 s, 22% faster.
- **First 2 s:** frame 0 is the CPU/GPU timeline with red idle gaps and the line "Your GPU waits for your CPU."
- **Beats:** hook → intro → recap → sync loop (300.6 s, 24% idle, 228 s ceiling) → streams → wrong results → events → slots A/B (+ one memory pool) → carry-over (0 + mask) → the async loop → 99.4%, 234.5 s, 22% → transformers, 16K+ tokens → end card
- **Look:** series look; CPU blocks in navy, GPU blocks in tint, idle in red, the green arrow for overlap.
- **Sound:** a tick per block, a buzz under the red gaps, a click per event link, a riser into the result, a pop on the end card.

## B. The kitchen
**Device:** a metaphor made literal · **Form:** object-to-object chain
The GPU is a stove and the CPU is a prep cook. In the synchronous kitchen, the cook chops, then waits while the stove cooks, then chops again. Async: the cook preps the next order while this one cooks, using two cutting boards (slots A/B), with tickets clipped in order (events) and a side dish added when the last one is ready (carry-over). The kitchen then flips into the real timeline with the numbers.
- **First 2 s:** a stove sitting cold while the cook chops, with "Idle 24% of the time".
- **Beats:** hook → intro → recap → sync kitchen → two boards → tickets = events → side dish = carry-over → flip to the timeline → results → end card
- **Look:** flat navy line art; the stove drawn like the series GPU card.
- **Sound:** chopping ticks, a sizzle, a ticket bell, a pop on the end card.

## C. 300.6 → 234.5 (the bold one)
**Device:** a number lands · **Form:** split screen to one
Two stopwatches run side by side, synchronous against async, and each chapter of the mechanism shaves visible seconds off the right one: streams (wrong at first), events, double buffering, carry-over. It ends on 234.5 against 300.6 and a 22% badge, with the 24% ceiling ghosted beside it.
- **First 2 s:** two stopwatches at 0, labelled "Same model. Same GPU." Both start.
- **Beats:** hook → intro → recap → the 24% idle reveal → four mechanisms, each moving the right clock → 22% vs 24% ceiling → end card
- **Look:** navy left / sand right split; green only on the winning clock.
- **Sound:** two clock ticks panned left and right; the right one speeds up after each mechanism.

---

**Assumptions:** 70–85 s, same voice, numbers only from the article. CUDA `record`/`wait` are shown as labels, with no real code on screen. The end card points to Caching (Ep 5) unless you want to continue with offloading or the decode kernels the source mentions next.
