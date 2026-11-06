"""Generate ep05 (Caching: the three layers) scene files. usage: python gen_scenes.py <project_dir>
Shared look/helpers: .claude/skills/reel-series/scripts/reel_lib.py. Beat times are scene-relative seconds synced to the VO words.
Never give an element the id "<scene>-w" (that's the scene wrapper)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.claude/skills/reel-series/scripts"))
from reel_lib import BASE, BIG, ENTER, EXIT, gauge, gpu, scene

OUT = sys.argv[1]
S = {}
CLIP = lambda sel, t, d=0.45: f'tl.fromTo("{sel}", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: {d}, ease: "power3.inOut" }}, {t});'
KICK = lambda n, t=0.15: f'tl.fromTo("#{n}-kick", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, {t});'
POP = lambda sel, t, st=0.0: f'tl.fromTo("{sel}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, stagger: {st}, ease: "back.out(1.8)" }}, {t});'
RED = "#D9442B"
REDH = f"repeating-linear-gradient(45deg, {RED} 0 7px, #E8806C 7px 14px)"
TINT = ["#14213D", "#2B3B60", "#3E5280", "#576A99"]
DUR = dict(hook=5.933, intro=4.0, recap=7.133, why=5.933, repeat=6.567, what=4.5, kv=10.333, prefix=9.367, semantic=9.2,
           table=10.533, layer=6.6, next=5.533)
X = lambda n: round(DUR[n] - 0.5, 2)
B5 = lambda n: BIG(n).replace(">0<", ">5<")

# 0 hook: the barista makes the same order from scratch ------------------------------
cups = "".join(f'<div class="hk-cup pn" style="left:{90 + i * 230}px"><div class="hk-lid"></div><div class="hk-tag">from scratch</div></div>' for i in range(4))
S["hook"] = scene("hook", """
#hook-l1, #hook-l2 { position: absolute; left: 84px; font: 900 112px/1 Inter; letter-spacing: -0.035em; white-space: nowrap; }
#hook-l1 { top: 230px; } #hook-l2 { top: 370px; }
.hk-cup { top: 620px; width: 200px; height: 260px; border-radius: 0 0 40px 40px; }
.hk-lid { position: absolute; left: -14px; top: -30px; width: 220px; height: 30px; border-radius: 12px; background: #14213D; }
.hk-tag { position: absolute; left: 10px; right: 10px; top: 100px; padding: 10px 0; border-radius: 10px; background: #F6D5CE; border: 4px solid """ + RED + """; color: #14213D; font: 900 28px/1 Inter; text-align: center; }
#hook-app { position: absolute; left: 90px; top: 960px; font: 900 64px/1 Inter; white-space: nowrap; }
""", f"""
      <div id="hook-l1">Same order.</div>
      <div id="hook-l2">From <span class="g">scratch.</span></div>
      {cups}
      <div class="lb" style="left:90px;top:900px">every single time</div>
      <div id="hook-app">= most LLM apps</div>
""", f"""
    tl.fromTo(".hk-cup", {{ y: 0 }}, {{ y: -18, duration: 0.15, stagger: 0.25, yoyo: true, repeat: 1, ease: "power2.out" }}, 1.9);
    {CLIP("#hook-app", 4.5, 0.4)}
    {EXIT("hook", X("hook"))}
""")

# 1 intro ------------------------------------------------------------------------------
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
      <div id="intro-ser">AI inference, end to end · Ep 5</div>
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

# 2 recap + the four-episode caching plan ------------------------------------------
eps = [("Ep 5", "the 3 layers"), ("Ep 6", "KV caching"), ("Ep 7", "prefix caching"), ("Ep 8", "semantic caching")]
chips = "".join(f'<div class="rc-ch pn" style="top:{780 + i * 110}px"><div class="lb" style="left:24px;top:24px">{a}</div><div class="lb" style="left:160px;top:24px">{b}</div></div>' for i, (a, b) in enumerate(eps))
S["recap"] = scene("recap", """
.rc-ln { position: absolute; left: 230px; width: 760px; height: 60px; border-radius: 10px; }
.rc-ch { left: 90px; width: 900px; height: 90px; }
#recap-c0 { border-color: #00C46A; }
""", f"""
      {BIG("recap").replace(">0<", ">4<")}
      <div id="recap-kick" class="kick">Previously · Ep 4</div>
      <div id="recap-ttl" class="ttl" style="font-size:112px">Then <span class="g">caching</span></div>
      <div class="lb" style="left:90px;top:520px">CPU</div><div id="recap-a" class="rc-ln" style="top:508px;background:#14213D"></div>
      <div class="lb" style="left:90px;top:600px">GPU</div><div id="recap-b" class="rc-ln" style="top:588px;background:#00C46A"></div>
      <div class="lb" style="left:90px;top:690px;opacity:.62">async batching: GPU busy 99.4%</div>
      {chips.replace('class="rc-ch pn" style="top:780px"', 'id="recap-c0" class="rc-ch pn" style="top:780px"')}
""", f"""
    {ENTER("recap")}
    {KICK("recap")}
    tl.fromTo("#recap-a, #recap-b", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.7, stagger: 0.2, ease: "power2.out" }}, 0.7);
    {CLIP("#recap-ttl", 4.3)}
    tl.fromTo(".rc-ch", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, stagger: 0.15, ease: "expo.out" }}, 5.2);
    {EXIT("recap", X("recap"))}
""")

# 3 why: slow, expensive, repeated (C's bill) ------------------------------------------
lines = "".join(f'<div class="bl-l" style="top:{620 + i * 52}px;width:{[520, 440, 560, 480, 520, 400, 540][i]}px"></div>' for i in range(7))
reps = "".join(f'<div class="bl-r" style="top:{620 + i * 52}px;width:{[520, 440, 560, 480, 520, 400, 540][i]}px"></div>' for i in (1, 2, 4, 5))
S["why"] = scene("why", """
#why-bill { left: 90px; top: 520px; width: 640px; height: 640px; }
.bl-l { position: absolute; left: 150px; height: 26px; border-radius: 13px; background: rgba(20,33,61,.25); }
.bl-r { position: absolute; left: 150px; height: 26px; border-radius: 13px; background: """ + REDH + """; transform-origin: 0 50%; }
.wy-t { position: absolute; left: 780px; font: 900 48px/1 Inter; white-space: nowrap; }
""", f"""
      {B5("why")}
      <div id="why-kick" class="kick">Why caching</div>
      <div id="why-ttl" class="ttl" style="font-size:112px">The <span class="g">bill</span></div>
      <div id="why-bill" class="pn"><div class="lb" style="left:30px;top:30px">token bill (illustrative)</div></div>
      {lines}{reps}
      <div id="why-s" class="wy-t" style="top:600px">slow</div>
      <div id="why-e" class="wy-t" style="top:690px">costly</div>
      <div id="why-rl" class="lb" style="left:90px;top:1200px;color:{RED};font-size:44px">red = repeated work</div>
""", f"""
    {ENTER("why")}
    {KICK("why")}
    {CLIP("#why-ttl", 0.3)}
    tl.fromTo(".bl-l", {{ scaleX: 0, transformOrigin: "0 50%" }}, {{ scaleX: 1, duration: 0.25, stagger: 0.12, ease: "power2.out" }}, 0.6);
    {POP("#why-s", 2.1)}
    {POP("#why-e", 2.75)}
    tl.fromTo(".bl-r", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, stagger: 0.08, ease: "power2.out" }}, 4.85);
    {CLIP("#why-rl", 3.4, 0.4)}
    {EXIT("why", X("why"))}
""")

# 4 repeat: system prompt reprocessed, same questions answered anew --------------------------
reqs = "".join(f'<div class="rp-r" style="top:{500 + i * 92}px"><div class="rp-sp">system prompt · recomputed</div><div class="rp-u">user</div></div>' for i in range(4))
S["repeat"] = scene("repeat", """
.rp-r { position: absolute; left: 90px; width: 900px; height: 76px; }
.rp-sp { position: absolute; left: 0; top: 0; width: 700px; height: 76px; border-radius: 12px; background: #F6D5CE; border: 4px solid """ + RED + """; color: #14213D; font: 900 30px/76px Inter; padding-left: 24px; }
.rp-u { position: absolute; left: 716px; top: 0; width: 184px; height: 76px; border-radius: 12px; background: #14213D; color: #E6D8BF; font: 700 30px/76px Inter; text-align: center; }
.rp-q { position: absolute; left: 90px; width: 640px; height: 80px; border-radius: 20px; background: #F3EBDD; border: 4px solid #14213D; font: 700 34px/72px Inter; padding-left: 24px; white-space: nowrap; }
.rp-n { position: absolute; left: 760px; width: 230px; height: 80px; border-radius: 20px; background: #F6D5CE; border: 4px solid """ + RED + """; color: #14213D; font: 900 28px/80px Inter; text-align: center; }
""", f"""
      {B5("repeat")}
      <div id="repeat-kick" class="kick">Repeated work</div>
      <div id="repeat-rq">{reqs}</div>
      <div id="repeat-q1" class="rp-q" style="top:910px">How do I reset my password?</div>
      <div id="repeat-n1" class="rp-n" style="top:910px">new answer</div>
      <div id="repeat-q2" class="rp-q" style="top:1020px">How can I reset my password?</div>
      <div id="repeat-n2" class="rp-n" style="top:1020px">new answer</div>
      <div class="lb" style="left:90px;top:1140px;opacity:.62">example questions</div>
""", f"""
    {ENTER("repeat")}
    {KICK("repeat")}
    tl.fromTo("#repeat-rq .rp-r", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.3, stagger: 0.55, ease: "expo.out" }}, 0.6);
    tl.fromTo("#repeat-q1, #repeat-q2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, stagger: 0.5, ease: "expo.out" }}, 4.1);
    {POP("#repeat-n1", 4.9)}
    {POP("#repeat-n2", 5.4)}
    {EXIT("repeat", X("repeat"))}
""")

# 5-8: the building (one frame that rebuilds) -----------------------------------------------
FL = {"sem": 520, "pre": 740, "kv": 960}
NAMES = {"sem": "3 · Semantic", "pre": "2 · Prefix", "kv": "1 · KV"}
BLD_CSS = """
.fl { position: absolute; left: 90px; width: 900px; height: 200px; border: 4px dashed rgba(20,33,61,.35); border-radius: 18px; }
.fl.on { border: 5px solid #00C46A; background: #F3EBDD; box-shadow: 0 10px 0 rgba(20,33,61,.12); }
.fln { position: absolute; left: 24px; top: 20px; font: 900 34px/1 Inter; white-space: nowrap; }
.kvc { position: absolute; width: 60px; height: 60px; border-radius: 10px; background: #3E5280; color: #F3EBDD; font: 900 28px/60px Inter; text-align: center; }
.blk { position: absolute; border-radius: 12px; font: 700 30px/1 Inter; color: #F3EBDD; display: flex; align-items: center; padding-left: 20px; white-space: nowrap; }
.bub { position: absolute; height: 58px; border-radius: 16px; border: 4px solid #14213D; background: #fff; font: 700 30px/50px Inter; padding-left: 18px; white-space: nowrap; }
.stamp { position: absolute; padding: 8px 18px; border-radius: 12px; background: #00C46A; font: 900 30px/1 Inter; white-space: nowrap; }
"""
def building(n, on):
    h = []
    for k in ("sem", "pre", "kv"):
        cls = "fl on" if k in on else "fl"
        h.append(f'<div id="{n}-f{k}" class="{cls}" style="top:{FL[k]}px"><div class="fln" style="{"" if k in on else "opacity:.45"}">{NAMES[k]}</div></div>')
    return "\n      ".join(h)
def kv_content(n, shown):
    y = FL["kv"] + 90
    h = [f'<div class="kvc {n}-kp" data-layout-ignore style="left:{120 + i * 68}px;top:{y}px">KV</div>' for i in range(8)]
    h.append(f'<div id="{n}-kn" class="kvc" data-layout-ignore style="left:{120 + 8 * 68}px;top:{y}px;width:84px;background:#00C46A;color:#14213D">new</div>')
    h.append(f'<div id="{n}-ka" class="stamp" style="left:{730}px;top:{FL["kv"] + 20}px">always on</div>')
    s = "" if shown else "opacity:0;"
    return "\n      ".join(x.replace('style="', f'style="{s}', 1) for x in h)
def pre_content(n, shown):
    y = FL["pre"]
    h = [f'<div id="{n}-ps" class="blk" style="left:120px;top:{y + 70}px;width:470px;height:100px;background:#14213D">system prompt · docs</div>',
         f'<div id="{n}-pc" class="stamp" style="left:330px;top:{y + 16}px">computed once</div>']
    h += [f'<div class="blk {n}-pu" style="left:620px;top:{y + 62 + i * 42}px;width:250px;height:36px;background:#576A99;font-size:28px">request {i + 1}</div>' for i in range(3)]
    s = "" if shown else "opacity:0;"
    return "\n      ".join(x.replace('style="', f'style="{s}', 1) for x in h)
def sem_content(n, shown):
    y = FL["sem"]
    h = [f'<div id="{n}-q1" class="bub" style="left:120px;top:{y + 66}px;width:430px">“reset my password?”</div>',
         f'<div id="{n}-a1" class="blk" style="left:570px;top:{y + 66}px;width:150px;height:58px;background:#3E5280">answer</div>',
         f'<div id="{n}-q2" class="bub" style="left:120px;top:{y + 132}px;width:430px">“password reset how?”</div>',
         f'<div id="{n}-a2" class="blk" style="left:570px;top:{y + 132}px;width:150px;height:58px;background:#00C46A;color:#14213D">answer</div>',
         f'<div id="{n}-m" class="blk" style="left:750px;top:{y + 66}px;width:210px;height:124px;background:#14213D;font-size:28px">model</div>',
         f'<div id="{n}-mx" style="position:absolute;left:740px;top:{y + 124}px;width:230px;height:8px;background:{RED};border-radius:4px;transform:rotate(-24deg)"></div>']
    s = "" if shown else "opacity:0;"
    return "\n      ".join(x.replace('style="', f'style="{s}', 1) for x in h)

S["what"] = scene("what", BLD_CSS + ".st { position: absolute; top: 420px; height: 70px; padding: 0 24px; border: 4px solid #14213D; border-radius: 14px; background: #F3EBDD; font: 700 32px/62px Inter; white-space: nowrap; }\n", f"""
      {B5("what")}
      <div id="what-kick" class="kick">Inference caching</div>
      <div id="what-ttl" class="ttl" style="font-size:112px">Store, <span class="g">reuse</span></div>
      <div id="what-s1" class="st" style="left:90px">compute</div><div id="what-s2" class="st" style="left:340px">store</div><div id="what-s3" class="st" style="left:540px">reuse</div>
      <div id="what-bld">{building("what", set())}</div>
""", f"""
    {ENTER("what")}
    {KICK("what")}
    {CLIP("#what-ttl", 0.25)}
    {POP("#what-s1", 1.0)}
    {POP("#what-s2", 1.4)}
    {POP("#what-s3", 2.1)}
    tl.fromTo("#what-bld .fl", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.35, stagger: -0.12, ease: "back.out(1.4)" }}, 3.3)
""")

def bscene(n, on, title, kick, contents, js, exit_=False):
    css = BLD_CSS
    markup = f"""
      {B5(n)}
      <div id="{n}-kick" class="kick">{kick}</div>
      <div id="{n}-ttl" class="ttl" style="font-size:112px">{title}</div>
      {building(n, on)}
      {contents}
"""
    s = f'{CLIP(f"#{n}-ttl", 0.1)}\n    ' + js.strip()
    if exit_:
        s += "\n    " + EXIT(n, X(n))
    return scene(n, css, markup, s)

S["kv"] = bscene("kv", set(), 'KV <span class="g">caching</span>', "Layer 1 · inside one request", kv_content("kv", False) + """
      <div id="kv-l1" class="lb" style="left:90px;top:1200px">attention keys + values kept in GPU memory</div>
      <div id="kv-l2" class="lb" style="left:90px;top:1260px">new tokens load them, not recompute them</div>""", """
    tl.fromTo("#kv-l1", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.45 }, 3.8);
    tl.fromTo("#kv-l2", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.45 }, 6.6);
    tl.to("#kv-fkv", { borderStyle: "solid", borderColor: "#00C46A", backgroundColor: "#F3EBDD", duration: 0.3 }, 1.4);
    tl.to("#kv-fkv .fln", { opacity: 1, duration: 0.2 }, 1.4);
    tl.fromTo(".kv-kp", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.2, stagger: 0.08, ease: "back.out(2)" }, 2.5);
    tl.fromTo(".kv-kp", { backgroundColor: "#3E5280" }, { backgroundColor: "#14213D", duration: 0.2, stagger: 0.06 }, 3.9);
    tl.fromTo("#kv-kn", { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.3, ease: "back.out(1.6)" }, 6.4);
    tl.fromTo("#kv-ka", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, 9.25);
""")
S["prefix"] = bscene("prefix", {"kv"}, 'Prefix <span class="g">caching</span>', "Layer 2 · across requests", kv_content("prefix", True) + "\n      " + pre_content("prefix", False), """
    tl.to("#prefix-fpre", { borderStyle: "solid", borderColor: "#00C46A", backgroundColor: "#F3EBDD", duration: 0.3 }, 1.0);
    tl.to("#prefix-fpre .fln", { opacity: 1, duration: 0.2 }, 1.0);
    tl.fromTo("#prefix-ps", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }, 2.4);
    tl.to("#prefix-ps", { scale: 1.04, duration: 0.2, yoyo: true, repeat: 1 }, 4.0);
    tl.fromTo("#prefix-pc", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, 5.9);
    tl.fromTo(".prefix-pu", { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.3, stagger: 0.3, ease: "back.out(1.6)" }, 7.2);
""")
S["semantic"] = bscene("semantic", {"kv", "pre"}, 'Semantic <span class="g">caching</span>', "Layer 3 · the app layer",
    kv_content("semantic", True) + "\n      " + pre_content("semantic", True) + "\n      " + sem_content("semantic", False), """
    tl.to("#semantic-fsem", { borderStyle: "solid", borderColor: "#00C46A", backgroundColor: "#F3EBDD", duration: 0.3 }, 0.8);
    tl.to("#semantic-fsem .fln", { opacity: 1, duration: 0.2 }, 0.8);
    tl.fromTo("#semantic-q1, #semantic-a1, #semantic-m", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, stagger: 0.1, ease: "expo.out" }, 2.6);
    tl.fromTo("#semantic-q2", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }, 3.5);
    tl.fromTo("#semantic-a2", { opacity: 0, y: -66 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.inOut" }, 5.6);
    tl.to("#semantic-m", { opacity: 0.35, duration: 0.3 }, 7.5);
    tl.fromTo("#semantic-mx", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.3, ease: "power3.out" }, 7.5);
""", exit_=True)

# 9 table: which layer, when -----------------------------------------------------------------
rows = [("Every app, always", "KV", 0.35), ("Long shared system prompt", "Prefix", 2.85), ("RAG with large shared docs", "Prefix", 4.3),
        ("Agents with large stable context", "Prefix", 4.85), ("High volume, paraphrased questions", "Semantic", 7.1)]
rm = "".join(f'<div class="tb-r pn" style="top:{480 + i * 125}px"><div class="tb-u">{u}</div><div class="tb-l">{l}</div></div>' for i, (u, l, _) in enumerate(rows))
S["table"] = scene("table", """
.tb-r { left: 90px; width: 900px; height: 105px; }
.tb-u { position: absolute; left: 26px; top: 34px; font: 700 34px/1 Inter; white-space: nowrap; }
.tb-l { position: absolute; right: 20px; top: 22px; padding: 10px 20px; border-radius: 12px; background: #14213D; color: #E6D8BF; font: 900 32px/1 Inter; }
""", f"""
      {B5("table")}
      <div id="table-kick" class="kick">Use case → layer</div>
      <div id="table-ttl" class="ttl" style="font-size:112px">Which <span class="g">one?</span></div>
      <div id="table-rows">{rm}</div>
""", f"""
    {ENTER("table")}
    {KICK("table")}
    {CLIP("#table-ttl", 0.2)}
    {"".join(f'tl.fromTo("#table-rows .tb-r:nth-child({i + 1})", {{ opacity: 0, x: -50 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "expo.out" }}, {t});' + chr(10) + "    " for i, (_, _, t) in enumerate(rows))}
    {EXIT("table", X("table"))}
""")

# 10 layer them: start with prefix -----------------------------------------------------------
S["layer"] = scene("layer", BLD_CSS + "#layer-here { position: absolute; left: 640px; top: 760px; padding: 12px 24px; border-radius: 14px; background: #00C46A; font: 900 40px/1 Inter; }\n", f"""
      {B5("layer")}
      <div id="layer-kick" class="kick">Not alternatives</div>
      <div id="layer-ttl" class="ttl" style="font-size:112px">Layer <span class="g">them</span></div>
      {building("layer", {"kv", "pre", "sem"})}
      <div id="layer-here">start here</div>
      <div id="layer-lb" class="lb" style="left:90px;top:1200px;font-size:44px">the biggest win for most apps</div>
""", f"""
    {ENTER("layer")}
    {KICK("layer")}
    {CLIP("#layer-ttl", 1.8)}
    tl.fromTo("#layer-w .fl", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.35, stagger: -0.12, ease: "back.out(1.4)" }}, 0.4);
    tl.to("#layer-fpre", {{ scale: 1.04, duration: 0.3, ease: "back.out(2)" }}, 2.7);
    {POP("#layer-here", 3.3)}
    {CLIP("#layer-lb", 4.0, 0.45)}
    {EXIT("layer", X("layer"))}
""")

# 11 next --------------------------------------------------------------------------------------
S["next"] = scene("next", """
#next-k { position: absolute; left: 90px; top: 214px; font: 700 48px/1 Inter; opacity: .62; }
#next-ep { position: absolute; left: 70px; top: 270px; font: 900 360px/1 Inter; letter-spacing: -0.06em; }
#next-t { position: absolute; left: 84px; top: 660px; font: 900 150px/1 Inter; letter-spacing: -0.045em; white-space: nowrap; }
#next-ul { position: absolute; left: 90px; top: 830px; width: 640px; height: 18px; background: #00C46A; transform-origin: 0 50%; }
#next-s { position: absolute; left: 90px; top: 900px; font: 700 50px/1.2 Inter; }
#next-f { position: absolute; left: 90px; top: 1160px; font: 900 64px/1 Inter; letter-spacing: -0.02em; white-space: nowrap; }
""", f"""
      {B5("next")}
      <div id="next-k">Next episode</div>
      <div id="next-ep">Ep 6</div>
      <div id="next-t">KV caching</div>
      <div id="next-ul"></div>
      <div id="next-s">Up close: keys, values, decode</div>
      <div id="next-f">Follow <span id="next-h" data-var-text="handle">@vr_waingankar</span> →</div>
""", f"""
    {ENTER("next")}
    tl.fromTo("#next-k", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, 0.15);
    tl.fromTo("#next-ep", {{ scale: 1.6, opacity: 0, transformOrigin: "0% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "expo.out" }}, 0.3);
    {CLIP("#next-t", 1.3, 0.45)}
    tl.fromTo("#next-ul", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "power3.inOut" }}, 1.7);
    tl.fromTo("#next-s", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 1.9);
    {CLIP("#next-f", 3.1, 0.45)}
""")

os.makedirs(f"{OUT}/compositions", exist_ok=True)
for k, v in S.items():
    open(f"{OUT}/compositions/{k}.html", "w").write(v)
print("wrote", list(S))
