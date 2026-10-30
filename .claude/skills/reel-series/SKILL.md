---
name: reel-series
description: Lessons and scripts from making Vinit's AI-inference Instagram Reel series (ep00 onward) with HyperFrames - his cloned voiceover (Chatterbox), pronunciations, retiming scenes to the voice, sound levels, this cloud environment's network quirks, and the delivery checklist. Read it before starting or changing any episode in videos/, and before any voiceover work for Vinit.
---

# Vinit's reel series: what ep00 taught us

Read `/hyperframes` first for the render contract; this file holds only what is specific to this series and this environment. Add to it whenever an episode teaches something new.

## The series
- Instagram Reel, 1080×1920, 30 fps, **55–60 s**. One folder per episode: `videos/epNN-<slug>/` with STORYLINES.md → SPEC.md → SCRIPT.md, then index.html + `compositions/` (one scene per script line).
- Look carried over from ep00 (keep it unless Vinit asks): sand ground #E6D8BF with a 4% navy grid, ink navy #14213D, one green accent #00C46A, Inter 900 titles at x=90, engineering line art, the endless zoom through a green dot at (540,760). Handle on the end card: **@vr_waingankar**. Photo: `videos/ep00-series-intro/assets/vinit.jpg`.
- Vinit follows on his iPhone: keep replies short, send files with SendUserFile, and send A/B samples when a choice is his to make (he picked the voice from three samples).

## Environment gotchas (cloud session)
- **GSAP**: the jsdelivr CDN is blocked. Copy the vendored `assets/vendor/gsap.min.js` from ep00.
- **Hugging Face**: huggingface.co resolves, but weights come from `*.hf.co` CDNs (`cas-server.xethub.hf.co`, `us.aws.cdn.hf.co`), which must be in the environment's allowed domains. If downloads 403, tell Vinit to add `*.hf.co` (environment settings → Network access) and stop.
- **PyTorch CPU index** (download.pytorch.org) is blocked: install from plain PyPI (`uv pip install chatterbox-tts`; it pulls the CUDA wheel, which still runs on CPU, ~3 GB).
- `pip install git+https://github.com/...` is refused by the permission classifier. Use PyPI packages only. `melotts` on PyPI is broken (sdist missing requirements.txt).
- Chatterbox imports `perth`, which needs `pkg_resources`: `uv pip install "setuptools<81"`, or the watermarker is None and loading fails.
- `npx hyperframes transcribe` can't fetch its whisper model (node can't reach the HF CDN). Fetch it in Python and copy it in:
  `hf_hub_download('ggerganov/whisper.cpp', 'ggml-small.en.bin')` → `~/.cache/hyperframes/whisper/models/`.
- Use Python 3.11 venvs in the scratchpad (`uv venv -p 3.11`); run scripts with `python -I`.
- Background "wait then run" loops: never `pgrep -f "<pattern>"` with a pattern that also appears in the waiting command itself. It matches itself and waits forever (cost us ~20 min). Wait on a PID or an output file instead, or just run jobs one after another.

## Voiceover: Vinit's cloned voice
**Privacy**: the raw voice sample is never committed and never leaves the scratchpad. The generated `assets/vo.m4a` is fine to commit. Use the sample only for tone, never its words.

1. **Reference**: trim to the speech (his ep00 sample: speech ran 10.6–38 s of a 39 s m4a; the start was near-silent), mono 24 kHz, `highpass=f=70,loudnorm=I=-18:TP=-2`, then remove pauses so Chatterbox's ~6–10 s conditioning window is all speech:
   `silenceremove=stop_periods=-1:stop_duration=0.15:stop_threshold=-40dB:stop_silence=0.12`.
2. **Settings Vinit chose ("C")**: `cfg_weight=0.3, exaggeration=0.6, temperature=0.7` (faster and more expressive). The defaults (0.5/0.5) were slower; 0.8/0.3 was slow and flat. The accent tends toward American; that is a model limit, and setting C was the best available.
3. **Write the script for the ear**, not the screen (TTS text only; on-screen text stays correct):
   | Say | Write in the TTS line |
   | --- | --- |
   | Vinit (his name) | `Vineet` |
   | vLLM | `vee-ell-ell-em` |
   | SGLang (S-G-Lang, never "S-ghi-lang") | `ess-jee-lang` |
   | KV cache | `K V caching` |
   | What you're | `What you are` (contraction got slurred) |
   "ess gee lang" was read as "S-ghi-lang"; "V L L M, S G Lang" was slow and garbled. Add new terms here as they come up.
4. **One clip per script line** (`scripts/clone_voice.py`, jobs file `name|seed|cfg|exag|text`). CPU speed is ~1.5–2 min per line, so 11 lines take ~20 min: run in the background and tell Vinit the ETA.
5. **Verify every line**: transcribe each clip on its own and compare with the script. Retake any slip with another seed (seeds 7 and 11 both worked). ep00 slips: "Pokins" (Tokens), "work your building", "influence" (inference), "Blackwidth". Make 2–4 takes of the hardest lines (acronyms, names) and keep the cleanest; send Vinit the takes when it's his ear that decides.
6. **Assemble** (`scripts/build_vo.py`): trim each clip's edge silence
   (`silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,` same again`,areverse`), apply up to 1.04× `atempo` to land in 55–60 s, join with pauses (0.3 s normal; ~0.8–1.1 s after the hook, after dense lines and before the payoff), then `loudnorm=I=-16:TP=-1.5:LRA=9` → AAC 192k `assets/vo.m4a`.

## Retime the film to the voice
- The voice is the clock. `scripts/retime_to_vo.py <project> <layout.json>` sets each scene to start **0.15 s before its line** (frame-snapped), the root duration to the VO length, each camera exit at duration − 0.5 s, and the dot's travel to finish before the exit. It also moves the SFX and adds the `<audio id="vo">`. It can be re-run after VO changes.
- **Word-synced beats are manual.** Take word times from **per-line** transcripts plus the layout's line starts. The whole-file transcript drifts ±0.5 s. Beat at scene time = word time in clip + (line start − scene start ≈ 0.14 s). ep00 synced beats: GPU names highlight on "Hopper"/"Blackwell"; software stack layers drop on "CUDA", "vLLM", "SGLang" (function stagger `(i) => [...][i]`); end-card follow line on "Follow"; the "chapter 0" subline on "chapter zero".
- A line that is long relative to its visuals leaves dead air: add a beat (ep00 added a small scale punch on "Inference"), or lengthen the pause instead of stretching the line.

## Craft rules `hyperframes check` enforced on ep00
- Text must stay on screen at least **0.5 s + 0.3 s per word** (5 words → 2.0 s, 7 → 2.6 s). The hook's input text and the answer bubble both tripped it: start text earlier or give the scene more room in the VO.
- Nothing may stay still for more than **3 s**: add a beat or use `data-hold` deliberately.
- Short layer drops passing over a title raise only an info-level overlap note; that's fine.

## Sound under voice
Whooshes 0.2 (three takes rotated, one per dive, 0.35 s before each cut), send click 0.4, riser 0.22 into impact 0.35 on the answer, end-card pop 0.3, VO 1.0. Final mix measured ≈ −16 LUFS. No music source is available in this environment.

## Delivery checklist
1. `npx hyperframes@<pinned> check --json`: 0 errors, and weigh each warning.
2. `snapshot --review` and look at both beat sheets (thumbnail, name card, every chapter mid-frame, answer, end card); update `REVIEW.md`.
3. `render -q delivery -o renders/epNN-final.mp4` (~2 min for 60 s), then ffprobe the duration and size.
4. SendUserFile the MP4 to Vinit, mentioning anything to listen for (names, acronyms).
5. Commit (VO, transcript, compositions, index, REVIEW.md, render; never the raw sample) and `git push -u origin master`.
