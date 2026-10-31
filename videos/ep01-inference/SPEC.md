GOAL:    A viewer learns why GenAI inference is hard, the three layers that fix it (runtime, infrastructure, tooling),
         and what the runtime runs on, and follows for Ep 2 (Batching).
STORY:   Mix: A "Weights aren't enough" spine; B's split screens (training/inference, classic ML/GenAI); C's gauge and six dials.
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps, Instagram Reel, 59.2 s; voice is the clock (Kokoro am_michael, 1.0x)
LOOK:    ep00 series look: sand #E6D8BF + 4% navy 60 px grid; ink navy #14213D; panel #F3EBDD, 4 px navy strokes, radius 18,
         shadow 0 10 0 rgba(20,33,61,.12); accent green #00C46A only on the request's path, the gauge's good zone, one word per shot,
         the Ep 2 underline; stall red #D9442B only on the stalled gauge and the queue. Inter 900 titles 128 px at x=90.
         Every word inside the 168–1330 px band.
OBJECTS: a weights file (grid of numbers), a GPU card, a gauge (response speed, no numbers), a small decision tree on a CPU chip,
         a token stream, a request queue, the inference stack (runtime box around the GPU, instances across cluster/region/cloud,
         a tooling console on top), the runtime software stack, six dials.
MOTION:  enter expo.out 15 f; move power3.inOut; dive out power2.in 15 f; drops back.out(1.6); layer locks back.out(1.4) + thud.
         Scenes 0–3 and 8–10 dive (ep00 zoom). Scenes 4–7 are ONE frame that rebuilds: identical positions, hard match cuts.
SHOTS:   0 hook 0–4.27   weights + GPU + "= inference?" on frame 0; "?" turns green on "inference"
         1 phases 4.27   split: Training (navy, data → weights) / Inference (sand, weights → answer); training dims
         2 classic 9.10  tiny tree on a CPU, request in → answer out at once, gauge needle green
         3 stall 14.0    big weights block on GPU, tokens stutter (glitch), queue piles, needle drops to red
         4 runtime 20.9  stack frame: runtime box locks around the GPU, needle rises
         5 infra 27.2    the instance copies across Cluster / Region / Cloud, uptime light green
         6 tooling 31.3  console locks on top
         7 flow 34.33    request runs through all layers, token stream flows, needle green
         8 stack 36.73   dive into the runtime: CUDA → PyTorch → vLLM | SGLang | TensorRT-LLM, FlashAttention bolt
         9 dials 46.43   six dials turn to green one per word
         10 next 53.5    "Next episode / Ep 2 / Batching", follow line on "follow"
SOUND:   VO 1.0; whoosh 0.2 on dives; glitch 0.25 on the stall; thud (impact-bass-2) 0.3 per layer lock; click-soft 0.3 per dial;
         ping 0.25 on uptime; riser 0.2 → impact 0.3 on "streams"; pop 0.3 on the end card. No music.
BANNED:  spec.md defaults, plus: pill chips, monospace caps labels, centred layouts, fade+slide-up entrances, glow, three cards in a row,
         invented numbers (the gauge has no numbers), first-person Baseten anecdotes.
