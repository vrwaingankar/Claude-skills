# Review — ep02 Batching

v2 80.1 s (full first-draft script: "keeping the past in a KV cache", "no padding", "which one wins depends on your clock"), all beats re-synced; check clean (0 findings), mix ≈ −16 LUFS. All 12 VO lines verified against their own transcripts
(whisper spells "KV cache" as "KV cash" and "lengths" as "links": sound is right).
Review frames: hook bus with idle seats on frame 0; name card; Ep 1 recap with the Batching chip lit; requests packed into one
batch; token row + KV cache + 50/500 bars; static grid going idle (GPU busy meter drops); dynamic timer gate; continuous grid
refilled from the queue (meter full); throughput gauge + vLLM/TGI; offline/online split with two stopwatches; Ep 3 end card.
Fixed during review: requests overlapped the GPU after packing, chat tokens were positioned outside their bubble,
a silent SFX file (error.mp3 starts with 0.6 s of silence) swapped for glitch-1.
Build: `python gen_scenes.py .` then `python build_index.py vo_layout.json`.
