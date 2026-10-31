"""Voiceover with Kokoro (Apache-2.0), the series' default voice: one wav per script line.

usage: python -I kokoro_vo.py <out_dir> <voice> <speed>     e.g. kok am_michael 0.95
Edit LINES per episode. Pronunciation overrides use Kokoro's [word](/phonemes/) markup;
check a word with KPipeline(lang_code="a").g2p("word")[0]. Runs in seconds on CPU.
"""
import sys, os, numpy as np, soundfile as sf
from kokoro import KPipeline
out, voice, speed = sys.argv[1], sys.argv[2], float(sys.argv[3])
CUDA = "[CUDA](/kˈudə/)"
LINES = [
 "What actually happens after you hit send?",
 "Hi, I'm [Vineeth](/vɪnˈiθ/), a senior AI architect and tech lead. This series is all about AI inference: how models actually run.",
 "Let's follow one prompt. First stop: your app. What you're building shapes every choice after it.",
 "Then the model. Tokens flow through transformer blocks and attention.",
 "Down to the hardware: GPUs like Hopper and Blackwell.",
 f"The software that drives them: {CUDA}, vLLM, and SGLang.",
 "The tricks that make it fast: quantization, speculative decoding, KV caching.",
 "Beyond text: vision, speech, image and video models.",
 "And production: scaling it reliably, at a cost that makes sense.",
 "And back comes your answer.",
 "Next episode, we start at chapter zero: what inference really is. Follow, so you don't miss it.",
]
p = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
os.makedirs(out, exist_ok=True)
for i, t in enumerate(LINES):
    a = np.concatenate([np.asarray(x) for _, _, x in p(t, voice=voice, speed=speed)])
    sf.write(f"{out}/l{i:02d}.wav", a, 24000)
    print(i, round(len(a) / 24000, 2), flush=True)
