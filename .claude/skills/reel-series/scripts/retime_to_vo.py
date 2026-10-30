"""Retime a HyperFrames reel to a voiceover layout (from build_vo.py).

usage: python retime_to_vo.py <project_dir> <layout.json>
Assumes ep00's structure: one scene per VO line in SCENES order, each scene's camera exit is
`tl.to("#<id>-w", { scale: 6 ... }, t)` and its prompt dot is `#<id>-dot`. Sets each scene host's
data-start (line start - 0.15 s, frame-snapped) and data-duration, the root duration, moves exits to
duration - 0.5 s, fits dot travel before the exit, moves SFX with their cuts at under-voice volumes,
and adds the <audio id="vo">. Reads the current durations as "old", so it can be re-run.
Word-synced beats inside scenes are NOT moved: re-sync them by hand (see SKILL.md).
"""
import json, re, sys
proj, layout = sys.argv[1], sys.argv[2]
L = json.load(open(layout))
FPS = 30
snap = lambda t: round(t * FPS) / FPS
fmt = lambda t: f"{t:.3f}".rstrip("0").rstrip(".") if t % 1 else f"{t:.1f}"

SCENES = scenes = ["hook", "intro", "app", "model", "gpu", "soft", "tricks", "modal", "prod", "answer", "next"]
total = snap(L["total"])
starts = [0.0] + [snap(s - 0.15) for s in L["starts"][1:]]
durs = [round(b - a, 4) for a, b in zip(starts, starts[1:] + [total])]

idx = open(f"{proj}/index.html").read()
old = {}
for name, s, d in zip(scenes, starts, durs):
    m = re.search(rf'(<div id="{name}" [^>]*?data-start=")([0-9.]+)(" data-duration=")([0-9.]+)', idx)
    old[name] = float(m.group(4))
    idx = idx.replace(m.group(0), f"{m.group(1)}{fmt(s)}{m.group(3)}{fmt(d)}")
idx = re.sub(r'(<div id="root"[^>]*data-duration=")[0-9.]+', rf"\g<1>{fmt(total)}", idx)

# SFX: whoosh into each dive, send click, riser -> impact on the answer, pop on the end card.
st = dict(zip(scenes, starts))
sfx = {f"sfx-w{i+1}": st[n] - 0.35 for i, n in enumerate(["intro", "app", "model", "gpu", "soft", "tricks", "modal", "prod", "next"])}
sfx.update({"sfx-send": 0.83, "sfx-hit": st["answer"] + 0.35, "sfx-riser": st["answer"] + 0.35 - 1.95, "sfx-pop": st["next"] + 0.28})
vol = {"sfx-send": 0.4, "sfx-hit": 0.35, "sfx-riser": 0.22, "sfx-pop": 0.3}
for k, t in sfx.items():
    v = vol.get(k, 0.2)
    idx = re.sub(rf'(<audio id="{k}"[^>]*data-start=")[0-9.]+', rf"\g<1>{t:.2f}", idx)
    idx = re.sub(rf'(<audio id="{k}"[^>]*data-volume=")[0-9.]+', rf"\g<1>{v}", idx)
idx = re.sub(r"<!-- Voiceover goes here[^\n]*-->",
             f'<audio id="vo" class="clip" src="assets/vo.m4a" data-start="0" data-duration="{fmt(total)}" data-track-index="2" data-volume="1"></audio>', idx)
open(f"{proj}/index.html", "w").write(idx)

POS = re.compile(r"(, )([0-9.]+)(\);\s*)$")
for name, d in zip(scenes, durs):
    path = f"{proj}/compositions/{name}.html"
    src = open(path).read().split("\n")
    do, delta = old[name], d - old[name]
    exit_old = do - 0.5
    dot_a = dot_s = None
    for i, line in enumerate(src):
        if f'"#{name}-w", {{ scale: 6' in line:
            src[i] = POS.sub(lambda m: f"{m.group(1)}{d - 0.5:.2f}{m.group(3)}", line)
        elif f'tl.fromTo("#{name}-dot"' in line:
            dot_a = i
        elif f'tl.to("#{name}-dot"' in line:
            dot_s = i
        elif name == "intro" and '"#intro-img"' in line:
            src[i] = re.sub(r"duration: ([0-9.]+)", lambda m: f"duration: {float(m.group(1)) + delta:.2f}", line, count=1)
    if dot_s is not None:
        a = float(POS.search(src[dot_a]).group(2))
        s = float(POS.search(src[dot_s]).group(2))
        dur = float(re.search(r"duration: ([0-9.]+)", src[dot_s]).group(1))
        gap = exit_old - (s + dur)
        end = d - 0.5 - gap
        if delta >= 0:
            a2, s2, dur2 = a + delta, s + delta, dur
        else:
            dur2 = min(dur, max(1.0, end - s))
            s2 = min(s, end - dur2)
            a2 = s2 - (s - a)
        src[dot_a] = POS.sub(lambda m: f"{m.group(1)}{a2:.2f}{m.group(3)}", src[dot_a])
        src[dot_s] = POS.sub(lambda m: f"{m.group(1)}{s2:.2f}{m.group(3)}", src[dot_s])
        src[dot_s] = re.sub(r"duration: [0-9.]+", f"duration: {dur2:.2f}", src[dot_s], count=1)
    open(path, "w").write("\n".join(src))
    print(f"{name:7s} start {starts[scenes.index(name)]:6.3f} dur {do:.2f} -> {d:.3f}")
print("total", total)
