# Ep 03 — Continuous batching, in depth

Instagram Reel · 1080×1920 · 30 fps · 60–80 s · Kokoro `am_michael` · series look
Opening (series rule): hook → Vinit's name card → 2–3 s recap of Ep 2 → topic. End card: **Next: Ep 4 — Asynchronous batching**.

**The one thing:** padding is the enemy. Continuous batching drops the batch axis, packs prompts into one ragged row that the attention mask keeps apart, and refills it every step.

**Facts from Vinit's notes** (paraphrased; nothing on screen beyond these):
- Throughput means tokens generated per second. To raise it, generate for several prompts in parallel.
- Naive batching adds a batch axis to the token and attention-mask tensors. Tensors must be rectangular, so every prompt is left-padded to the same length and the mask hides the pads.
- Batched generation is one prefill step, then decode steps. When one prompt emits `<eos>`, every later token for it is wasted until the longest prompt finishes.
- **Dynamic scheduling** swaps a finished prompt for a waiting one. But the newcomer needs prefill while the others decode one token at a time, so it costs almost as much padding as its own length: **(n−1)(B−1)** pad tokens. With **B = 8 and n = 100**, that's **693**. The cost grows with both batch size and prompt length.
- CUDA graphs and torch.compile need static shapes, which forces padding to a fixed maximum length and wastes even more.
- **Ragged batching** removes the batch axis and concatenates the prompts into one sequence. The attention mask (a boolean mask) stops tokens of one prompt from attending to another. There's no padding; the only limit is **m**, the tokens per batch that GPU memory allows.
- **The scheduler:** fill the budget m. Add every decoding prompt first, at 1 token each, then fill the rest with prefill using **chunked prefill** to split long prompts. Remove finished prompts at once and slot in new chunks.
- **Continuous batching** = KV cache + chunked prefill + ragged batching with dynamic scheduling. It's the technique behind modern LLM serving.
- Next in the notes: **asynchronous batching**.

---

## A. Kill the padding (recommended: one picture, the waste visibly disappears)
**Device:** the object is the explanation · **Form:** one frame that rebuilds
One token grid stays on screen the whole time, and padding cells are painted red as waste.
1. Four prompts are left-padded into a rectangle. One hits `<eos>` and its row keeps generating useless tokens.
2. Dynamic scheduling swaps in a new prompt, and a red wall of padding floods in while a counter runs (n−1)(B−1) → **693**.
3. The camera pulls back: the rectangle cracks, and its rows slide end to end into one long ragged row with no red at all. Beside it, the attention mask appears as block-diagonal tiles that keep each prompt to itself.
4. The row becomes a budget bar of m tokens. Decode tokens drop in first, one per prompt, and prefill chunks fill the rest. A finished prompt leaves, a new chunk takes its place, and the bar stays full.
- **First 2 s:** frame 0 is a token grid half red, with the line "Most of this batch is padding."
- **Beats:** hook → intro → recap (static / dynamic / continuous) → throughput = tokens/s → rectangle + left padding → `<eos>` waste → dynamic swap → 693 → CUDA graphs force max length → crack into one ragged row → attention mask → budget m: decodes first, prefill chunks fill → continuous = 3 parts → end card
- **Look:** series sand and navy; prompts in four navy tints; padding in red #D9442B, the only red; green only for the full budget bar and the end card.
- **Sound:** a soft tick per token, a low buzz under the red padding, a glass crack as the batch axis breaks, a click per chunk landing, a pop on the end card.

## B. Pack the truck
**Device:** a metaphor made literal · **Form:** object-to-object chain
The GPU is a truck with room for m tokens. The old way ships prompts in identical crates, the biggest crate size for everything, so most of each crate is foam padding. A crate that empties early still rides the whole trip. Swapping in a new crate means a pile of extra foam (693 pieces for 8 crates of a 100-token prompt). The new way throws the crates out: prompts are packed loose, end to end, with thin dividers (the attention mask) between them. At every stop, finished cargo leaves and the gap is filled with the next prompt, split into chunks if it's long.
- **First 2 s:** a truck bed full of crates that are mostly foam, with the line "You're shipping air."
- **Beats:** hook → intro → recap → crates = padded batch → early `<eos>` crate rides empty → swap → foam pile 693 → fixed-size crates (CUDA graphs) → crates gone, loose packing + dividers → refill at each stop, chunks → the truck becomes the token row → end card
- **Look:** flat navy line art; foam in red hatch; the truck drawn like the GPU card from the series.
- **Sound:** a cardboard thud per crate, foam rustle, a latch click per divider, a pop on the end card.

## C. The mask is the trick (the bold one)
**Device:** a number lands · **Form:** an endless zoom
The attention mask, a big grid of on/off squares, is the hero. We zoom into the padded batch's masks, which are mostly off and red at the edges, and the number 693 lands. Then we zoom out to the one trick: a single block-diagonal mask over one long row of tokens, with prompts side by side and no padding. The zoom continues into the scheduler, where the mask redraws every step as prompts come and go.
- **First 2 s:** a huge mask matrix fills the frame, with the line "This grid is why LLM serving scales."
- **Beats:** hook → intro → recap → masks of the padded batch → 693 → zoom out: block-diagonal mask → scheduler redraws it each step → 3 parts → end card
- **Look:** mask cells in navy and white with green only where attention is allowed; red for padding.
- **Sound:** a tick on each mask redraw, a riser into 693, a pop on the end card.

---

**Assumptions:** 60–80 s, same male voice. Numbers on screen come only from the notes: (n−1)(B−1), B = 8, n = 100, 693. "ChatGPT can handle thousands of users" is not stated as fact; it becomes "the technique behind modern LLM serving". The next episode is asynchronous batching, as the notes say.
