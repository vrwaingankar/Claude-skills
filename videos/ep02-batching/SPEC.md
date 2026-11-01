GOAL:    A viewer sees why LLM batching is hard (token by token, lengths vary) and how static → dynamic → continuous batching
         removes idle GPU time; knows offline wants throughput/cost and online wants TTFT/ITL; follows for Ep 3.
STORY:   Mix: A's batch grid (spine) + B's GPU-as-bus hook + C's two clocks (offline / online split).
OUTPUT:  1080 x 1920, 30 fps, 80.1 s (v2: Vinit OK'd up to ~80 s, full script restored); voice is the clock (Kokoro am_michael 1.0, name line 0.95)
LOOK:    series look (sand, navy line art, green only on refilled slots, the picked chip, wins, end-card underline);
         request bars in navy tints, idle cells hatched; grid geometry identical in static and continuous scenes.
SHOTS:   scene starts in vo_layout.json (scene_starts)
NUMBERS: only the notes' 50 vs 500 tokens; "much higher throughput" with no multiple.
BANNED:  series bans + invented numbers.
