"""Write index.html from the VO layout. usage: python build_index.py <layout.json>"""
import json, re, sys, os
P = os.path.dirname(os.path.abspath(__file__)); L = json.load(open(sys.argv[1]))
names = ["hook", "intro", "recap", "goal", "rect", "decode", "swap", "formula", "shapes", "ragged", "mask", "budget", "refill", "sum", "next"]
starts, total = L["scene_starts"], L["total"]
f = lambda x: (f"{x:.3f}".rstrip("0").rstrip(".") if x % 1 else f"{x:.1f}")
hosts = []
for i, n in enumerate(names):
    d = (starts[i + 1] if i + 1 < len(names) else total) - starts[i]
    hosts.append(f'      <div id="{n}" data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-start="{f(starts[i])}" data-duration="{f(round(d, 3))}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>')
st = dict(zip(names, starts)); sfx = []; k = [0]
def add(id_, file, t, dur, vol, extra=""):
    k[0] += 1; sfx.append(f'      <audio id="{id_}" class="clip" src="assets/sfx/{file}" data-start="{t:.2f}" data-duration="{dur}" data-track-index="{9 + k[0]}" data-volume="{vol}"{extra}></audio>')
for i, n in enumerate(["intro", "recap", "goal", "rect", "decode", "swap", "formula", "shapes", "ragged", "budget", "sum", "next"]):
    add(f"sfx-w{i + 1}", ["whoosh.mp3", "whoosh-short.mp3"][i % 2], st[n] - 0.35, 0.57, 0.2)
add("sfx-pick", "click.mp3", st["recap"] + 3.25, 0.37, 0.3)
add("sfx-frame", "click-soft.mp3", st["rect"] + 1.45, 0.37, 0.3)
add("sfx-pads", "glitch-1.mp3", st["rect"] + 3.45, 0.7, 0.14, ' data-fade-out="0.2"')
for j, t in enumerate([1.8, 2.4, 3.0, 3.6]): add(f"sfx-dec{j + 1}", "click-soft.mp3", st["decode"] + t, 0.37, 0.22)
add("sfx-eos", "ping.mp3", st["decode"] + 4.5, 0.5, 0.2, ' data-fade-out="0.2"')
add("sfx-flood", "glitch-1.mp3", st["swap"] + 4.4, 0.9, 0.18, ' data-fade-out="0.3"')
add("sfx-riser", "riser.mp3", st["formula"] + 6.3 - 1.6, 1.6, 0.18, ' data-fade-out="0.2"')
add("sfx-693", "impact-bass-1.mp3", st["formula"] + 6.3, 1.6, 0.3)
add("sfx-crack", "impact-bass-2.mp3", st["ragged"] + 0.9, 1.0, 0.28, ' data-fade-out="0.3"')
for j, t in enumerate([2.4, 2.6, 2.8]): add(f"sfx-b{j + 1}", "click-soft.mp3", st["budget"] + t, 0.37, 0.25)
add("sfx-full", "ping.mp3", st["budget"] + 5.6, 0.5, 0.2, ' data-fade-out="0.2"')
add("sfx-slot", "click.mp3", st["refill"] + 3.85, 0.37, 0.3)
add("sfx-sum", "impact-bass-1.mp3", st["sum"] + 4.55, 1.4, 0.26)
add("sfx-pop", "pop.mp3", st["next"] + 0.3, 0.72, 0.3)
idx = open(f"{P}/../ep01-inference/index.html").read()
head = idx[:idx.index('      <div id="ground"></div>') + len('      <div id="ground"></div>\n')]
head = re.sub(r'(id="root"[^>]*data-duration=")[0-9.]+', rf'\g<1>{f(total)}', head)
tail = '    </div>\n    <script>\n      window.__timelines["main"] = gsap.timeline({ paused: true });\n    </script>\n  </body>\n</html>\n'
vo = f'      <audio id="vo" class="clip" src="assets/vo.m4a" data-start="0" data-duration="{f(total)}" data-track-index="2" data-volume="1"></audio>'
open(f"{P}/index.html", "w").write(head + "\n".join(hosts) + "\n" + vo + "\n" + "\n".join(sfx) + "\n" + tail)
