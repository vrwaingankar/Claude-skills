# Ep 01 — Voiceover script (Chapter 0: Inference)

Narrator: Kokoro `am_michael`, speed 1.0. `CUDA` is written `[CUDA](/kˈudə/)` in the TTS line. Source: Vinit's notes on inference (paraphrased).

| # | Line | On screen |
| --- | --- | --- |
| 0 | You've got the weights. You've got a GPU. Is that inference? | Weights + GPU = inference? |
| 1 | A model has two lives. Training learns the weights. Inference serves them. | Split: Training / Inference |
| 2 | Classic ML was easy to serve: a small model on a cheap CPU. | Classic ML · tree on a CPU, gauge green |
| 3 | Generative AI isn't. Put the weights on a GPU, and tokens crawl while requests pile up. | Generative AI · stall, queue, gauge red |
| 4 | It takes three layers. The runtime: one model on one GPU, as fast as it goes. | Layer 1 · Runtime |
| 5 | Infrastructure: scale across regions and clouds, and stay up. | Layer 2 · Infrastructure |
| 6 | Tooling: the right controls for the engineers. | Layer 3 · Tooling |
| 7 | Together, the same request streams. | Together · stream flows |
| 8 | Inside the runtime: CUDA, PyTorch, engines like vLLM, SGLang and TensorRT LLM, and kernels like FlashAttention. | Runtime stack |
| 9 | Plus six techniques: batching, caching, quantization, speculation, parallelism, disaggregation. | Six dials |
| 10 | Each gets its own episode. Next up: batching. Follow so you don't miss it. | Next: Ep 2 · Batching |
