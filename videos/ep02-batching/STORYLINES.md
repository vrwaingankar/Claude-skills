# Ep 02 — Batching

Instagram Reel · 1080×1920 · 30 fps · ~60–66 s · Kokoro `am_michael` · series look (sand, navy, one green accent)
Opening (series rule): hook → Vinit's name card → 2–3 s recap of Ep 1 → topic. End card: **Next: Ep 3 — Continuous batching, in depth**.

**The one thing:** LLM requests vary wildly in length, so how you batch them decides how much of the GPU sits idle. Continuous batching refills each slot the moment a request finishes.

**Facts from Vinit's notes** (paraphrased; nothing on screen beyond these):
- Batching groups requests or tokens to raise GPU utilization and throughput and to lower the cost per token.
- Classic models (e.g. ResNet) batch easily. LLMs are autoregressive: they generate token by token and keep past state in the KV cache. Prompt and output lengths vary wildly.
- **Static batching**: a fixed group starts together and waits until all of them finish. A 50-token request waits on a 500-token one, so its GPU share sits idle. Rarely used in production.
- **Dynamic batching**: requests pool as they arrive, up to a max batch size or a short timeout, then run. It trades queue wait against utilization. Good for light traffic.
- **Continuous (in-flight) batching**: it works per token (iteration level), not per request. When a request emits its last token, its slot goes straight to a waiting request. There's no padding waste and no idle GPU. Popularized by vLLM and TGI. The notes say throughput gains can be "orders of magnitude"; on screen this becomes "much higher throughput", with no number.
- **Offline (batch) inference**: big pre-collected datasets (e.g. summarizing millions of support tickets), judged on throughput and cost; per-request latency doesn't matter. **Online serving**: live chat, judged on time to first token (TTFT) and inter-token latency (ITL).

---

## A. One grid, three rules (recommended: one picture a stranger can read in a second, rebuilt three times)
**Device:** the object is the explanation · **Form:** one frame that rebuilds
One grid fills the frame. Rows are batch slots on the GPU and columns are token steps marching left to right. Each request is a coloured bar whose length is its output. Under **static** rules, short bars finish early and their rows turn grey and idle until the longest bar ends. A utilization meter on the side sits low. Under **dynamic** rules, a timer gate holds new requests at the door until it fills or times out. Under **continuous** rules, the moment a bar ends a waiting request snaps into the empty row, the grid stays solid green and the meter pins high. The ending splits the screen into the offline and online clocks.
- **First 2 s:** frame 0 is the grid half grey with one long bar still running and the line "Why is your GPU waiting?". The idle cells blink.
- **Beats:** hook → intro → recap (3 layers, 6 techniques) → why LLMs are different (token by token, lengths vary: 50 vs 500) → static (grey idle rows) → dynamic (timer gate) → continuous (slots refill, vLLM · TGI) → offline vs online split (throughput meter vs TTFT/ITL stopwatches) → end card
- **Look:** series look. Request bars in navy tints, idle cells hatched grey, green only on refilled slots and the end-card underline.
- **Sound:** a soft tick per token column, a dull thud as a row goes idle, a click as each slot refills, whooshes on the dives, a pop on the end card.

## B. The GPU bus
**Device:** a metaphor made literal · **Form:** object-to-object chain
The GPU is a bus with four seats and each request is a rider with a different stop. **Static**: the bus won't leave the last stop until its longest rider gets off, so empty seats ride along. **Dynamic**: the bus departs when full or when the timetable says so. **Continuous**: at every stop a rider gets off and a new one hops straight on. Then the bus flips into the real token grid, so the viewer sees the metaphor was the math.
- **First 2 s:** a bus with three empty seats and one passenger, captioned "Your GPU, most of the time".
- **Beats:** hook → intro → recap → riders = requests, stops = tokens → static bus → dynamic timetable → continuous hop-on → flip to the token grid → offline coach (an overnight run) vs online taxi (TTFT, ITL) → end card
- **Look:** flat navy line art on sand; the bus is drawn like the GPU card from Ep 1, with green only on new riders.
- **Sound:** a bell per stop, door hiss on each refill, the whoosh into the grid, a pop on the end card.

## C. Two clocks (the bold one)
**Device:** a number lands · **Form:** split screen to one
The screen splits from the start. The left half is offline: a mountain of support tickets and a throughput meter. The right half is online: a chat bubble with two stopwatches, TTFT and ITL. Each batching rule plays on both halves at once. Static ruins the chat clocks, dynamic trades one clock for the other, and continuous wins both. The halves merge into one green grid.
- **First 2 s:** two stopwatches already running, labelled "Overnight job" and "Live chat", with the line "Same GPU. Two clocks."
- **Beats:** hook → intro → recap → the two clocks explained → static on both → dynamic on both → continuous on both → merge to one grid → end card
- **Look:** a navy left half and a sand right half, with the series type; green only where a clock wins.
- **Sound:** two ticking clocks panned left and right that slow down or speed up with each rule, a pop on the end card.

---

**Assumptions:** ~60–66 s (you said a few seconds over 60 is fine). Same male voice. The next episode is "Continuous batching, in depth", as your notes say. Numbers shown: only the notes' 50-vs-500-token example; no throughput multiples.
