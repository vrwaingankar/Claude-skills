CUDA = "[CUDA](/kˈudə/)"
LINES = [
 "Your GPU spends almost a quarter of its time waiting for your CPU.",
 "Hi, I'm [Vineeth](/vɪnˈiθ/), a senior AI architect and tech lead.",
 "Last time: continuous batching. Today, we make it asynchronous.",
 "The loop is synchronous: the GPU computes while the CPU waits, then the CPU preps while the GPU waits.",
 "In one profile: three hundred seconds, and the GPU sat idle for twenty-four percent of it.",
 "The fix: prep batch N plus one on the CPU, while the GPU runs batch N.",
 f"{CUDA} streams split the work: inputs in, compute, outputs out.",
 "Launch them freely, and results come back instantly, and wrong.",
 f"{CUDA} events fix the order, and the CPU blocks only once per step.",
 "Two input slots, A and B, take turns, so the CPU never overwrites what the GPU is reading.",
 "Each slot gets its own captured graph, in one shared memory pool.",
 "And tokens batch N hasn't made yet? A zero placeholder, then a carry-over mask swaps in the real one, on the GPU.",
 "The result: the GPU is busy ninety-nine point four percent of the time, up from seventy-six. Twenty-two percent faster.",
 "It ships in Hugging Face transformers, built for long generations.",
 "Next episode: caching. Follow so you don't miss it.",
]
