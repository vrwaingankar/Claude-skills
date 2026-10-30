"""Join per-line VO clips into one voiceover and write its line layout.

usage: python build_vo.py <clip_dir> <out.wav> <layout.json> [tempo]
  clip_dir holds l00.wav, l01.wav, ... already silence-trimmed (see SKILL.md).
  Edit GAPS to taste: one pause after each line except the last.
Then: ffmpeg -i out.wav -af "loudnorm=I=-16:TP=-1.5:LRA=9" -c:a aac -b:a 192k assets/vo.m4a
"""
import glob, json, subprocess, sys, tempfile, os
import numpy as np, soundfile as sf

clip_dir, out_wav, layout = sys.argv[1:4]
tempo = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
LEAD, TAIL = 0.2, 0.8
# ep00: longer pause after the hook (room for its on-screen beat), after a dense line, and before the end card.
GAPS = [1.0, 0.3, 0.3, 0.3, 0.8, 0.3, 0.3, 0.3, 0.7, 1.1]

clips = sorted(glob.glob(f"{clip_dir}/l[0-9][0-9].wav"))
assert len(GAPS) == len(clips) - 1, f"{len(clips)} clips need {len(clips) - 1} gaps"
sr = 44100
out, t, starts, ends = [np.zeros(int(LEAD * sr))], LEAD, [], []
for i, path in enumerate(clips):
    if tempo != 1.0:
        tmp = os.path.join(tempfile.mkdtemp(), "c.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-af", f"atempo={tempo}", "-ar", str(sr), tmp], check=True)
        path = tmp
    a, r = sf.read(path)
    assert r == sr, f"{path}: resample to {sr} Hz first"
    if a.ndim > 1:
        a = a.mean(1)
    starts.append(round(t, 3)); out.append(a); t += len(a) / sr; ends.append(round(t, 3))
    pad = GAPS[i] if i < len(GAPS) else TAIL
    out.append(np.zeros(int(pad * sr))); t += pad
sf.write(out_wav, np.concatenate(out), sr)
json.dump({"starts": starts, "ends": ends, "total": round(t, 3)}, open(layout, "w"))
print("line starts", starts, "total", round(t, 3))
