LINES = [
 "Your GPU is probably sitting idle. Here's why.",
 "Hi, I'm [Vineeth](/vɪnˈiθ/), a senior AI architect and tech lead.",
 "Last time: three layers, and six techniques inside the runtime. Today, the first one: batching.",
 "Batching groups requests together, so every GPU step does more work, and each token costs less.",
 "But LLMs write one token at a time, keeping the past in a KV cache. And lengths vary wildly: fifty tokens here, five hundred there.",
 "Static batching starts a group together, and waits for the longest. Short requests finish, and their slots sit idle.",
 "Dynamic batching fills a batch as requests arrive, until it's full or a timer runs out. Better, but still waiting.",
 "Continuous batching works token by token. The moment one request finishes, a waiting one takes its slot.",
 "No idle slots, no padding, much higher throughput. Engines like vLLM and TGI made it popular.",
 "Which one wins depends on your clock. Offline jobs, like millions of support tickets, want throughput and low cost.",
 "Live chat wants speed: time to first token, and the gap between tokens.",
 "Next episode: continuous batching, in depth. Follow so you don't miss it.",
]
