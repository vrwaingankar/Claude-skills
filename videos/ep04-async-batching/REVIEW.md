# Review — ep04 Asynchronous batching

84.6 s. Story mix: A's CPU/GPU timeline (spine), B's kitchen (hook), C's two stopwatches (result).
All 15 VO lines verified on their own transcripts; "CUDA graph" was heard as "coup de grâce", so line 10 says
"captured graph" and the screen says CUDA graphs. Numbers only from the article: 300.6 s, 24% idle, ~228 s, 76.0% → 99.4%,
234.5 s, 22% (ceiling 24%), 8B model, batch 32, 8K tokens, 16K+ tokens. Check clean (0 findings), mix ≈ −16 LUFS.
Fixed during review: growing blocks squashed their labels (scaleX → clip reveal), late labels moved earlier, a 3 s still in the
result scene got a meter pulse, recap title overflow, graph dots over their labels, carry-over arrow position.
Build: `python gen_scenes.py .` then `python build_index.py vo_layout.json`.
