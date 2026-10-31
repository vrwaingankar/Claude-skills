# Review — ep00 final (voiced)

Voice (v3, final): stock male narrator, Kokoro `am_michael` at 0.95x (Vinit dropped his cloned voice). Name said "Vineeth"
via phoneme override, CUDA forced to "koo-da"; every line checked against its own transcript (all clean). Clips trimmed,
joined with 0.45–1.1 s pauses, loudness-normalised to -16 LUFS → `assets/vo.m4a` (58.0 s). Name card now reads
"Sr AI Architect · Tech Lead". Word timings: `assets/transcript.json`.

Retime: every chapter scene starts 0.15 s before its line (cut leads the voice), exits at its own end − 0.5 s,
the prompt dot's travel ends just before each dive. Beats synced to words: GPU underline on "Hopper"/"Blackwell",
software stack layers drop on "CUDA", "vLLM", "SGLang", end-card follow line on "Follow". SFX moved with their cuts and
lowered under the voice (whooshes 0.2, click 0.4, riser 0.22, impact 0.35, pop 0.3).

Checked: `hyperframes check` clean (0 errors, 0 warnings). Snapshot review: thumbnail (phone + "You hit send."), name card,
each chapter readable at its mid frame, answer streams in, end card holds ~2.4 s after "Follow".
