"""Generate ep04 (Asynchronous batching) scene files. usage: python gen_scenes.py <project_dir>
Shared look/helpers: .claude/skills/reel-series/scripts/reel_lib.py. Beat times are scene-relative seconds synced to the VO words.
Never give an element the id "<scene>-w" (that's the scene wrapper)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.claude/skills/reel-series/scripts"))
from reel_lib import BASE, BIG, ENTER, EXIT, gauge, gpu, scene

OUT = sys.argv[1]
S = {}
CLIP = lambda sel, t, d=0.45: f'tl.fromTo("{sel}", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: {d}, ease: "power3.inOut" }}, {t});'
KICK = lambda n, t=0.15: f'tl.fromTo("#{n}-kick", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, {t});'
GROW = lambda sel, t, d=0.6: f'tl.fromTo("{sel}", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: {d}, ease: "power2.out" }}, {t});'
RED = "#D9442B"
IDLE = f"repeating-linear-gradient(45deg, {RED} 0 7px, #E8806C 7px 14px)"
DUR = dict(hook=5.167, intro=4.0, recap=4.333, sync=7.933, profile=6.2, fix=5.767, streams=4.133, wrong=4.1, events=4.667,
           slots=7.467, graphs=4.567, carry=8.467, result=8.8, ships=4.7, next=4.333)
X = lambda n: round(DUR[n] - 0.5, 2)
B4 = lambda n: BIG(n).replace(">0<", ">4<")
TL_CSS = """
.ln { position: absolute; left: 230px; width: 760px; height: 90px; border-radius: 12px; background: rgba(20,33,61,.07); }
.lnl { position: absolute; left: 90px; font: 900 40px/90px Inter; white-space: nowrap; }
.bk { position: absolute; height: 90px; border-radius: 12px; transform-origin: 0 50%; font: 700 30px/90px Inter; text-align: center; white-space: nowrap; overflow: hidden; }
.bk.cpu { background: #14213D; color: #E6D8BF; }
.bk.gpu { background: #576A99; color: #F3EBDD; }
.bk.idle { background: """ + IDLE + """; }
"""
def lanes(n, rows, y0=560, gap=130):
    return "".join(f'<div class="lnl" style="top:{y0 + i * gap}px">{r}</div><div class="ln" style="top:{y0 + i * gap}px"></div>' for i, r in enumerate(rows))
def block(id_, kind, lane, x, w, label="", y0=560, gap=130, extra=""):
    return f'<div id="{id_}" class="bk {kind}" style="left:{230 + x}px;top:{y0 + lane * gap}px;width:{w}px;{extra}">{label}</div>'

# 0 hook: the kitchen -----------------------------------------------------------------
S["hook"] = scene("hook", """
#hook-l1, #hook-l2 { position: absolute; left: 84px; font: 900 128px/1 Inter; letter-spacing: -0.035em; white-space: nowrap; }
#hook-l1 { top: 230px; } #hook-l2 { top: 380px; }
.kt { position: absolute; top: 580px; width: 430px; height: 420px; }
.burn { position: absolute; width: 130px; height: 130px; border-radius: 50%; border: 10px solid rgba(20,33,61,.3); }
#hook-board { position: absolute; left: 60px; top: 230px; width: 310px; height: 120px; border-radius: 14px; background: #E6D8BF; border: 4px solid #14213D; }
#hook-knife { position: absolute; left: 150px; top: 150px; width: 16px; height: 140px; border-radius: 8px; background: #14213D; transform-origin: 50% 100%; }
""", f"""
      <div id="hook-l1">Your GPU,</div>
      <div id="hook-l2"><span class="g">waiting</span></div>
      <div class="kt pn" style="left:90px"><div class="lb" style="left:30px;top:30px">CPU · the prep cook</div><div id="hook-board"></div><div id="hook-knife"></div></div>
      <div class="kt pn" style="left:560px"><div class="lb" style="left:30px;top:30px">GPU · the stove</div>
        <div class="burn" style="left:60px;top:120px"></div><div class="burn" style="left:230px;top:120px"></div>
        <div class="burn" style="left:60px;top:270px"></div><div class="burn" style="left:230px;top:270px"></div></div>
      <div id="hook-idle" class="lb" style="left:560px;top:1040px;color:{RED};font-size:44px">idle ~24% of the time</div>
""", f"""
    tl.fromTo("#hook-knife", {{ rotation: 0 }}, {{ rotation: -28, duration: 0.18, yoyo: true, repeat: 13, ease: "power1.inOut" }}, 0.2);
    tl.fromTo(".burn", {{ borderColor: "rgba(20,33,61,.3)" }}, {{ borderColor: "{RED}", duration: 0.25, stagger: 0.08 }}, 1.8);
    {CLIP("#hook-idle", 1.9, 0.4)}
    {EXIT("hook", X("hook"))}
""")

# 1 intro -----------------------------------------------------------------------------------
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
      <div id="intro-ser">AI inference, end to end · Ep 4</div>
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

# 2 recap -----------------------------------------------------------------------------------
TINT = ["#14213D", "#2B3B60", "#3E5280", "#576A99"]
row = "".join(f'<div class="rc-t" style="left:{90 + k * 42}px;background:{TINT[[0]*6+[1]*3+[2]*8+[3]*4][k] if False else TINT[(0 if k < 6 else 1 if k < 9 else 2 if k < 17 else 3)]}"></div>' for k in range(21))
S["recap"] = scene("recap", """
.rc-t { position: absolute; top: 620px; width: 38px; height: 60px; border-radius: 8px; }
#recap-st { position: absolute; left: 90px; top: 800px; padding: 18px 30px; border: 6px solid #00C46A; border-radius: 18px; font: 900 72px/1 Inter; transform-origin: 0% 50%; }
""", f"""
      {BIG("recap").replace(">0<", ">3<")}
      <div id="recap-kick" class="kick">Previously · Ep 3</div>
      <div id="recap-ttl" class="ttl" style="font-size:96px">Continuous <span class="g">batching</span></div>
      <div class="lb" style="left:90px;top:560px;opacity:.62">one ragged row, refilled every step</div>
      <div id="recap-row">{row}</div>
      <div id="recap-st">+ async</div>
""", f"""
    {ENTER("recap")}
    {KICK("recap")}
    {CLIP("#recap-ttl", 0.7)}
    tl.fromTo("#recap-row .rc-t", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.2, stagger: 0.03, ease: "expo.out" }}, 0.4);
    tl.fromTo("#recap-st", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, 3.6);
    {EXIT("recap", X("recap"))}
""")

# 3 sync: CPU and GPU take turns ----------------------------------------------------------
sync_bk = (block("sync-g1", "gpu", 1, 0, 230, "compute") + block("sync-ci1", "idle", 0, 0, 230) +
           block("sync-c1", "cpu", 0, 230, 200, "prep") + block("sync-gi1", "idle", 1, 230, 200) +
           block("sync-g2", "gpu", 1, 430, 200) + block("sync-ci2", "idle", 0, 430, 200) +
           block("sync-c2", "cpu", 0, 630, 130) + block("sync-gi2", "idle", 1, 630, 130))
S["sync"] = scene("sync", TL_CSS, f"""
      {B4("sync")}
      <div id="sync-kick" class="kick">The problem</div>
      <div id="sync-ttl" class="ttl" style="font-size:112px">Taking <span class="g">turns</span></div>
      <div class="lb" style="left:90px;top:500px;opacity:.62">time →</div>
      {lanes("sync", ["CPU", "GPU"])}
      {sync_bk}
      <div id="sync-lb" class="lb" style="left:90px;top:860px;color:{RED}">red = waiting · they never overlap</div>
""", f"""
    {ENTER("sync")}
    {KICK("sync")}
    {CLIP("#sync-ttl", 0.6)}
    {GROW("#sync-g1", 2.2, 1.2)}
    {GROW("#sync-ci1", 3.65, 0.5)}
    {GROW("#sync-c1", 5.4, 0.9)}
    {GROW("#sync-gi1", 6.9, 0.4)}
    {GROW("#sync-g2, #sync-ci2", 7.15, 0.3)}
    {GROW("#sync-c2, #sync-gi2", 7.3, 0.25)}
    {CLIP("#sync-lb", 4.1, 0.4)}
    {EXIT("sync", X("sync"))}
""")

# 4 profile: 300.6 s, 24% idle ----------------------------------------------------------
S["profile"] = scene("profile", """
#profile-sec { position: absolute; left: 80px; top: 470px; font: 900 220px/1 Inter; letter-spacing: -0.05em; }
.pf-bar { position: absolute; left: 90px; top: 860px; width: 900px; height: 90px; border-radius: 16px; overflow: hidden; background: #576A99; }
#profile-idle { position: absolute; right: 0; top: 0; bottom: 0; width: 24%; background: """ + IDLE + """; transform-origin: 100% 50%; }
""", f"""
      {B4("profile")}
      <div id="profile-kick" class="kick">One profile · 8B model · batch 32 · 8K tokens</div>
      <div id="profile-sec"><span id="profile-n">0</span> s</div>
      <div class="lb" style="left:90px;top:800px">total generation time</div>
      <div class="pf-bar"><div id="profile-idle"></div></div>
      <div id="profile-l1" class="lb" style="left:90px;top:980px;color:{RED};font-size:44px">24% with the GPU idle</div>
      <div id="profile-l2" class="lb" style="left:90px;top:1060px">no CPU overhead → about 228 s</div>
""", f"""
    {ENTER("profile")}
    {KICK("profile")}
    tl.fromTo("#profile-n", {{ textContent: 0 }}, {{ textContent: 300.6, duration: 1.0, snap: {{ textContent: 0.1 }}, ease: "power2.out" }}, 1.5);
    {GROW("#profile-idle", 4.9, 0.4)}
    {CLIP("#profile-l1", 3.6, 0.35)}
    {CLIP("#profile-l2", 2.9, 0.4)}
    {EXIT("profile", X("profile"))}
""")

# 5 fix: overlap N+1 prep with N compute --------------------------------------------------
fix_bk = (block("fix-g1", "gpu", 1, 0, 360, "batch N") + block("fix-c1", "cpu", 0, 40, 260, "prep N+1") +
          block("fix-g2", "gpu", 1, 370, 360, "batch N+1") + block("fix-c2", "cpu", 0, 410, 260, "prep N+2"))
S["fix"] = scene("fix", TL_CSS, f"""
      {B4("fix")}
      <div id="fix-kick" class="kick">The fix</div>
      <div id="fix-ttl" class="ttl" style="font-size:112px"><span class="g">Overlap</span></div>
      <div class="lb" style="left:90px;top:500px;opacity:.62">time →</div>
      {lanes("fix", ["CPU", "GPU"])}
      {fix_bk}
      <div id="fix-lb" class="lb" style="left:90px;top:860px">CPU builds the next batch while the GPU runs this one</div>
""", f"""
    {ENTER("fix")}
    {KICK("fix")}
    {CLIP("#fix-ttl", 0.3)}
    {GROW("#fix-c1", 1.4, 0.8)}
    {GROW("#fix-g1", 3.6, 0.6)}
    {GROW("#fix-g2", 3.85, 0.4)}
    {GROW("#fix-c2", 3.85, 0.35)}
    {CLIP("#fix-lb", 2.2, 0.45)}
    {EXIT("fix", X("fix"))}
""")

# 6-8: streams, wrong, events (one frame that rebuilds) -----------------------------------
ST = ["H2D · inputs in", "compute", "D2H · outputs out"]
def st_lanes():
    return "".join(f'<div class="lnl" style="top:{560 + i * 130}px;font-size:30px;width:130px;line-height:1.1;padding-top:16px">{["H2D", "compute", "D2H"][i]}</div><div class="ln" style="top:{560 + i * 130}px"></div>' for i in range(3))
STREAM_CSS = TL_CSS + """
.ev { position: absolute; width: 8px; height: 80px; background: #00C46A; border-radius: 4px; transform-origin: 50% 0; }
"""
ordered = block("{n}-h", "cpu", 0, 0, 220, "inputs in") + block("{n}-k", "gpu", 1, 220, 320, "compute") + block("{n}-o", "cpu", 2, 540, 220, "outputs out")
S["streams"] = scene("streams", STREAM_CSS, f"""
      {B4("streams")}
      <div id="streams-kick" class="kick">Step 1</div>
      <div id="streams-ttl" class="ttl" style="font-size:112px">CUDA <span class="g">streams</span></div>
      <div class="lb" style="left:90px;top:500px;opacity:.62">3 GPU queues that can run at once</div>
      {st_lanes()}
      {ordered.replace("{n}", "streams")}
""", f"""
    {ENTER("streams")}
    {KICK("streams")}
    {CLIP("#streams-ttl", 0.2)}
    {GROW("#streams-h", 1.95, 0.4)}
    {GROW("#streams-k", 2.6, 0.4)}
    {GROW("#streams-o", 3.25, 0.4)}
""")
S["wrong"] = scene("wrong", STREAM_CSS + "#wrong-st { position: absolute; left: 600px; top: 960px; padding: 14px 30px; border: 6px solid " + RED + "; border-radius: 16px; font: 900 72px/1 Inter; color: " + RED + "; transform: rotate(-6deg); }\n", f"""
      {B4("wrong")}
      <div id="wrong-kick" class="kick">Step 1 · no ordering</div>
      <div id="wrong-ttl" class="ttl" style="font-size:112px">Launch <span class="g">freely</span></div>
      <div class="lb" style="left:90px;top:500px;opacity:.62">3 GPU queues that can run at once</div>
      {st_lanes()}
      {ordered.replace("{n}", "wrong")}
      <div id="wrong-lb" class="lb" style="left:90px;top:960px">all start together</div>
      <div id="wrong-sw"><div id="wrong-st">wrong</div></div>
""", f"""
    {CLIP("#wrong-ttl", 0.1)}
    tl.to("#wrong-k", {{ x: -220, duration: 0.35, ease: "power3.inOut" }}, 0.4);
    tl.to("#wrong-o", {{ x: -540, duration: 0.35, ease: "power3.inOut" }}, 0.4);
    {CLIP("#wrong-lb", 0.8, 0.35)}
    tl.fromTo("#wrong-sw", {{ opacity: 0, scale: 1.8 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, 3.5);
""")
S["events"] = scene("events", STREAM_CSS, f"""
      {B4("events")}
      <div id="events-kick" class="kick">Step 2</div>
      <div id="events-ttl" class="ttl" style="font-size:112px">CUDA <span class="g">events</span></div>
      <div class="lb" style="left:90px;top:500px;opacity:.62">record → wait: each stream waits for the last</div>
      {st_lanes()}
      {ordered.replace("{n}", "events")}
      <div id="events-e1" class="ev" style="left:{230 + 218}px;top:{560 + 90}px"></div>
      <div id="events-e2" class="ev" style="left:{230 + 538}px;top:{560 + 220}px"></div>
      <div id="events-lb" class="lb" style="left:90px;top:960px">CPU blocks once per step: on outputs out</div>
""", f"""
    tl.set("#events-k", {{ x: -220 }}, 0);
    tl.set("#events-o", {{ x: -540 }}, 0);
    {CLIP("#events-ttl", 0.35)}
    tl.to("#events-k, #events-o", {{ x: 0, duration: 0.45, ease: "power3.inOut" }}, 1.05);
    tl.fromTo("#events-e1, #events-e2", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.2, stagger: 0.25, ease: "back.out(2)" }}, 1.5);
    {CLIP("#events-lb", 1.9, 0.4)}
    {EXIT("events", X("events"))}
""")

# 9 slots A/B ------------------------------------------------------------------------------
S["slots"] = scene("slots", """
.sl { position: absolute; top: 560px; width: 420px; height: 300px; }
.sl .nm { position: absolute; left: 30px; top: 24px; font: 900 96px/1 Inter; }
.sl .rl { position: absolute; left: 30px; top: 170px; font: 700 36px/1.2 Inter; white-space: nowrap; }
""", f"""
      {B4("slots")}
      <div id="slots-kick" class="kick">Step 3 · double buffering</div>
      <div id="slots-ttl" class="ttl" style="font-size:112px">Slots <span class="g">A + B</span></div>
      <div id="slots-a" class="sl pn" style="left:90px"><div class="nm">A</div><div class="rl"><span id="slots-ra">GPU reads</span></div></div>
      <div id="slots-b" class="sl pn" style="left:570px"><div class="nm">B</div><div class="rl"><span id="slots-rb">CPU writes</span></div></div>
      <div id="slots-l1" class="lb" style="left:90px;top:920px">they swap every step</div>
      <div id="slots-l2" class="lb" style="left:90px;top:990px">no overwriting data the GPU still reads</div>
      <div id="slots-l3" class="lb" style="left:90px;top:1060px;opacity:.62">cost: ~2× memory for input/output tensors</div>
""", f"""
    {ENTER("slots")}
    {KICK("slots")}
    {CLIP("#slots-ttl", 0.3)}
    tl.fromTo("#slots-a", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, 1.7);
    tl.fromTo("#slots-b", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, 2.15);
    tl.to("#slots-a", {{ borderColor: "#00C46A", duration: 0.15 }}, 2.6);
    tl.to("#slots-a", {{ borderColor: "#14213D", duration: 0.15 }}, 3.4);
    tl.to("#slots-b", {{ borderColor: "#00C46A", duration: 0.15 }}, 3.4);
    tl.set("#slots-ra", {{ textContent: "CPU writes" }}, 3.4);
    tl.set("#slots-rb", {{ textContent: "GPU reads" }}, 3.4);
    {CLIP("#slots-l1", 2.7, 0.35)}
    {CLIP("#slots-l2", 4.7, 0.4)}
    {CLIP("#slots-l3", 4.3, 0.4)}
    {EXIT("slots", X("slots"))}
""")

# 10 graphs + memory pool ------------------------------------------------------------------
def gicon(x):
    pts = [(60, 60), (160, 40), (110, 140), (220, 130)]
    dots = "".join(f'<div style="position:absolute;left:{x + px}px;top:{565 + int(py * 0.7)}px;width:34px;height:34px;border-radius:50%;background:#14213D"></div>' for px, py in pts)
    return dots
S["graphs"] = scene("graphs", """
.gp { position: absolute; top: 540px; width: 420px; height: 260px; }
#graphs-pool { position: absolute; left: 90px; top: 860px; width: 900px; height: 110px; border-radius: 16px; background: #576A99; transform-origin: 0 50%; }
""", f"""
      {B4("graphs")}
      <div id="graphs-kick" class="kick">Step 3 · CUDA graphs</div>
      <div id="graphs-ttl" class="ttl" style="font-size:112px">One <span class="g">pool</span></div>
      <div id="graphs-a" class="gp pn" style="left:90px"><div class="lb" style="left:24px;top:200px">graph for slot A</div></div>
      <div id="graphs-b" class="gp pn" style="left:570px"><div class="lb" style="left:24px;top:200px">graph for slot B</div></div>
      <div id="graphs-ga">{gicon(110)}</div><div id="graphs-gb">{gicon(590)}</div>
      <div id="graphs-pool"><div class="lb" style="left:30px;top:36px;color:#F3EBDD">shared memory pool</div></div>
      <div id="graphs-lb" class="lb" style="left:90px;top:1010px">never run together · sized to the largest graph</div>
""", f"""
    {ENTER("graphs")}
    {KICK("graphs")}
    {CLIP("#graphs-ttl", 2.9)}
    tl.fromTo("#graphs-a, #graphs-ga", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, 0.5);
    tl.fromTo("#graphs-b, #graphs-gb", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, 1.1);
    {GROW("#graphs-pool", 2.9, 0.5)}
    {CLIP("#graphs-lb", 2.0, 0.4)}
    {EXIT("graphs", X("graphs"))}
""")

# 11 carry-over ----------------------------------------------------------------------------
def toks(id_, y, vals, hi=None):
    h = ""
    for k, v in enumerate(vals):
        bg = "#F3EBDD;border:4px dashed #D9442B;color:#D9442B" if k == hi else TINT[k % 4] + ";color:#F3EBDD"
        h += f'<div {"id=" + chr(34) + id_ + "-x" + chr(34) if k == hi else ""} class="cv" style="left:{230 + k * 130}px;top:{y}px;background:{bg}">{v}</div>'
    return h
S["carry"] = scene("carry", """
.cv { position: absolute; width: 110px; height: 90px; border-radius: 12px; font: 900 40px/82px Inter; text-align: center; }
.cl { position: absolute; left: 90px; font: 700 30px/1.1 Inter; width: 130px; }
#carry-arrow { position: absolute; left: 540px; top: 660px; width: 10px; height: 200px; background: #00C46A; border-radius: 5px; transform-origin: 50% 0; }
""", f"""
      {B4("carry")}
      <div id="carry-kick" class="kick">Step 4</div>
      <div id="carry-ttl" class="ttl" style="font-size:112px">Carry-<span class="g">over</span></div>
      <div class="cl" style="top:590px">batch N output</div>
      {toks("carry-o", 570, ["t", "t", "t", "t"])}
      <div class="cl" style="top:890px">batch N+1 input</div>
      {toks("carry-i", 870, ["t", "t", "?", "t"], hi=2)}
      <div id="carry-arrow"></div>
      <div class="cl" style="top:1010px">carry-over mask</div>
      <div id="carry-mask" class="lb" style="left:230px;top:1020px;font-size:40px">[ −1, −1, 2, −1 ]</div>
      <div id="carry-lb" class="lb" style="left:90px;top:1120px">token not made yet → write 0, patch it on the GPU</div>
""", f"""
    {ENTER("carry")}
    {KICK("carry")}
    {CLIP("#carry-ttl", 0.3)}
    tl.fromTo("#carry-i-x", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, 0.9);
    tl.set("#carry-i-x", {{ textContent: "0" }}, 2.8);
    tl.to("#carry-i-x", {{ scale: 1.15, duration: 0.15, yoyo: true, repeat: 1 }}, 2.8);
    {CLIP("#carry-mask", 4.7, 0.4)}
    {CLIP("#carry-lb", 2.2, 0.45)}
    tl.fromTo("#carry-arrow", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.4, ease: "power3.out" }}, 5.7);
    tl.set("#carry-i-x", {{ textContent: "t", backgroundColor: "#3E5280", color: "#F3EBDD", borderStyle: "solid", borderColor: "#00C46A" }}, 6.2);
    {EXIT("carry", X("carry"))}
""")

# 12 result: two stopwatches + busy meters --------------------------------------------------
S["result"] = scene("result", """
.rw { position: absolute; top: 470px; width: 430px; height: 300px; }
.rw .v { position: absolute; left: 30px; top: 90px; font: 900 110px/1 Inter; letter-spacing: -0.04em; }
.mt { position: absolute; left: 90px; width: 900px; height: 60px; border-radius: 30px; background: rgba(20,33,61,.12); overflow: hidden; }
.mf { position: absolute; inset: 0; border-radius: 30px; transform-origin: 0 50%; }
#result-badge { position: absolute; left: 90px; top: 1150px; padding: 16px 34px; border-radius: 18px; background: #00C46A; font: 900 80px/1 Inter; transform-origin: 0% 50%; }
""", f"""
      {B4("result")}
      <div id="result-kick" class="kick">Same model · same GPU</div>
      <div class="rw pn" style="left:90px"><div class="lb" style="left:30px;top:30px">synchronous</div><div class="v"><span id="result-s">0</span>s</div></div>
      <div class="rw pn" style="left:560px;border-color:#00C46A"><div class="lb" style="left:30px;top:30px">asynchronous</div><div class="v"><span id="result-a">0</span>s</div></div>
      <div class="lb" style="left:90px;top:820px">GPU busy · sync 76.0%</div>
      <div class="mt" style="top:870px"><div id="result-m1" class="mf" style="background:#576A99;width:76%"></div></div>
      <div class="lb" style="left:90px;top:960px">GPU busy · async 99.4%</div>
      <div class="mt" style="top:1010px"><div id="result-m2" class="mf" style="background:#00C46A;width:99.4%"></div></div>
      <div id="result-badge">22% faster</div>
      <div id="result-cap" class="lb" style="left:520px;top:1172px;opacity:.62">ceiling was 24%</div>
""", f"""
    {ENTER("result")}
    {KICK("result")}
    tl.fromTo("#result-s", {{ textContent: 0 }}, {{ textContent: 300.6, duration: 1.4, snap: {{ textContent: 0.1 }}, ease: "power1.out" }}, 0.3);
    tl.fromTo("#result-a", {{ textContent: 0 }}, {{ textContent: 234.5, duration: 1.1, snap: {{ textContent: 0.1 }}, ease: "power1.out" }}, 0.3);
    {GROW("#result-m2", 1.4, 0.9)}
    tl.to("#result-m2", {{ opacity: 0.6, duration: 0.2, yoyo: true, repeat: 3 }}, 2.7);
    {GROW("#result-m1", 5.5, 0.7)}
    tl.fromTo("#result-badge", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, 7.1);
    {CLIP("#result-cap", 7.4, 0.35)}
    {EXIT("result", X("result"))}
""")

# 13 ships ----------------------------------------------------------------------------------
S["ships"] = scene("ships", """
#ships-chip { position: absolute; left: 90px; top: 520px; padding: 24px 36px; border: 5px solid #14213D; border-radius: 18px; background: #F3EBDD; font: 900 64px/1 Inter; white-space: nowrap; }
""", f"""
      {B4("ships")}
      <div id="ships-kick" class="kick">Where it lives</div>
      <div id="ships-ttl" class="ttl" style="font-size:112px">It <span class="g">ships</span></div>
      <div id="ships-chip">Hugging Face transformers</div>
      <div id="ships-l1" class="lb" style="left:90px;top:700px;font-size:44px">ContinuousBatchingAsyncIOs</div>
      <div id="ships-l2" class="lb" style="left:90px;top:800px;font-size:44px">for long generations · 16K+ tokens, e.g. RL</div>
""", f"""
    {ENTER("ships")}
    {KICK("ships")}
    {CLIP("#ships-ttl", 0.2)}
    tl.fromTo("#ships-chip", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }}, 0.75);
    {CLIP("#ships-l1", 1.4, 0.4)}
    {CLIP("#ships-l2", 1.9, 0.45)}
    {EXIT("ships", X("ships"))}
""")

# 14 next -----------------------------------------------------------------------------------
S["next"] = scene("next", """
#next-k { position: absolute; left: 90px; top: 214px; font: 700 48px/1 Inter; opacity: .62; }
#next-ep { position: absolute; left: 70px; top: 270px; font: 900 360px/1 Inter; letter-spacing: -0.06em; }
#next-t { position: absolute; left: 84px; top: 660px; font: 900 150px/1 Inter; letter-spacing: -0.045em; }
#next-ul { position: absolute; left: 90px; top: 830px; width: 640px; height: 18px; background: #00C46A; transform-origin: 0 50%; }
#next-s { position: absolute; left: 90px; top: 900px; font: 700 50px/1.2 Inter; }
#next-f { position: absolute; left: 90px; top: 1160px; font: 900 64px/1 Inter; letter-spacing: -0.02em; white-space: nowrap; }
""", f"""
      {B4("next")}
      <div id="next-k">Next episode</div>
      <div id="next-ep">Ep 5</div>
      <div id="next-t">Caching</div>
      <div id="next-ul"></div>
      <div id="next-s">Reusing the KV cache</div>
      <div id="next-f">Follow <span id="next-h" data-var-text="handle">@vr_waingankar</span> →</div>
""", f"""
    {ENTER("next")}
    tl.fromTo("#next-k", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, 0.15);
    tl.fromTo("#next-ep", {{ scale: 1.6, opacity: 0, transformOrigin: "0% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "expo.out" }}, 0.3);
    {CLIP("#next-t", 1.3, 0.45)}
    tl.fromTo("#next-ul", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "power3.inOut" }}, 1.6);
    tl.fromTo("#next-s", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 1.7);
    {CLIP("#next-f", 2.1, 0.45)}
""")

os.makedirs(f"{OUT}/compositions", exist_ok=True)
for k, v in S.items():
    open(f"{OUT}/compositions/{k}.html", "w").write(v)
print("wrote", list(S))
