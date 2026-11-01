GOAL:    A viewer sees why LLM batching is hard (token by token, lengths vary) and how static → dynamic → continuous batching
         removes idle GPU time; knows offline wants throughput/cost and online wants TTFT/ITL; follows for Ep 3.
STORY:   Mix: A's batch grid (spine) + B's GPU-as-bus hook + C's two clocks (offline / online split).
OUTPUT:  1080 x 1920, 30 fps, 67.1 s; voice is the clock (Kokoro am_michael 1.0, name line 0.95)
LOOK:    series look (sand, navy line art, green only on refilled slots, the picked chip, wins, end-card underline);
         request bars in navy tints, idle cells hatched; grid geometry identical in static and continuous scenes.
SHOTS:   hook 0 · intro 3.77 · recap 7.77 · batch 12.93 · tokens 18.77 · static 26.27 · dynamic 32.4 · cont 38.4 ·
         thru 45.03 · offline 50.73 · online 55.87 (same split frame) · next 61.07
NUMBERS: only the notes' 50 vs 500 tokens; "much higher throughput" with no multiple.
BANNED:  series bans + invented numbers.
