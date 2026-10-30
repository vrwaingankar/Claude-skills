# Review — ep00 final (voiced)

Voice: Vinit's voice cloned locally with Chatterbox (MIT) from a private sample (not in the repo); one clip per SCRIPT.md line,
silence-trimmed, 1.04x tempo, joined with 0.3–1.1 s pauses, loudness-normalised to -16 LUFS → `assets/vo.m4a` (60.0 s).
V2 (Vinit's pick "C"): cfg_weight 0.3, exaggeration 0.6, pause-free reference; name spelled "Vineet" for pronunciation,
vLLM/SGLang spelled "vee-ell-ell-em", "ess-jee-lang"; each line checked against its transcript, slips retaken.
Word timings: `assets/transcript.json` (whisper small.en).

Retime: every chapter scene starts 0.15 s before its line (cut leads the voice), exits at its own end − 0.5 s,
the prompt dot's travel ends just before each dive. Beats synced to words: GPU underline on "Hopper"/"Blackwell",
software stack layers drop on "CUDA", "vLLM", "SGLang", end-card follow line on "Follow". SFX moved with their cuts and
lowered under the voice (whooshes 0.2, click 0.4, riser 0.22, impact 0.35, pop 0.3).

Checked: `hyperframes check` clean (0 errors, 0 warnings). Snapshot review: thumbnail (phone + "You hit send."), name card,
each chapter readable at its mid frame, answer streams in, end card holds ~2.4 s after "Follow".
