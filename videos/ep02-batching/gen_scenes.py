"""Generate ep02 (Batching) scene files. usage: python gen_scenes.py <project_dir>
Shared look/helpers: .claude/skills/reel-series/scripts/reel_lib.py. Beat times are scene-relative seconds synced to the VO words."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.claude/skills/reel-series/scripts"))
from reel_lib import BASE, BIG, ENTER, EXIT, gauge, gpu, scene

OUT = sys.argv[1]
S = {}
CLIP = lambda sel, t, d=0.45: f'tl.fromTo("{sel}", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: {d}, ease: "power3.inOut" }}, {t});'
KICK = lambda n, t=0.15: f'tl.fromTo("#{n}-kick", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, {t});'
HATCH = "repeating-linear-gradient(45deg, rgba(20,33,61,.28) 0 6px, transparent 6px 14px)"
ROWC = ["#14213D", "#2B3B60", "#3E5280", "#576A99"]
DUR = {"hook": 3.767, "intro": 4.0, "recap": 5.167, "batch": 5.833, "tokens": 7.5, "static": 6.133, "dynamic": 6.0,
       "cont": 6.633, "thru": 5.7, "offline": 5.133, "online": 5.2, "next": 6.067}
X = lambda n: round(DUR[n] - 0.5, 2)

# 0 hook: the GPU as a bus with one rider --------------------------------------
seats = "".join(f'<div class="hk-seat" style="left:{40 + i * 210}px"><div id="hook-s{i}" class="hk-fill" style="{"background:#14213D" if i == 0 else "background:" + HATCH}"></div></div>' for i in range(4))
S["hook"] = scene("hook", """
#hook-l1, #hook-l2 { position: absolute; left: 84px; font: 900 128px/1 Inter; letter-spacing: -0.035em; white-space: nowrap; }
#hook-l1 { top: 230px; } #hook-l2 { top: 380px; }
#hook-bus { left: 90px; top: 600px; width: 900px; height: 330px; }
.hk-seat { position: absolute; top: 90px; width: 180px; height: 170px; border: 4px solid #14213D; border-radius: 14px; background: #F3EBDD; overflow: hidden; }
.hk-fill { position: absolute; inset: 10px; border-radius: 8px; }
.hk-wh { position: absolute; top: 905px; width: 110px; height: 110px; border-radius: 50%; background: #14213D; border: 14px solid #F3EBDD; box-shadow: 0 0 0 4px #14213D; }
""", f"""
      <div id="hook-l1">Your GPU,</div>
      <div id="hook-l2">mostly <span class="g">idle</span></div>
      <div id="hook-bus" class="pn"><div class="lb" style="left:40px;top:28px">GPU · 4 batch slots</div>{seats}</div>
      <div class="hk-wh" style="left:200px"></div><div class="hk-wh" style="left:770px"></div>
      <div class="lb" style="left:90px;top:1060px">1 request running · 3 slots waiting</div>
""", f"""
    tl.fromTo("#hook-bus", {{ x: 0 }}, {{ x: 14, duration: 0.12, yoyo: true, repeat: 3, ease: "sine.inOut" }}, 0.5);
    tl.fromTo("#hook-s1, #hook-s2, #hook-s3", {{ opacity: 1 }}, {{ opacity: 0.35, duration: 0.18, stagger: 0.08, yoyo: true, repeat: 3 }}, 2.0);
    {EXIT("hook", X("hook"))}
""")

# 1 intro: same name card as ep00/ep01 ----------------------------------------------
S["intro"] = scene("intro", """
#intro-ph { position: absolute; left: 90px; top: 214px; width: 600px; height: 720px; border-radius: 28px; overflow: hidden; border: 6px solid #14213D; box-shadow: 0 14px 0 rgba(20,33,61,.14); }
#intro-ph img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 20%; }
#intro-name { position: absolute; left: 80px; top: 966px; font: 900 190px/1 Inter; letter-spacing: -0.045em; }
#intro-role { position: absolute; left: 90px; top: 1166px; font: 700 52px/1 Inter; white-space: nowrap; }
#intro-rule { position: absolute; left: 90px; top: 1240px; width: 420px; height: 10px; background: #00C46A; transform-origin: 0 50%; }
#intro-ser { position: absolute; left: 90px; top: 1272px; font: 700 40px/1 Inter; opacity: .7; white-space: nowrap; }
""", """
      <div id="intro-ph"><img id="intro-img" src="assets/vinit.jpg" alt="Vinit" /></div>
      <div id="intro-name">Vinit</div>
      <div id="intro-role">Sr AI Architect · Tech Lead</div>
      <div id="intro-rule"></div>
      <div id="intro-ser">AI inference, end to end · Ep 2</div>
""", f"""
    {ENTER("intro")}
    tl.fromTo("#intro-ph", {{ clipPath: "inset(100% 0 0 0)" }}, {{ clipPath: "inset(0% 0 0 0)", duration: 0.5, ease: "expo.out" }}, 0.1);
    tl.fromTo("#intro-img", {{ scale: 1.18 }}, {{ scale: 1.04, duration: 3.8, ease: "power1.out" }}, 0.1);
    {CLIP("#intro-name", 0.55)}
    tl.fromTo("#intro-role", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 1.2);
    tl.fromTo("#intro-rule", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "power3.inOut" }}, 1.4);
    {CLIP("#intro-ser", 1.4)}
    {EXIT("intro", X("intro"))}
""")

# 2 recap: three layers, six techniques, batching lights up ---------------------------
techs = ["Batching", "Caching", "Quantization", "Speculation", "Parallelism", "Disaggregation"]
chips = "".join(f'<div id="recap-c{i}" class="pn rc-c" style="left:{90 + (i % 3) * 305}px;top:{900 + (i // 3) * 130}px"><div class="rc-t">{t}</div></div>' for i, t in enumerate(techs))
layers = "".join(f'<div class="pn rc-l" style="top:{520 + i * 110}px"><div class="lb" style="left:26px;top:24px">{t}</div></div>' for i, t in enumerate(["Tooling", "Infrastructure", "Runtime"]))
S["recap"] = scene("recap", """
.rc-l { left: 90px; width: 900px; height: 86px; }
.rc-c { width: 285px; height: 104px; }
.rc-t { position: absolute; left: 0; right: 0; top: 36px; text-align: center; font: 700 30px/1 Inter; white-space: nowrap; }
#recap-c0 { transform-origin: 50% 50%; }
""", f"""
      {BIG("recap").replace(">0<", ">1<")}
      <div id="recap-kick" class="kick">Previously · Ep 1</div>
      <div id="recap-ttl" class="ttl">The <span class="g">stack</span></div>
      {layers}
      {chips}
""", f"""
    {ENTER("recap")}
    {KICK("recap")}
    {CLIP("#recap-ttl", 0.25)}
    tl.fromTo(".rc-l", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, stagger: 0.12, ease: "expo.out" }}, 0.75);
    tl.fromTo(".rc-c", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, stagger: 0.06, ease: "back.out(1.6)" }}, 1.85);
    tl.to("#recap-c0", {{ backgroundColor: "#00C46A", scale: 1.12, duration: 0.3, ease: "back.out(2)" }}, 4.3);
    {EXIT("recap", X("recap"))}
""")

# 3 batch: requests grouped into one batch, meters --------------------------------------
reqs = "".join(f'<div class="bt-r pn" style="left:{x}px;top:{y}px;width:{w}px"><div class="lb" style="left:20px;top:22px">request</div></div>' for x, y, w in [(120, 520, 300), (560, 560, 360), (180, 690, 340), (600, 720, 300)])
S["batch"] = scene("batch", """
.bt-r { height: 84px; }
#batch-tray { position: absolute; left: 90px; top: 500px; width: 900px; height: 420px; border: 4px dashed rgba(20,33,61,.4); border-radius: 22px; }
.bt-m { position: absolute; left: 90px; width: 900px; height: 34px; border-radius: 17px; background: rgba(20,33,61,.12); overflow: hidden; }
.bt-f { position: absolute; left: 0; top: 0; bottom: 0; width: 100%; border-radius: 17px; transform-origin: 0 50%; }
""", f"""
      {BIG("batch").replace(">0<", ">2<")}
      <div id="batch-kick" class="kick">Technique 1</div>
      <div id="batch-ttl" class="ttl"><span class="g">Batching</span></div>
      <div id="batch-tray" style="opacity:0"><div class="lb" style="left:24px;top:-50px">one batch</div></div>
      <div id="batch-reqs">{reqs}</div>
      {gpu("batch-gpu", 390, 950)}
      <div class="lb" style="left:90px;top:1150px">work per GPU step</div>
      <div class="bt-m" style="top:1200px"><div id="batch-work" class="bt-f" style="background:#14213D"></div></div>
      <div class="lb" style="left:90px;top:1252px">cost per token</div>
      <div class="bt-m" style="top:1290px"><div id="batch-cost" class="bt-f" style="background:#576A99"></div></div>
""", f"""
    {ENTER("batch")}
    {KICK("batch")}
    {CLIP("#batch-ttl", 0.2)}
    tl.set("#batch-work", {{ scaleX: 0.25 }}, 0);
    tl.set("#batch-cost", {{ scaleX: 0.85 }}, 0);
    tl.fromTo("#batch-reqs .bt-r", {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.3, stagger: 0.1, ease: "expo.out" }}, 0.4);
    tl.to("#batch-tray", {{ opacity: 1, duration: 0.2 }}, 1.2);
    tl.to("#batch-reqs .bt-r", {{ x: (i) => [-10, -450, -70, -490][i], y: (i) => [0, 50, 10, 70][i], duration: 0.45, stagger: 0.06, ease: "power3.inOut" }}, 1.25);
    tl.to("#batch-gpu .cell", {{ backgroundColor: "#00C46A", duration: 0.1, stagger: 0.03 }}, 2.75);
    tl.to("#batch-work", {{ scaleX: 0.92, duration: 0.5, ease: "power3.out" }}, 3.65);
    tl.to("#batch-cost", {{ scaleX: 0.32, duration: 0.5, ease: "power3.out" }}, 4.65);
    {EXIT("batch", X("batch"))}
""")

# 4 tokens: token by token, KV cache, 50 vs 500 -------------------------------------
toks = "".join(f'<div class="tok tk-t" style="left:{90 + i * 74}px;top:540px"></div>' for i in range(11))
kv = "".join(f'<div class="tk-kv" style="left:{24 + i * 76}px"></div>' for i in range(11))
S["tokens"] = scene("tokens", """
.tk-t { width: 62px; height: 62px; }
#tokens-kv { left: 90px; top: 690px; width: 900px; height: 130px; }
.tk-kv { position: absolute; top: 62px; width: 62px; height: 44px; border-radius: 8px; background: #3E5280; }
.tk-bar { position: absolute; left: 90px; height: 64px; border-radius: 12px; background: #14213D; transform-origin: 0 50%; }
""", f"""
      {BIG("tokens").replace(">0<", ">2<")}
      <div id="tokens-kick" class="kick">Why LLMs are different</div>
      <div id="tokens-ttl" class="ttl" style="font-size:112px">Token by <span class="g">token</span></div>
      {toks}
      <div id="tokens-kv" class="pn"><div class="lb" style="left:24px;top:16px">KV cache · past tokens</div>{kv}</div>
      <div class="lb" style="left:90px;top:900px">lengths vary</div>
      <div id="tokens-b1" class="tk-bar" style="top:960px;width:120px"></div><div id="tokens-l1" class="lb" style="left:230px;top:976px">50 tokens</div>
      <div id="tokens-b2" class="tk-bar" style="top:1070px;width:900px;background:#3E5280"></div><div id="tokens-l2" class="lb" style="left:90px;top:1160px">500 tokens</div>
""", f"""
    {ENTER("tokens")}
    {KICK("tokens")}
    {CLIP("#tokens-ttl", 0.3)}
    tl.fromTo(".tk-t", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.12, stagger: 0.16, ease: "back.out(2)" }}, 1.15);
    tl.fromTo("#tokens-kv", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 2.7);
    tl.fromTo(".tk-kv", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, stagger: 0.12 }}, 2.75);
    tl.fromTo("#tokens-b1", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power2.out" }}, 4.9);
    tl.fromTo("#tokens-l1", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 4.95);
    tl.fromTo("#tokens-b2", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.9, ease: "power1.inOut" }}, 6.05);
    tl.fromTo("#tokens-l2", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 6.1);
    {EXIT("tokens", X("tokens"))}
""")

# 5 & 7: the batch grid (identical geometry) ------------------------------------------
COLS, CW, GX, GY, RH = 8, 100, 90, 560, 112
GRID_CSS = """
.gd-c { position: absolute; width: 90px; height: 94px; border: 3px solid rgba(20,33,61,.25); border-radius: 10px; background: #F3EBDD; overflow: hidden; }
.gd-f, .gd-i { position: absolute; inset: 0; opacity: 0; }
.gd-i { background: """ + HATCH + """; }
.gd-ph { position: absolute; top: 540px; width: 6px; height: 470px; background: #14213D; border-radius: 3px; }
.gd-m { position: absolute; left: 90px; top: 1120px; width: 800px; height: 40px; border-radius: 20px; background: rgba(20,33,61,.12); overflow: hidden; }
.gd-mf { position: absolute; inset: 0; border-radius: 20px; background: #14213D; transform-origin: 0 50%; }
.gd-q { position: absolute; left: 930px; width: 70px; height: 94px; border-radius: 10px; background: #00C46A; border: 3px solid #14213D; }
"""

def grid(n, plan, t0, step, queue=0):
    """plan: per row a list of (length, color); cells after the last request turn idle."""
    h, js = [], []
    for r, reqs in enumerate(plan):
        col = 0
        cells = {}
        for k, (ln, colr) in enumerate(reqs):
            for c in range(col, min(col + ln, COLS)):
                cells[c] = colr
            col += ln
        for c in range(COLS):
            cid = f"{n}-r{r}c{c}"
            h.append(f'<div class="gd-c" style="left:{GX + c * CW}px;top:{GY + r * RH}px"><div id="{cid}f" class="gd-f" style="background:{cells.get(c, "transparent")}"></div><div id="{cid}i" class="gd-i"></div></div>')
            t = round(t0 + c * step, 2)
            js.append(f'tl.to("#{cid}{"f" if c in cells else "i"}", {{ opacity: 1, duration: 0.12 }}, {t});')
    for q in range(queue):
        h.append(f'<div id="{n}-q{q}" class="gd-q" style="top:{GY + q * RH}px"></div>')
    h.append(f'<div id="{n}-ph" class="gd-ph" style="left:{GX - 8}px"></div>')
    js.append(f'tl.fromTo("#{n}-ph", {{ x: 0 }}, {{ x: {COLS * CW}, duration: {COLS * step:.2f}, ease: "none" }}, {t0});')
    return "\n      ".join(h), "\n    ".join(js)

g5, j5 = grid("static", [[(8, ROWC[0])], [(3, ROWC[1])], [(5, ROWC[2])], [(2, ROWC[3])]], 0.9, 0.55)
S["static"] = scene("static", GRID_CSS, f"""
      {BIG("static").replace(">0<", ">2<")}
      <div id="static-kick" class="kick">Rule 1 · wait for the longest</div>
      <div id="static-ttl" class="ttl"><span class="g">Static</span></div>
      <div class="lb" style="left:90px;top:500px;opacity:.62">GPU slots × token steps</div>
      {g5}
      <div class="lb" style="left:90px;top:1070px">GPU busy</div>
      <div class="gd-m"><div id="static-m" class="gd-mf"></div></div>
""", f"""
    {ENTER("static")}
    {KICK("static")}
    {CLIP("#static-ttl", 0.25)}
    {j5}
    tl.to("#static-m", {{ keyframes: [{{ scaleX: 1, duration: 0.01 }}, {{ scaleX: 0.75, duration: 0.3 }}, {{ scaleX: 0.5, duration: 0.6 }}, {{ scaleX: 0.25, duration: 0.6 }}], ease: "power2.out" }}, 1.9);
    tl.fromTo("#static-w .gd-i", {{ scale: 1 }}, {{ scale: 0.86, duration: 0.15, yoyo: true, repeat: 1 }}, 5.05);
    {EXIT("static", X("static"))}
""")

# 6 dynamic: a timer gate --------------------------------------------------------------
S["dynamic"] = scene("dynamic", """
.dy-s { position: absolute; top: 640px; width: 150px; height: 110px; border: 4px dashed rgba(20,33,61,.4); border-radius: 14px; }
.dy-r { position: absolute; top: 650px; width: 130px; height: 90px; border-radius: 10px; background: #14213D; }
.dy-w { position: absolute; top: 1150px; width: 110px; height: 80px; border-radius: 10px; background: #576A99; }
#dynamic-tray { position: absolute; left: 90px; top: 600px; width: 690px; height: 190px; }
""", f"""
      {BIG("dynamic").replace(">0<", ">2<")}
      <div id="dynamic-kick" class="kick">Rule 2 · fill, or time out</div>
      <div id="dynamic-ttl" class="ttl"><span class="g">Dynamic</span></div>
      <div class="lb" style="left:90px;top:560px">batch · max size 4</div>
      {"".join(f'<div class="dy-s" style="left:{100 + i * 170}px"></div>' for i in range(4))}
      <div id="dynamic-reqs">{"".join(f'<div class="dy-r" style="left:{110 + i * 170}px"></div>' for i in range(3))}</div>
      <svg id="dynamic-clock" style="position:absolute;left:800px;top:580px" width="190" height="190" viewBox="0 0 190 190">
        <circle cx="95" cy="95" r="70" fill="#F3EBDD" stroke="#14213D" stroke-opacity=".2" stroke-width="18"/>
        <circle id="dynamic-arc" cx="95" cy="95" r="70" fill="none" stroke="#14213D" stroke-width="18" stroke-dasharray="440" stroke-dashoffset="440" transform="rotate(-90 95 95)"/></svg>
      <div class="lb" style="left:820px;top:800px">timeout</div>
      {gpu("dynamic-gpu", 390, 880)}
      <div id="dynamic-wl" class="lb" style="left:90px;top:1100px">next requests wait</div>
      <div id="dynamic-wait">{"".join(f'<div class="dy-w" style="left:{90 + i * 130}px"></div>' for i in range(4))}</div>
""", f"""
    {ENTER("dynamic")}
    {KICK("dynamic")}
    {CLIP("#dynamic-ttl", 0.25)}
    tl.fromTo("#dynamic-reqs .dy-r", {{ x: -500, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, stagger: 0.55, ease: "power3.out" }}, 0.6);
    tl.to("#dynamic-arc", {{ strokeDashoffset: 0, duration: 2.75, ease: "none" }}, 1.0);
    tl.to("#dynamic-reqs", {{ y: 300, scale: 0.5, opacity: 0, transformOrigin: "50% 100%", duration: 0.4, ease: "power2.in" }}, 3.75);
    tl.to("#dynamic-gpu .cell", {{ backgroundColor: "#00C46A", duration: 0.1, stagger: 0.03 }}, 4.0);
    tl.fromTo("#dynamic-wl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 4.6);
    tl.fromTo("#dynamic-wait .dy-w", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.25, stagger: 0.15, ease: "back.out(1.6)" }}, 4.7);
    {EXIT("dynamic", X("dynamic"))}
""")

# 7 continuous: same grid, finished slots refill from the queue ---------------------
G = "#00C46A"
g7, j7 = grid("cont", [[(8, ROWC[0])], [(3, ROWC[1]), (5, G)], [(7, ROWC[2]), (1, G)], [(2, ROWC[3]), (6, G)]], 0.6, 0.6, queue=3)
S["cont"] = scene("cont", GRID_CSS, f"""
      {BIG("cont").replace(">0<", ">2<")}
      <div id="cont-kick" class="kick">Rule 3 · refill every step</div>
      <div id="cont-ttl" class="ttl"><span class="g">Continuous</span></div>
      <div class="lb" style="left:90px;top:500px;opacity:.62">GPU slots × token steps</div>
      <div class="lb" style="left:905px;top:500px;opacity:.62">queue</div>
      {g7}
      <div class="lb" style="left:90px;top:1070px">GPU busy</div>
      <div class="gd-m"><div id="cont-m" class="gd-mf"></div></div>
""", f"""
    {ENTER("cont")}
    {KICK("cont")}
    {CLIP("#cont-ttl", 0.25)}
    {j7}
    tl.to("#cont-q0", {{ x: -640, y: {3 * RH}, duration: 0.35, ease: "power3.inOut" }}, 1.4);
    tl.to("#cont-q0", {{ opacity: 0, duration: 0.1 }}, 1.8);
    tl.to("#cont-q1", {{ x: -540, y: 0, duration: 0.35, ease: "power3.inOut" }}, 2.0);
    tl.to("#cont-q1", {{ opacity: 0, duration: 0.1 }}, 2.4);
    tl.to("#cont-q2", {{ x: -140, y: 0, scale: 1.1, duration: 0.45, ease: "power3.inOut" }}, 4.3);
    tl.to("#cont-q2", {{ opacity: 0, duration: 0.1 }}, 4.85);
    {EXIT("cont", X("cont"))}
""")

# 8 throughput: no idle slots, engines ------------------------------------------------
S["thru"] = scene("thru", """
.th-e { position: absolute; top: 980px; width: 420px; height: 120px; }
.th-e .lb { left: 30px; top: 42px; font-size: 40px; }
""", f"""
      {BIG("thru").replace(">0<", ">2<")}
      <div id="thru-kick" class="kick">Continuous batching</div>
      <div id="thru-ttl" class="ttl" style="font-size:112px">No idle <span class="g">slots</span></div>
      {gauge("thru-g", 90, 520, 520)}
      <div class="lb" style="left:640px;top:600px">throughput</div>
      <div id="thru-hi" class="lb" style="left:640px;top:660px;font-size:44px">much higher</div>
      <div class="lb" style="left:90px;top:920px;opacity:.62">made popular by</div>
      <div id="thru-e0" class="th-e pn" style="left:90px"><div class="lb">vLLM</div></div>
      <div id="thru-e1" class="th-e pn" style="left:570px"><div class="lb">TGI</div></div>
""", f"""
    {ENTER("thru")}
    {KICK("thru")}
    {CLIP("#thru-ttl", 0.2)}
    tl.set("#thru-g-n", {{ rotation: -60, svgOrigin: "200 200" }}, 0);
    tl.to("#thru-g-n", {{ rotation: 72, duration: 0.6, svgOrigin: "200 200", ease: "back.out(1.4)" }}, 1.0);
    {CLIP("#thru-hi", 1.5, 0.35)}
    tl.fromTo("#thru-e0", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(1.6)" }}, 2.75);
    tl.fromTo("#thru-e1", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(1.6)" }}, 3.9);
    {EXIT("thru", X("thru"))}
""")

# 9 & 10: two clocks (one split frame, two scenes) ----------------------------------
def clocks(n, focus):
    tickets = "".join(f'<div class="ck-t" style="left:{60 + (i % 5) * 84}px;top:{420 + (i // 5) * 64}px"></div>' for i in range(25))
    stream = "".join(f'<div class="tok ck-s" style="left:{24 + (i % 6) * 64}px;top:{90 + (i // 6) * 54}px;width:52px;height:38px"></div>' for i in range(12))
    css = """
.ck-l { position: absolute; left: 0; top: 180px; width: 536px; height: 1140px; background: #14213D; }
.ck-h { position: absolute; top: 220px; font: 900 96px/1 Inter; letter-spacing: -0.03em; }
.ck-t { position: absolute; width: 70px; height: 50px; border-radius: 8px; background: #E6D8BF; }
.ck-m { position: absolute; left: 60px; width: 420px; height: 30px; border-radius: 15px; background: rgba(230,216,191,.2); overflow: hidden; }
.ck-mf { position: absolute; inset: 0; border-radius: 15px; transform-origin: 0 50%; }
.ck-lb { position: absolute; font: 700 34px/1 Inter; white-space: nowrap; }
#N-chat { left: 590px; top: 400px; width: 440px; height: 300px; }
.ck-sw { position: absolute; top: 820px; width: 190px; height: 190px; border-radius: 50%; border: 8px solid #14213D; background: #F3EBDD; }
.ck-hand { position: absolute; left: 89px; top: 20px; width: 6px; height: 76px; background: #14213D; border-radius: 3px; transform-origin: 50% 100%; }
""".replace("N-", f"{n}-")
    markup = f"""
      <div id="{n}-lw"{' style="opacity:0.55"' if focus == "r" and False else ""}>
      <div id="{n}-left" class="ck-l"></div>
      <div id="{n}-oh" class="ck-h" style="left:60px;color:#E6D8BF">Offline</div>
      <div id="{n}-tk">{tickets}</div>
      <div class="ck-lb" style="left:60px;top:780px;color:#E6D8BF">millions of tickets</div>
      <div class="ck-lb" style="left:60px;top:900px;color:#E6D8BF">throughput</div>
      <div class="ck-m" style="top:950px"><div id="{n}-tp" class="ck-mf" style="background:#00C46A"></div></div>
      <div class="ck-lb" style="left:60px;top:1030px;color:#E6D8BF">cost per token</div>
      <div class="ck-m" style="top:1080px"><div id="{n}-cs" class="ck-mf" style="background:#E6D8BF"></div></div>
      </div>
      <div id="{n}-rw"{' style="opacity:0.55"' if focus == "l" else ""}>
      <div id="{n}-nh" class="ck-h" style="left:590px">Online</div>
      <div id="{n}-chat" class="pn"><div class="ck-lb" style="left:24px;top:24px">live chat</div><div style="position:absolute;left:0;top:0">{stream}</div></div>
      <div class="ck-sw" style="left:600px"><div id="{n}-h1" class="ck-hand"></div></div>
      <div class="ck-sw" style="left:830px"><div id="{n}-h2" class="ck-hand"></div></div>
      <div class="ck-lb" style="left:620px;top:1040px">first token</div>
      <div class="ck-lb" style="left:840px;top:1040px">between</div>
      </div>
"""
    return css, markup

c9, m9 = clocks("offline", "l")
S["offline"] = scene("offline", c9 + "\n#offline-chat .ck-s { opacity: 0; }", m9, f"""
    {ENTER("offline")}
    tl.set("#offline-tp", {{ scaleX: 0.3 }}, 0);
    tl.set("#offline-cs", {{ scaleX: 0.8 }}, 0);
    tl.fromTo("#offline-tk .ck-t", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.15, stagger: 0.04, ease: "power2.out" }}, 1.1);
    tl.to("#offline-tp", {{ scaleX: 0.95, duration: 0.5, ease: "power3.out" }}, 3.55);
    tl.to("#offline-cs", {{ scaleX: 0.25, duration: 0.5, ease: "power3.out" }}, 4.1);
""", origin="800px 900px")
c10, m10 = clocks("online", "r")
S["online"] = scene("online", c10, m10, f"""
    tl.set("#online-tp", {{ scaleX: 0.95 }}, 0);
    tl.set("#online-cs", {{ scaleX: 0.25 }}, 0);
    tl.fromTo("#online-rw", {{ opacity: 0.55 }}, {{ opacity: 1, duration: 0.3 }}, 0.1);
    tl.to("#online-lw", {{ opacity: 0.55, duration: 0.3 }}, 0.2);
    tl.fromTo("#online-chat .ck-s", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.06, stagger: (i) => i === 0 ? 0 : 0.6 + i * 0.22 }}, 2.0);
    tl.fromTo("#online-h1", {{ rotation: 0 }}, {{ rotation: 140, duration: 0.6, ease: "none" }}, 1.95);
    tl.fromTo("#online-h2", {{ rotation: 0 }}, {{ rotation: 300, duration: 1.6, ease: "steps(8)" }}, 3.5);
    {EXIT("online", X("online"))}
""", origin="800px 900px")

# 11 next -----------------------------------------------------------------------------------
S["next"] = scene("next", """
#next-k { position: absolute; left: 90px; top: 214px; font: 700 48px/1 Inter; opacity: .62; }
#next-ep { position: absolute; left: 70px; top: 270px; font: 900 360px/1 Inter; letter-spacing: -0.06em; }
#next-t { position: absolute; left: 84px; top: 640px; font: 900 128px/1.02 Inter; letter-spacing: -0.045em; }
#next-ul { position: absolute; left: 90px; top: 920px; width: 640px; height: 18px; background: #00C46A; transform-origin: 0 50%; }
#next-s { position: absolute; left: 90px; top: 980px; font: 700 50px/1.2 Inter; }
#next-f { position: absolute; left: 90px; top: 1160px; font: 900 64px/1 Inter; letter-spacing: -0.02em; white-space: nowrap; }
""", f"""
      {BIG("next").replace(">0<", ">2<")}
      <div id="next-k">Next episode</div>
      <div id="next-ep">Ep 3</div>
      <div id="next-t">Continuous<br>batching</div>
      <div id="next-ul"></div>
      <div id="next-s">In depth</div>
      <div id="next-f">Follow <span id="next-h" data-var-text="handle">@vr_waingankar</span> →</div>
""", f"""
    {ENTER("next")}
    tl.fromTo("#next-k", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, 0.15);
    tl.fromTo("#next-ep", {{ scale: 1.6, opacity: 0, transformOrigin: "0% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "expo.out" }}, 0.3);
    {CLIP("#next-t", 1.35, 0.5)}
    tl.fromTo("#next-ul", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power3.inOut" }}, 2.0);
    tl.fromTo("#next-s", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 2.85);
    {CLIP("#next-f", 3.5, 0.5)}
""")

os.makedirs(f"{OUT}/compositions", exist_ok=True)
for k, v in S.items():
    open(f"{OUT}/compositions/{k}.html", "w").write(v)
print("wrote", list(S))
