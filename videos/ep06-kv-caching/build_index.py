"""Write index.html from the VO layout. usage: python build_index.py <layout.json>"""
import json, re, sys, os
P = os.path.dirname(os.path.abspath(__file__)); L = json.load(open(sys.argv[1]))
names = ["hook", "intro", "recap", "qkv", "attn", "auto", "without", "cache", "lookup", "compare", "scope", "found", "next"]
starts, total = L["scene_starts"], L["total"]
f = lambda x: (f"{x:.3f}".rstrip("0").rstrip(".") if x % 1 else f"{x:.1f}")
hosts = []
for i, n in enumerate(names):
    d = (starts[i + 1] if i + 1 < len(names) else total) - starts[i]
    hosts.append(f'      <div id="{n}" data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-start="{f(starts[i])}" data-duration="{f(round(d, 3))}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>')
st = dict(zip(names, starts)); sfx = []; k = [0]
def add(id_, file, t, dur, vol, extra=""):
    k[0] += 1; sfx.append(f'      <audio id="{id_}" class="clip" src="assets/sfx/{file}" data-start="{t:.2f}" data-duration="{dur}" data-track-index="{9 + k[0]}" data-volume="{vol}"{extra}></audio>')
for i, n in enumerate(["intro", "recap", "qkv", "attn", "auto", "cache", "compare", "scope", "found", "next"]):
    add(f"sfx-w{i + 1}", ["whoosh.mp3", "whoosh-short.mp3"][i % 2], st[n] - 0.35, 0.57, 0.2)
add("sfx-reread", "glitch-1.mp3", st["hook"] + 2.9, 0.8, 0.14, ' data-fade-out="0.3"')
add("sfx-kv", "click.mp3", st["recap"] + 3.15, 0.37, 0.28)
for j, t in enumerate([2.55, 4.25, 5.65]): add(f"sfx-v{j + 1}", "click-soft.mp3", st["qkv"] + t, 0.37, 0.25)
add("sfx-score", "click-soft.mp3", st["attn"] + 5.75, 0.37, 0.25)
add("sfx-rec", "glitch-1.mp3", st["without"] + 2.9, 1.2, 0.16, ' data-fade-out="0.4"')
add("sfx-mem", "impact-bass-2.mp3", st["cache"] + 1.4, 1.0, 0.22, ' data-fade-out="0.3"')
add("sfx-new", "ping.mp3", st["lookup"] + 2.7, 0.5, 0.2, ' data-fade-out="0.2"')
add("sfx-one", "impact-bass-1.mp3", st["compare"] + 2.55, 1.2, 0.26)
add("sfx-on", "click.mp3", st["scope"] + 3.05, 0.37, 0.3)
add("sfx-pop", "pop.mp3", st["next"] + 0.3, 0.72, 0.3)
idx = open(f"{P}/../ep01-inference/index.html").read()
head = idx[:idx.index('      <div id="ground"></div>') + len('      <div id="ground"></div>\n')]
head = re.sub(r'(id="root"[^>]*data-duration=")[0-9.]+', rf'\g<1>{f(total)}', head)
tail = '    </div>\n    <script>\n      window.__timelines["main"] = gsap.timeline({ paused: true });\n    </script>\n  </body>\n</html>\n'
vo = f'      <audio id="vo" class="clip" src="assets/vo.m4a" data-start="0" data-duration="{f(total)}" data-track-index="2" data-volume="1"></audio>'
open(f"{P}/index.html", "w").write(head + "\n".join(hosts) + "\n" + vo + "\n" + "\n".join(sfx) + "\n" + tail)
