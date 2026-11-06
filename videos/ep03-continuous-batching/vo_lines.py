CUDA = "[CUDA](/kˈudə/)"
LINES = [
 "Your GPU might be shipping air. Here's where it hides.",
 "Hi, I'm [Vineeth](/vɪnˈiθ/), a senior AI architect and tech lead.",
 "Last time: three ways to batch. Today, how continuous batching really works.",
 "The goal: more tokens per second, from many prompts at once.",
 "The naive batch is a rectangle. Short prompts get padding on the left, and the attention mask hides it.",
 "Prefill once, then decode token by token. When one prompt ends, its slot keeps working for nothing.",
 "Swap in a waiting prompt? It needs prefill while the others decode, so they all get padded.",
 "That's n minus one, times B minus one, pads. Eight prompts, a hundred-token newcomer: six hundred ninety-three.",
 f"{CUDA} graphs and torch compile need fixed shapes, so we pad to the max. More waste.",
 "The fix: drop the batch axis. Put every prompt end to end, in one long row.",
 "The attention mask keeps them apart. That's ragged batching: no padding.",
 "Fill a budget of M tokens: decoding prompts first, one token each, then prefill chunks.",
 "When a prompt finishes, it leaves at once, and the next chunk takes its place.",
 "KV cache, chunked prefill, ragged batching, dynamic scheduling: that's continuous batching.",
 "Next episode: asynchronous batching. Follow so you don't miss it.",
]
