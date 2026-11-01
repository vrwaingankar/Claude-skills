LINES = [
 "Your GPU is probably sitting idle. Here's why.",
 "Hi, I'm [Vineeth](/vɪnˈiθ/), a senior AI architect and tech lead.",
 "Last time: three layers and six techniques. Today, the first one: batching.",
 "Batching groups requests, so each GPU step does more work, and tokens cost less.",
 "But LLMs write token by token, with a KV cache, and lengths vary: fifty tokens here, five hundred there.",
 "Static batching waits for the longest request. Short ones finish, and their slots sit idle.",
 "Dynamic batching starts when the batch fills, or a timer runs out. Better, but still waiting.",
 "Continuous batching works token by token. When one request finishes, a new one takes its slot.",
 "No idle slots, much higher throughput. vLLM and TGI made it popular.",
 "Offline jobs, like millions of support tickets, want throughput and low cost.",
 "Live chat wants speed: time to first token, and the gap between tokens.",
 "Next episode: continuous batching, in depth. Follow so you don't miss it.",
]
