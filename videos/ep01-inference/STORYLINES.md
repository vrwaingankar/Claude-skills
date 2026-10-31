# Ep 01 — Chapter 0: Inference

Instagram Reel · 1080×1920 · 30 fps · 55–60 s · Kokoro `am_michael` narration · series look from ep00 (sand, navy, one green accent)

**The one thing:** generative AI inference is hard: weights plus GPUs is not enough. You need three layers (runtime, infrastructure, tooling), and the runtime runs on six techniques the series covers next.

**Facts from Vinit's source** (paraphrased; no on-screen claim beyond these):
- A model has two phases: training learns the weights from data; inference serves the model in production.
- Classic ML inference was simple: an XGBoost-style model on a lightweight CPU with a simple stack.
- GenAI inference is complex. Taking the weights and some GPUs does not make it fast or reliable at scale.
- There are three layers. **Runtime**: one model on one GPU-backed instance, as fast and efficient as possible. **Infrastructure**: scaling across clusters, regions and clouds without silos, with high uptime. **Tooling**: the right abstraction for engineers, balancing control and productivity. The three must work together.
- The runtime's software stack: CUDA → PyTorch → engines (vLLM, SGLang, TensorRT-LLM). Kernels like FlashAttention bring big gains.
- Six runtime techniques: **batching** (weave requests token by token for throughput), **caching** (reuse the KV cache across shared prefixes), **quantization** (lower precision for more compute and less memory), **speculation** (draft and verify tokens, more than one per forward pass), **parallelism** (several GPUs without new bottlenecks), **disaggregation** (prefill and decode on separately scaling workers).
- Each technique gets its own episode next.

---

## A. Weights aren't enough (recommended: the failure-then-fix arc is the one a stranger remembers)
**Device:** life before and after · **Form:** one frame that rebuilds
A model file and a GPU are dropped on the floor with the label "ship it". A request comes in, the token stream stutters, and a queue piles up. Then the frame rebuilds itself into the full inference stack: the runtime snaps around the GPU, infrastructure multiplies it across regions, tooling caps it with an engineer's console. The same request now streams smoothly. Finally the camera dives into the runtime layer, where six technique tiles light up one by one as a preview of the series.
- **First 2 s:** frame 0 shows a model-weights file and one GPU card with the line "Weights + GPUs = inference?". The "?" turns green as the first request arrives.
- **Beats:** hook (weights + GPU) → 2 phases in one line (training → inference) → classic ML: XGBoost on a small CPU, instant → GenAI: same move, it stalls → stack builds: runtime → infrastructure → tooling → the request flows → dive into runtime: CUDA → PyTorch → vLLM / SGLang / TRT-LLM, FlashAttention flash → six techniques light up → end card "Next: Ep 2 — Batching" + follow
- **Look:** ep00 sand + navy line art; the stack is one flat blueprint elevation that grows upward; green only on the request's path and the end-card underline.
- **Sound:** a low stutter/glitch tick while the request stalls, a solid thud as each layer locks in, a whoosh on the dive, the pop on the end card; voice on top.

## B. Two lives of a model
**Device:** the object is the explanation · **Form:** split screen to one, then an endless zoom (continues ep00's camera)
The screen splits. The top half is training: data pours in and a loss curve falls into a weights file. The bottom half is inference: the same weights answer a prompt. Training fades out because the series lives in the bottom half. Then a second split: classic ML (a tiny XGBoost tree on a CPU, answering instantly) against GenAI (a huge weights file on a GPU rack). The GenAI side swallows the frame, and the camera zooms through the three layers and into the runtime, ending on the six techniques.
- **First 2 s:** a model card cut in half. Top half labelled "Training", bottom half "Inference". The bottom half glows green: "This series lives here."
- **Beats:** split: training / inference → collapse to inference → split: classic ML / GenAI → GenAI takes over → zoom: infrastructure (map of regions) → runtime (one GPU instance) → software stack → six techniques ring → end card
- **Look:** ep00 look; split panes are two full-bleed worlds (training in a cooler navy, inference on sand), never floating cards.
- **Sound:** a soft tick on each split, a whoosh on each zoom (ep00 takes), a riser into the six techniques, the pop on the end card.

## C. Turn the dials (the bold one)
**Device:** a number lands · **Form:** one frame that never cuts
One live gauge fills the top of the frame: tokens per second for a single chat stream (numbers marked illustrative). Below it is a control board with three layer switches (runtime, infrastructure, tooling) and six technique dials. The narration flips each switch and turns each dial, and the gauge answers every move: batching widens the stream into many, caching skips a chunk, quantization shrinks the weights block, speculation makes tokens arrive in pairs, parallelism splits across two GPUs, disaggregation splits prefill and decode into two lanes. It feels like tuning an engine.
- **First 2 s:** the gauge needle sits in red at a crawl, with the line "Your model is ready. It's slow." The first switch is already under the cursor.
- **Beats:** slow gauge → "training made it, inference serves it" → classic ML needle at max on a CPU (for contrast) → GenAI needle in red → 3 switches on (needle climbs, uptime light, console) → 6 dials, one per technique, each with its own visual on the stream → needle green → end card
- **Look:** ep00 sand ground; the board is navy line art with big dial numbers; green only on the needle zone and the end card.
- **Sound:** a mechanical click for each switch, a ratchet tick per dial, a rising hum under the gauge, the pop on the end card.

---

**Assumptions:** 55–60 s; voice is Kokoro `am_michael` (free); no music, SFX from ep00. The next episode is **Ep 2 — Batching**, the first technique on the list. Classic-ML wording stays neutral (no first-person Baseten anecdote) since it's Vinit's channel.
