"""Generate ep06 (KV caching) scene files. usage: python gen_scenes.py <project_dir>
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
LRED = "#F6D5CE"
TINT = ["#14213D", "#2B3B60", "#3E5280", "#576A99"]
DUR = dict(hook=4.733, intro=4.0, recap=4.867, qkv=7.4, attn=7.867, auto=2.6, without=9.067, cache=7.0, lookup=5.0, compare=3.6,
           scope=7.033, found=5.133, next=4.967)
X = lambda n: round(DUR[n] - 0.5, 2)
B6 = lambda n: BIG(n).replace(">0<", ">6<")
CSS = """
.tk { position: absolute; width: 84px; height: 84px; border-radius: 14px; background: #3E5280; color: #F3EBDD; font: 900 30px/84px Inter; text-align: center; }
.mini { position: absolute; width: 34px; height: 34px; border-radius: 6px; background: #3E5280; }
.lbl { position: absolute; font: 700 34px/1.2 Inter; white-space: nowrap; }
.tag { position: absolute; padding: 10px 20px; border-radius: 12px; font: 900 32px/1 Inter; white-space: nowrap; }
"""
def grid99(n, x, y, cls, color, step=40, cols=11):
    return "".join(f'<div class="mini {n}-{cls}" data-layout-ignore style="left:{x + (i % cols) * step}px;top:{y + (i // cols) * step}px;background:{color}"></div>' for i in range(99))

# 0 hook --------------------------------------------------------------------------------------
S["hook"] = scene("hook", CSS + """
#hook-l1, #hook-l2 { position: absolute; left: 84px; font: 900 112px/1 Inter; letter-spacing: -0.035em; white-space: nowrap; }
#hook-l1 { top: 230px; } #hook-l2 { top: 370px; }
#hook-100 { left: 640px; top: 640px; width: 300px; height: 300px; border-radius: 30px; font: 900 120px/300px Inter; background: #00C46A; color: #14213D; }
""", f"""
      <div id="hook-l1">Token 100</div>
      <div id="hook-l2">re-reads <span class="g">1–99?</span></div>
      {grid99("hook", 90, 600, "c", "#3E5280")}
      <div id="hook-100" class="tk">100</div>
      <div class="lbl" style="left:90px;top:980px">tokens 1–99</div>
""", f"""
    tl.fromTo("#hook-100", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.2, yoyo: true, repeat: 1 }}, 1.1);
    tl.to(".hook-c", {{ backgroundColor: "{RED}", duration: 0.08, stagger: {{ each: 0.008, from: "end" }} }}, 2.9);
    {EXIT("hook", X("hook"))}
""")

# 1 intro --------------------------------------------------------------------------------------
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
      <div id="intro-ser">AI inference, end to end · Ep 6</div>
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

# 2 recap: the building, floor 1 lights -----------------------------------------------------------
FL = [("3 · Semantic", 520), ("2 · Prefix", 700), ("1 · KV", 880)]
fl = "".join(f'<div id="recap-f{i}" class="rf" style="top:{y}px"><div class="lbl" style="left:24px;top:20px">{t}</div></div>' for i, (t, y) in enumerate(FL))
S["recap"] = scene("recap", CSS + ".rf { position: absolute; left: 90px; width: 900px; height: 160px; border: 5px solid #00C46A; border-radius: 18px; background: #F3EBDD; }\n", f"""
      {BIG("recap").replace(">0<", ">5<")}
      <div id="recap-kick" class="kick">Previously · Ep 5</div>
      <div id="recap-ttl" class="ttl" style="font-size:112px">Three <span class="g">layers</span></div>
      {fl}
""", f"""
    {ENTER("recap")}
    {KICK("recap")}
    {CLIP("#recap-ttl", 0.25)}
    tl.fromTo(".rf", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.3, stagger: -0.15, ease: "back.out(1.4)" }}, 0.8);
    tl.to("#recap-f0, #recap-f1", {{ opacity: 0.35, duration: 0.3 }}, 3.1);
    tl.to("#recap-f2", {{ scale: 1.05, backgroundColor: "#00C46A", duration: 0.3, ease: "back.out(2)" }}, 3.15);
    {EXIT("recap", X("recap"))}
""")

# 3 qkv: three vectors ---------------------------------------------------------------------------
def vec(id_, y, letter, color, label):
    cells = "".join(f'<div class="mini" data-layout-ignore style="left:{380 + k * 44}px;top:{y + 22}px;background:{color}"></div>' for k in range(8))
    return f'<div id="{id_}" class="qv"><div class="tag" style="left:200px;top:{y + 14}px;background:{color};color:#F3EBDD">{letter}</div>{cells}<div class="lbl" style="left:740px;top:{y + 20}px;font-size:32px">{label}</div></div>'
S["qkv"] = scene("qkv", CSS, f"""
      {B6("qkv")}
      <div id="qkv-kick" class="kick">Inside attention</div>
      <div id="qkv-ttl" class="ttl" style="font-size:112px">Q, K, <span class="g">V</span></div>
      <div id="qkv-tok" class="tk" style="left:90px;top:640px">tok</div>
      {vec("qkv-q", 520, "Q", "#14213D", "looking for")}
      {vec("qkv-k", 660, "K", "#3E5280", "offers")}
      {vec("qkv-v", 800, "V", "#576A99", "carries")}
      <div id="qkv-lb" class="lbl" style="left:90px;top:980px">every token gets all three</div>
""", f"""
    {ENTER("qkv")}
    {KICK("qkv")}
    {CLIP("#qkv-ttl", 0.3)}
    {POP("#qkv-tok", 0.4)}
    {CLIP("#qkv-lb", 1.3, 0.4)}
    tl.fromTo("#qkv-q", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 2.55);
    tl.fromTo("#qkv-k", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 4.25);
    tl.fromTo("#qkv-v", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 5.65);
    {EXIT("qkv", X("qkv"))}
""")

# 4 attention: query vs earlier keys, weigh values -------------------------------------------------
toks = "".join(f'<div class="tk at-t" style="left:{90 + i * 124}px;top:720px;background:{"#00C46A;color:#14213D" if i == 6 else "#3E5280"}">{"new" if i == 6 else "K"}</div>' for i in range(7))
links = "".join(f'<div class="at-l" style="left:{132 + i * 124}px;width:{(6 - i) * 124}px"></div>' for i in range(6))
scores = [0.3, 0.9, 0.5, 0.2, 0.7, 0.4]
bars = "".join(f'<div class="at-s" style="left:{100 + i * 124}px;height:{int(s * 120)}px;top:{700 - int(s * 120)}px"></div>' for i, s in enumerate(scores))
vals = "".join(f'<div class="at-v" style="left:{100 + i * 124}px;width:{int(s * 64) + 8}px"></div>' for i, s in enumerate(scores))
S["attn"] = scene("attn", CSS + """
.at-l { position: absolute; top: 830px; height: 6px; background: #00C46A; border-radius: 3px; transform-origin: 100% 50%; }
.at-s { position: absolute; width: 64px; border-radius: 8px 8px 0 0; background: #14213D; transform-origin: 50% 100%; }
.at-v { position: absolute; top: 880px; height: 50px; border-radius: 8px; background: #576A99; transform-origin: 0 50%; }
""", f"""
      {B6("attn")}
      <div id="attn-kick" class="kick">Attention</div>
      <div id="attn-ttl" class="ttl" style="font-size:112px">Query × <span class="g">keys</span></div>
      <div class="lbl" style="left:90px;top:460px;opacity:.62">earlier tokens → newest token</div>
      {bars}{toks}{links}{vals}
      <div id="attn-l1" class="lbl" style="left:90px;top:980px">scores from query · keys</div>
      <div id="attn-l2" class="lbl" style="left:90px;top:1040px">values weighted by those scores</div>
""", f"""
    {ENTER("attn")}
    {KICK("attn")}
    {CLIP("#attn-ttl", 0.3)}
    tl.fromTo(".at-t", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25, stagger: 0.06, ease: "expo.out" }}, 0.6);
    tl.fromTo(".at-l", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, stagger: 0.18, ease: "power2.out" }}, 2.75);
    tl.fromTo(".at-s", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.3, stagger: 0.05, ease: "back.out(1.6)" }}, 5.75);
    {CLIP("#attn-l1", 4.5, 0.4)}
    tl.fromTo(".at-v", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, stagger: 0.05, ease: "power2.out" }}, 6.3);
    {CLIP("#attn-l2", 5.6, 0.4)}
    {EXIT("attn", X("attn"))}
""")

# 5 & 6: autoregressive, then without cache -------------------------------------------------------
row = lambda n, k: "".join(f'<div class="tk {n}-t" style="left:{90 + i * 124}px;top:560px">{i + 1}</div>' for i in range(k))
S["auto"] = scene("auto", CSS, f"""
      {B6("auto")}
      <div id="auto-kick" class="kick">Decoding</div>
      <div id="auto-ttl" class="ttl" style="font-size:112px">One at a <span class="g">time</span></div>
      {row("auto", 7)}
""", f"""
    {ENTER("auto")}
    {KICK("auto")}
    {CLIP("#auto-ttl", 0.2)}
    tl.fromTo(".auto-t", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.15, stagger: 0.25, ease: "back.out(2)" }}, 0.4);
""")
tri = "".join(f'<div class="wo-b" style="left:{90 + i * 76}px;height:{(i + 1) * 22}px;top:{1250 - (i + 1) * 22}px"></div>' for i in range(12))
S["without"] = scene("without", CSS + f"""
.wo-b {{ position: absolute; width: 60px; border-radius: 6px 6px 0 0; background: {RED}; transform-origin: 50% 100%; }}
#without-100 {{ left: 640px; top: 600px; width: 200px; height: 200px; border-radius: 24px; font: 900 80px/200px Inter; background: #00C46A; color: #14213D; }}
""", f"""
      {B6("without")}
      <div id="without-kick" class="kick">Without a cache</div>
      <div id="without-ttl" class="ttl" style="font-size:112px">Recompute <span class="g">all</span></div>
      {grid99("without", 90, 560, "c", "#3E5280")}
      <div id="without-100" class="tk">100</div>
      <div id="without-l1" class="lbl" style="left:90px;top:940px;color:{RED}">K, V for tokens 1–99, again</div>
      <div id="without-l2" class="lbl" style="left:90px;top:1010px">work per step (illustrative)</div>
      {tri}
""", f"""
    {CLIP("#without-ttl", 0.1)}
    tl.fromTo("#without-100", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, 1.5);
    tl.to(".without-c", {{ backgroundColor: "{RED}", duration: 0.08, stagger: 0.012 }}, 2.9);
    {CLIP("#without-l1", 4.2, 0.4)}
    {CLIP("#without-l2", 6.6, 0.4)}
    tl.fromTo(".wo-b", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.2, stagger: 0.1, ease: "power2.out" }}, 7.4);
    {EXIT("without", X("without"))}
""")

# 7 & 8: with cache: saved in GPU memory, then looked up -------------------------------------------
def kvmem(n, filled):
    s = "" if filled else "opacity:0;"
    return "".join(f'<div class="mini {n}-m" data-layout-ignore style="{s}left:{120 + (i % 20) * 42}px;top:{720 + (i // 20) * 42}px;background:#14213D"></div>' for i in range(99))
WITH_CSS = CSS + """
#N-mem { position: absolute; left: 90px; top: 640px; width: 900px; height: 330px; border: 5px solid #14213D; border-radius: 20px; background: #F3EBDD; }
#N-new { left: 840px; top: 1030px; width: 150px; height: 100px; border-radius: 16px; font: 900 34px/100px Inter; background: #00C46A; color: #14213D; }
#N-arrow { position: absolute; left: 905px; top: 975px; width: 10px; height: 55px; background: #00C46A; border-radius: 5px; transform-origin: 50% 0; }
"""
def cachemarkup(n, title, kick):
    return f"""
      {B6(n)}
      <div id="{n}-kick" class="kick">{kick}</div>
      <div id="{n}-ttl" class="ttl" style="font-size:112px">{title}</div>
      <div id="{n}-mem"><div class="lbl" style="left:28px;top:18px">GPU memory · K, V for tokens 1–99</div></div>
      {kvmem(n, n != "cache")}
      <div id="{n}-arrow" style="{'' if n == 'lookup' else 'opacity:0'}"></div>
      <div id="{n}-new" class="tk" style="{'' if n == 'lookup' else 'opacity:0'}">100</div>
"""
S["cache"] = scene("cache", WITH_CSS.replace("N-", "cache-"), cachemarkup("cache", 'KV <span class="g">cache</span>', "With KV caching") +
    '\n      <div id="cache-l1" class="lbl" style="left:90px;top:1030px">computed once, then kept</div>', f"""
    {ENTER("cache")}
    {KICK("cache")}
    {CLIP("#cache-ttl", 0.5)}
    tl.fromTo("#cache-mem", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.4)" }}, 1.4)
    tl.to(".cache-m", {{ opacity: 1, duration: 0.06, stagger: 0.025 }}, 2.2);
    tl.to("#cache-mem", {{ borderColor: "#00C46A", duration: 0.3 }}, 3.7);
    {CLIP("#cache-l1", 5.2, 0.4)}
""")
S["lookup"] = scene("lookup", WITH_CSS.replace("N-", "lookup-"), cachemarkup("lookup", 'Look <span class="g">up</span>', "Each new step") +
    '\n      <div id="lookup-l1" class="lbl" style="left:90px;top:1030px">load, don’t recompute</div>\n      <div id="lookup-l2" class="lbl" style="left:90px;top:1090px">only the newest token is fresh</div>', f"""
    {CLIP("#lookup-ttl", 0.1)}
    tl.fromTo(".lookup-m", {{ backgroundColor: "#14213D" }}, {{ backgroundColor: "#00C46A", duration: 0.1, stagger: 0.006, yoyo: true, repeat: 1 }}, 1.0);
    tl.fromTo("#lookup-arrow", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.3, ease: "power3.out" }}, 1.2);
    {CLIP("#lookup-l1", 1.4, 0.4)}
    tl.fromTo("#lookup-new", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, 2.7);
    {CLIP("#lookup-l2", 2.8, 0.4)}
    {EXIT("lookup", X("lookup"))}
""")

# 9 compare: recompute 99 vs load 99 ----------------------------------------------------------------
S["compare"] = scene("compare", CSS + """
.cp { position: absolute; top: 470px; width: 430px; height: 640px; }
.cp .h { position: absolute; left: 24px; top: 24px; font: 900 44px/1 Inter; }
.cp .s { position: absolute; left: 24px; top: 540px; font: 700 34px/1.25 Inter; }
""", f"""
      {B6("compare")}
      <div id="compare-kick" class="kick">Token 100</div>
      <div class="cp pn" style="left:90px"><div class="h">without</div><div class="s" style="color:{RED}">recompute 99<br>compute 1</div></div>
      <div id="compare-r" class="cp pn" style="left:560px;border-color:#00C46A"><div class="h">with KV</div><div id="compare-s" class="s">load 99<br>compute 1</div></div>
      {grid99("compare", 120, 560, "a", RED, step=38, cols=9)}
      {grid99("compare", 590, 560, "b", "#14213D", step=38, cols=9)}
      <div id="compare-one" class="mini" style="left:{590 + 9 * 38 + 4}px;top:{560 + 10 * 38}px;width:34px;background:#00C46A"></div>
""", f"""
    {ENTER("compare")}
    {KICK("compare")}
    tl.fromTo(".compare-b", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05, stagger: 0.004 }}, 1.6);
    {CLIP("#compare-s", 1.6, 0.4)}
    {POP("#compare-one", 2.55)}
    {EXIT("compare", X("compare"))}
""")

# 10 scope: one request, automatic, on by default ------------------------------------------------------
S["scope"] = scene("scope", CSS + """
#scope-req { position: absolute; left: 90px; top: 520px; width: 900px; height: 200px; border: 5px dashed #14213D; border-radius: 20px; }
#scope-sw { position: absolute; left: 90px; top: 800px; width: 220px; height: 110px; border-radius: 55px; background: rgba(20,33,61,.2); }
#scope-kn { position: absolute; left: 10px; top: 10px; width: 90px; height: 90px; border-radius: 50%; background: #14213D; }
""", f"""
      {B6("scope")}
      <div id="scope-kick" class="kick">Scope</div>
      <div id="scope-ttl" class="ttl" style="font-size:112px">Always <span class="g">on</span></div>
      <div id="scope-req"><div class="lbl" style="left:24px;top:-50px">one request</div>{"".join(f'<div class="tk" style="left:{30 + i * 124}px;top:56px">{i + 1}</div>' for i in range(7))}</div>
      <div id="scope-sw"><div id="scope-kn"></div></div>
      <div id="scope-l1" class="lbl" style="left:350px;top:830px">automatic</div>
      <div id="scope-l2" class="lbl" style="left:90px;top:970px">on by default in every inference framework</div>
      <div id="scope-l3" class="lbl" style="left:90px;top:1030px;opacity:.62">nothing to configure</div>
""", f"""
    {ENTER("scope")}
    {KICK("scope")}
    {CLIP("#scope-ttl", 3.0)}
    tl.fromTo("#scope-req", {{ opacity: 0, scale: 0.94 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }}, 1.3);
    tl.to("#scope-kn", {{ x: 110, duration: 0.3, ease: "back.out(1.6)" }}, 3.05);
    tl.to("#scope-sw", {{ backgroundColor: "#00C46A", duration: 0.3 }}, 3.05);
    {CLIP("#scope-l1", 3.1, 0.35)}
    {CLIP("#scope-l2", 4.0, 0.45)}
    {CLIP("#scope-l3", 4.6, 0.35)}
    {EXIT("scope", X("scope"))}
""")

# 11 foundation -> prefix next -------------------------------------------------------------------
ff = "".join(f'<div id="found-f{i}" class="rf" style="top:{y}px;{"" if i == 2 else "opacity:.35"}"><div class="lbl" style="left:24px;top:20px">{t}</div></div>' for i, (t, y) in enumerate(FL))
S["found"] = scene("found", CSS + """
.rf { position: absolute; left: 90px; width: 900px; height: 160px; border: 5px solid #00C46A; border-radius: 18px; background: #F3EBDD; }
#found-f2 { background: #00C46A; }
.fd-r { position: absolute; left: 640px; width: 300px; height: 34px; border-radius: 8px; background: #576A99; }
""", f"""
      {B6("found")}
      <div id="found-kick" class="kick">The foundation</div>
      <div id="found-ttl" class="ttl" style="font-size:112px">Next <span class="g">layer</span></div>
      {ff}
      {"".join(f'<div class="fd-r found-r" style="top:{742 + i * 42}px"></div>' for i in range(3))}
      <div id="found-l1" class="lbl" style="left:90px;top:1080px">share these states across requests</div>
""", f"""
    {ENTER("found")}
    {KICK("found")}
    {CLIP("#found-ttl", 1.9)}
    tl.to("#found-f1", {{ opacity: 1, scale: 1.04, duration: 0.3, ease: "back.out(2)" }}, 1.95);
    tl.fromTo(".found-r", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 0.3, stagger: 0.15, ease: "back.out(1.6)" }}, 2.65);
    {CLIP("#found-l1", 2.7, 0.4)}
    {EXIT("found", X("found"))}
""")

# 12 next -----------------------------------------------------------------------------------------
S["next"] = scene("next", """
#next-k { position: absolute; left: 90px; top: 214px; font: 700 48px/1 Inter; opacity: .62; }
#next-ep { position: absolute; left: 70px; top: 270px; font: 900 360px/1 Inter; letter-spacing: -0.06em; }
#next-t { position: absolute; left: 84px; top: 660px; font: 900 120px/1.02 Inter; letter-spacing: -0.045em; white-space: nowrap; }
#next-ul { position: absolute; left: 90px; top: 800px; width: 640px; height: 18px; background: #00C46A; transform-origin: 0 50%; }
#next-s { position: absolute; left: 90px; top: 870px; font: 700 50px/1.2 Inter; }
#next-f { position: absolute; left: 90px; top: 1160px; font: 900 64px/1 Inter; letter-spacing: -0.02em; white-space: nowrap; }
""", f"""
      {B6("next")}
      <div id="next-k">Next episode</div>
      <div id="next-ep">Ep 7</div>
      <div id="next-t">Prefix caching</div>
      <div id="next-ul"></div>
      <div id="next-s">Compute the shared prompt once</div>
      <div id="next-f">Follow <span id="next-h" data-var-text="handle">@vr_waingankar</span> →</div>
""", f"""
    {ENTER("next")}
    tl.fromTo("#next-k", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, 0.15);
    tl.fromTo("#next-ep", {{ scale: 1.6, opacity: 0, transformOrigin: "0% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "expo.out" }}, 0.3);
    {CLIP("#next-t", 1.3, 0.45)}
    tl.fromTo("#next-ul", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "power3.inOut" }}, 1.7);
    tl.fromTo("#next-s", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 1.9);
    {CLIP("#next-f", 2.6, 0.45)}
""")

os.makedirs(f"{OUT}/compositions", exist_ok=True)
for k, v in S.items():
    open(f"{OUT}/compositions/{k}.html", "w").write(v)
print("wrote", list(S))
