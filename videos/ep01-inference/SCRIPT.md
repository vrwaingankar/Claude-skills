# Ep 01 — Voiceover script (Chapter 0: Inference)

Narrator: Kokoro `am_michael`, speed 1.0. `CUDA` is written `[CUDA](/kˈudə/)` in the TTS line. Source: Vinit's notes on inference (paraphrased).

| # | Line | On screen |
| --- | --- | --- |
| 0 | You've got the weights. You've got a GPU. Is that inference? | Weights + GPU = inference? |
| 1 | Hi, I'm Vinit ("Vineeth"), a senior AI architect and tech lead. | Name card (as ep00) |
| 2 | Last time: one prompt, from your app to the GPU and back. Today, chapter zero. | Previously · Ep 0: the prompt's route |
| 3 | A model has two lives. Training learns the weights. Inference serves them. | Split: Training / Inference |
| 4 | Classic ML was easy to serve: a small model on a cheap CPU. | Classic ML · tree on a CPU, gauge green |
| 5 | Generative AI isn't. On a GPU, tokens crawl while requests pile up. | Generative AI · stall, queue, gauge red |
| 6 | It takes three layers. The runtime: one model, one GPU, full speed. | Layer 1 · Runtime |
| 7 | Infrastructure: scale across regions and clouds, and stay up. | Layer 2 · Infrastructure |
| 8 | Tooling: the right controls for the engineers. | Layer 3 · Tooling |
| 9 | Together, the same request streams. | Together · stream flows |
| 10 | Inside the runtime: CUDA, PyTorch, and engines like vLLM, SGLang and TensorRT LLM. | Runtime stack (+ FlashAttention on screen) |
| 11 | Plus six techniques: batching, caching, quantization, speculation, parallelism, disaggregation. | Six dials |
| 12 | Each gets its own episode, starting with batching. Follow so you don't miss it. | Next: Ep 2 · Batching |
