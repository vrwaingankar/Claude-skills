# Review — ep03 Continuous batching, in depth

82.7 s (Vinit: 80–85 s fine, cover every concept). Story mix: A's token grid (spine), B's "shipping air" truck (hook),
C's block-diagonal attention mask (reveal). All 15 VO lines verified on their own transcripts (whisper hears "prefill" as
"refill"/"pre-filled"; sound is right). Numbers only from the notes: (n−1)(B−1), B=8, n=100, 693; the 18 in the swap
scene is the same formula on the 4×8 picture (n=7, B=4). "ChatGPT handles thousands of users" not stated.
Check: clean except one false hold warning (budget label carries into the refill scene). Mix ≈ −16 LUFS.
Fixed during review: label ids "decode-w"/"shapes-w" collided with the scene wrappers (the label's clip reveal hid the whole
scene); wasted cells showed early because a later fromTo re-rendered their start state; late labels moved earlier.
Build: `python gen_scenes.py .` then `python build_index.py vo_layout.json`.
