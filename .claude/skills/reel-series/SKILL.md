---
name: reel-series
description: Lessons and scripts from making Vinit's AI-inference Instagram Reel series (ep00 onward) with HyperFrames - the narrator voice (stock Kokoro male, not his cloned voice), pronunciations, retiming scenes to the voice, sound levels, this cloud environment's network quirks, and the delivery checklist. Read it before starting or changing any episode in videos/, and before any voiceover work for Vinit.
---

# Vinit's reel series: what ep00 taught us

Read `/hyperframes` first for the render contract; this file holds only what is specific to this series and this environment. Add to it whenever an episode teaches something new.

## The series
- Instagram Reel, 1080×1920, 30 fps, **55–60 s**. One folder per episode: `videos/epNN-<slug>/` with STORYLINES.md → SPEC.md → SCRIPT.md, then index.html + `compositions/` (one scene per script line).
- Look carried over from ep00 (keep it unless Vinit asks): sand ground #E6D8BF with a 4% navy grid, ink navy #14213D, one green accent #00C46A, Inter 900 titles at x=90, engineering line art, the endless zoom through a green dot at (540,760). Handle on the end card: **@vr_waingankar**. Photo: `videos/ep00-series-intro/assets/vinit.jpg`.
- Vinit is a **Senior AI Architect and Tech Lead** (name card: "Sr AI Architect · Tech Lead"). His name is spelled **Vinit** on screen but said **"Vineeth"** (vi-NEETH).
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

## Voiceover: stock male narrator (decided after ep00)
**Don't clone Vinit's voice.** He tried it (Chatterbox, several settings) and it didn't sound good; he asked for a default male voice.
Use **Kokoro** (Apache-2.0, PyPI `kokoro>=0.9.4`, weights `hexgrad/Kokoro-82M`), voice **`am_michael`**, speed **0.95** (`scripts/kokoro_vo.py`). It runs in seconds on CPU, and the shared `en_core_web_sm` download works.

1. **Pronunciation overrides** (Kokoro markup `[word](/phonemes/)`; check with `KPipeline(lang_code="a").g2p("word")[0]`):
   | Word | In the TTS line | Why |
   | --- | --- | --- |
   | Vinit | `[Vineeth](/vɪnˈiθ/)` | plain "Vineeth" is stressed VIN-eeth; he wants vi-NEETH |
   | CUDA | `[CUDA](/kˈudə/)` | otherwise spelled out C-U-D-A |
   | vLLM, SGLang, KV, Hopper, Blackwell, quantization | write as-is | Kokoro gets these right (SGLang → S-G-Lang) |
   Add new terms here as episodes need them.
2. **Verify every line**: transcribe each clip on its own and compare with the script. All 11 ep00 lines were clean first time (whisper writes the name as "Veneeth", which is right).
3. **Length**: Kokoro at 1.0 ran 48 s for the ep00 script. Speed 0.95 plus 0.45 s pauses (1.0 after the hook, 0.9 after a dense line, 0.8–1.1 before the payoff and the end card) landed at 58 s.
4. **Assemble** (`scripts/build_vo.py`): trim each clip's edge silence
   (`silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,` same again`,areverse`), join with pauses, then `loudnorm=I=-16:TP=-1.5:LRA=9` → AAC 192k `assets/vo.m4a`.

### If voice cloning ever comes back (history from ep00)
Chatterbox (MIT) via `scripts/clone_voice.py`: the raw sample is never committed and is used for tone only; use a pause-free reference; Vinit preferred `cfg_weight=0.3, exaggeration=0.6`. Chatterbox misreads acronyms (spell them out: `vee-ell-ell-em`, `ess-jee-lang`), slurs contractions, drifts to an American accent, and needs 1.5–2 min per line on CPU with retakes.

## Retime the film to the voice
- The voice is the clock. `scripts/retime_to_vo.py <project> <layout.json>` sets each scene to start **0.15 s before its line** (frame-snapped), the root duration to the VO length, each camera exit at duration − 0.5 s, and the dot's travel to finish before the exit. It also moves the SFX and adds the `<audio id="vo">`. It can be re-run after VO changes.
- **Word-synced beats are manual.** Take word times from **per-line** transcripts plus the layout's line starts. The whole-file transcript drifts ±0.5 s. Beat at scene time = word time in clip + (line start − scene start ≈ 0.14 s). ep00 synced beats: GPU names highlight on "Hopper"/"Blackwell"; software stack layers drop on "CUDA", "vLLM", "SGLang" (function stagger `(i) => [...][i]`); end-card follow line on "Follow"; the "chapter 0" subline on "chapter zero".
- A line that is long relative to its visuals leaves dead air: add a beat (ep00 added a small scale punch on "Inference"), or lengthen the pause instead of stretching the line.

## Episode log
- **ep00** series intro (storyline A, endless zoom). **ep01** Chapter 0: Inference (A + B + C mix: stall → stack rebuilds → runtime stack → six dials). Next: **ep02 Batching**, then caching, quantization, speculation, parallelism, disaggregation (one each).
- Script length: Kokoro `am_michael` at 1.0 speaks ≈ 2.4 words/s. Aim for **~130 words** of narration for 55–60 s. ep01's first draft (~180 words) ran 77 s.
- Vinit sends source text from a book (Baseten's on inference). Paraphrase it, keep only its facts, and drop first-person company anecdotes.
- When Vinit says "mix with more of X", keep X's spine and borrow one device each from the others.

## Build lessons (ep01)
- `videos/ep01-inference/gen_scenes.py` generates every scene from one shared CSS and helper set (GPU card, gauge, stack layers). Copy it for the next episode and change the scene bodies.
- **SVG gauge needles**: set the start with `tl.set(sel, { rotation, svgOrigin: "200 200" }, 0)`, then `tl.to(..., { rotation, svgOrigin })`. A `fromTo` whose from-state lacks `svgOrigin` rotates around the wrong point and the needle vanishes.
- **Hidden-at-start elements**: put `opacity:0` inline in the markup, not `tl.set(..., 0)` (lint: a set at 0 doesn't render on frame 0).
- **Green text on sand fails contrast** (1.6:1). Use a green underline bar or highlight (`.g`) instead of coloured text.
- "One frame that rebuilds" across scenes: give the scenes identical element positions and render earlier layers statically, with no entrance/exit zoom between them. That makes hard match cuts.
- Keep slider and track geometry inside its panel's inner width (900 px panel → ≤ 860 px of content).

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
