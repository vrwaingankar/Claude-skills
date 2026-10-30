"""Clone a voice with Chatterbox (MIT) on CPU: one wav per job line.

usage: python -I clone_voice.py <ref.wav> <out_dir> <jobs.txt>
  jobs.txt lines: name|seed|cfg_weight|exaggeration|text
  Vinit's chosen setting ("C"): cfg_weight 0.3, exaggeration 0.6, pause-free reference.
"""
import sys, os, torch, torchaudio as ta
from chatterbox.tts import ChatterboxTTS
ref, out = sys.argv[1], sys.argv[2]
jobs = [l.split("|") for l in open(sys.argv[3]).read().strip().split("\n")]  # name|seed|cfg|exag|text
model = ChatterboxTTS.from_pretrained(device="cpu")
os.makedirs(out, exist_ok=True)
last = None
for name, seed, cfg, ex, text in jobs:
    if last != ex:
        model.prepare_conditionals(ref, exaggeration=float(ex)); last = ex
    torch.manual_seed(int(seed))
    wav = model.generate(text, exaggeration=float(ex), cfg_weight=float(cfg), temperature=0.7)
    ta.save(f"{out}/{name}.wav", wav, model.sr)
    print("done", name, round(wav.shape[-1] / model.sr, 2), flush=True)
