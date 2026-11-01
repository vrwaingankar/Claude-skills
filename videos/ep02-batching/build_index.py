"""Write index.html from the VO layout. usage: python build_index.py <layout.json>"""
import json, re, sys, os
P = os.path.dirname(os.path.abspath(__file__)); L = json.load(open(sys.argv[1]))
names = ["hook", "intro", "recap", "batch", "tokens", "static", "dynamic", "cont", "thru", "offline", "online", "next"]
starts, total = L["scene_starts"], L["total"]
f = lambda x: (f"{x:.3f}".rstrip("0").rstrip(".") if x % 1 else f"{x:.1f}")
hosts = []
for i, n in enumerate(names):
    d = (starts[i + 1] if i + 1 < len(names) else total) - starts[i]
    hosts.append(f'      <div id="{n}" data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-start="{f(starts[i])}" data-duration="{f(round(d, 3))}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>')
st = dict(zip(names, starts)); sfx = []; k = [0]
def add(id_, file, t, dur, vol, extra=""):
    k[0] += 1; sfx.append(f'      <audio id="{id_}" class="clip" src="assets/sfx/{file}" data-start="{t:.2f}" data-duration="{dur}" data-track-index="{9 + k[0]}" data-volume="{vol}"{extra}></audio>')
for i, n in enumerate(["intro", "recap", "batch", "tokens", "static", "dynamic", "cont", "thru", "offline", "next"]):
    add(f"sfx-w{i + 1}", ["whoosh.mp3", "whoosh-short.mp3"][i % 2], st[n] - 0.35, 0.57, 0.2)
add("sfx-pick", "click.mp3", st["recap"] + 4.3, 0.37, 0.35)
add("sfx-gpu", "impact-bass-2.mp3", st["batch"] + 2.75, 1.0, 0.25, ' data-fade-out="0.3"')
add("sfx-idle", "glitch-1.mp3", st["static"] + 5.0, 0.8, 0.15, ' data-fade-out="0.2"')
add("sfx-time", "ping.mp3", st["dynamic"] + 3.75, 0.5, 0.2, ' data-fade-out="0.2"')
for j, t in enumerate([1.45, 2.05, 4.35]): add(f"sfx-in{j + 1}", "click-soft.mp3", st["cont"] + t, 0.37, 0.3)
add("sfx-riser", "riser.mp3", st["thru"] + 1.0 - 1.6, 1.6, 0.18, ' data-fade-out="0.2"')
add("sfx-hit", "impact-bass-1.mp3", st["thru"] + 1.0, 1.6, 0.28)
add("sfx-pop", "pop.mp3", st["next"] + 0.3, 0.72, 0.3)
idx = open(f"{P}/../ep01-inference/index.html").read()
head = idx[:idx.index('      <div id="ground"></div>') + len('      <div id="ground"></div>\n')]
head = re.sub(r'(id="root"[^>]*data-duration=")[0-9.]+', rf'\g<1>{f(total)}', head)
tail = '    </div>\n    <script>\n      window.__timelines["main"] = gsap.timeline({ paused: true });\n    </script>\n  </body>\n</html>\n'
vo = f'      <audio id="vo" class="clip" src="assets/vo.m4a" data-start="0" data-duration="{f(total)}" data-track-index="2" data-volume="1"></audio>'
open(f"{P}/index.html", "w").write(head + "\n".join(hosts) + "\n" + vo + "\n" + "\n".join(sfx) + "\n" + tail)
