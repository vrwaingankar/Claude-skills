"""Generate ep03 (Continuous batching, in depth) scene files. usage: python gen_scenes.py <project_dir>
Shared look/helpers: .claude/skills/reel-series/scripts/reel_lib.py. Beat times are scene-relative seconds synced to the VO words."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.claude/skills/reel-series/scripts"))
from reel_lib import BASE, BIG, ENTER, EXIT, gauge, gpu, scene

OUT = sys.argv[1]
S = {}
CLIP = lambda sel, t, d=0.45: f'tl.fromTo("{sel}", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: {d}, ease: "power3.inOut" }}, {t});'
KICK = lambda n, t=0.15: f'tl.fromTo("#{n}-kick", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, {t});'
RED = "#D9442B"
PAD = f"repeating-linear-gradient(45deg, {RED} 0 7px, #E8806C 7px 14px)"
TINT = ["#14213D", "#2B3B60", "#3E5280", "#576A99"]
DUR = dict(hook=4.033, intro=4.0, recap=5.267, goal=3.933, rect=6.4, decode=6.8, swap=5.967, formula=7.833, shapes=5.7,
           ragged=5.167, mask=4.667, budget=6.233, refill=5.1, sum=6.4, next=5.167)
X = lambda n: round(DUR[n] - 0.5, 2)
B3 = lambda n: BIG(n).replace(">0<", ">3<")
CELL = ".c { position: absolute; border-radius: 8px; }\n.pad { background: " + PAD + "; }\n"

# 0 hook: a truck shipping crates of foam -------------------------------------------
crates = ""
for i, h in enumerate([60, 120, 40, 90]):
    crates += f'<div class="hk-cr" style="left:{40 + i * 210}px"><div class="hk-foam"></div><div class="hk-load" style="height:{h}px"></div></div>'
S["hook"] = scene("hook", """
#hook-l1, #hook-l2 { position: absolute; left: 84px; font: 900 128px/1 Inter; letter-spacing: -0.035em; white-space: nowrap; }
#hook-l1 { top: 230px; } #hook-l2 { top: 380px; }
#hook-bed { left: 90px; top: 600px; width: 900px; height: 330px; }
.hk-cr { position: absolute; top: 80px; width: 180px; height: 200px; border: 4px solid #14213D; border-radius: 10px; overflow: hidden; background: #F3EBDD; }
.hk-foam { position: absolute; inset: 0; background: """ + PAD + """; opacity: .85; }
.hk-load { position: absolute; left: 0; right: 0; bottom: 0; background: #14213D; }
.hk-wh { position: absolute; top: 905px; width: 110px; height: 110px; border-radius: 50%; background: #14213D; border: 14px solid #F3EBDD; box-shadow: 0 0 0 4px #14213D; }
""", f"""
      <div id="hook-l1">Your GPU is</div>
      <div id="hook-l2">shipping <span class="g">air</span></div>
      <div id="hook-bed" class="pn"><div class="lb" style="left:40px;top:24px">one batch · 4 prompts</div>{crates}</div>
      <div class="hk-wh" style="left:200px"></div><div class="hk-wh" style="left:770px"></div>
      <div class="lb" style="left:90px;top:1060px">red = padding, not tokens</div>
""", f"""
    tl.fromTo("#hook-bed", {{ x: 0 }}, {{ x: 14, duration: 0.12, yoyo: true, repeat: 3, ease: "sine.inOut" }}, 0.4);
    tl.fromTo(".hk-foam", {{ opacity: 0.85 }}, {{ opacity: 0.45, duration: 0.2, stagger: 0.08, yoyo: true, repeat: 3 }}, 1.4);
    {EXIT("hook", X("hook"))}
""")

# 1 intro (same name card as earlier episodes) ------------------------------------------
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
      <div id="intro-ser">AI inference, end to end · Ep 3</div>
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

# 2 recap: static / dynamic / continuous mini grids ----------------------------------
def mini(id_, y, label, rows):
    cells = ""
    for r, row in enumerate(rows):
        for c, col in enumerate(row):
            bg = PAD if col == "i" else ("#00C46A" if col == "g" else TINT[r])
            cells += f'<div class="c" style="left:{260 + c * 44}px;top:{20 + r * 44}px;width:38px;height:38px;background:{bg}"></div>'
    return f'<div id="{id_}" class="pn rc-g" style="top:{y}px"><div class="lb" style="left:26px;top:52px">{label}</div>{cells}</div>'
S["recap"] = scene("recap", CELL + """
.rc-g { left: 90px; width: 900px; height: 160px; }
""", f"""
      {BIG("recap").replace(">0<", ">2<")}
      <div id="recap-kick" class="kick">Previously · Ep 2</div>
      <div id="recap-ttl" class="ttl" style="font-size:112px">Three <span class="g">ways</span></div>
      {mini("recap-a", 500, "Static", ["nnnnnnnnnnnnnn".replace("n", "x")[:14], "xxxxiiiiiiiiii", "xxxxxxxiiiiiii"])}
      {mini("recap-b", 700, "Dynamic", ["xxxxxxxxxxxxxx", "iiixxxxxxxxxxx", "iiiiiixxxxxxxx"])}
      {mini("recap-c", 900, "Continuous", ["xxxxxxxxxxxxxx", "xxxxggggggggggg"[:14], "xxxxxxxggggggg"])}
""", f"""
    {ENTER("recap")}
    {KICK("recap")}
    {CLIP("#recap-ttl", 0.25)}
    tl.fromTo(".rc-g", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, stagger: 0.3, ease: "expo.out" }}, 0.85);
    tl.to("#recap-a, #recap-b", {{ opacity: 0.4, duration: 0.3 }}, 3.2);
    tl.to("#recap-c", {{ borderColor: "#00C46A", scale: 1.05, duration: 0.3, ease: "back.out(2)" }}, 3.25);
    {EXIT("recap", X("recap"))}
""")

# 3 goal: tokens per second, many prompts at once ---------------------------------------
streams = "".join(f'<div class="c gl-t" style="left:{90 + c * 72}px;top:{880 + r * 80}px;width:64px;height:60px;background:{TINT[r]}"></div>' for c in range(12) for r in range(4))
S["goal"] = scene("goal", CELL, f"""
      {B3("goal")}
      <div id="goal-kick" class="kick">The goal</div>
      <div id="goal-ttl" class="ttl"><span class="g">Throughput</span></div>
      {gauge("goal-g", 90, 470, 470)}
      <div class="lb" style="left:600px;top:560px;font-size:44px">tokens / second</div>
      <div class="lb" style="left:90px;top:820px">4 prompts, in parallel</div>
      {streams}
""", f"""
    {ENTER("goal")}
    {KICK("goal")}
    {CLIP("#goal-ttl", 0.2)}
    tl.set("#goal-g-n", {{ rotation: -60, svgOrigin: "200 200" }}, 0);
    tl.to("#goal-g-n", {{ rotation: 70, duration: 0.6, svgOrigin: "200 200", ease: "back.out(1.4)" }}, 1.1);
    tl.fromTo(".gl-t", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.1, stagger: 0.025, ease: "back.out(2)" }}, 2.5);
    {EXIT("goal", X("goal"))}
""")

# 4 & 5: the padded rectangle, then decode with <eos> -------------------------------------
LENS = [6, 3, 8, 4]
GX, GY, P, RP = 90, 560, 72, 86
def rect_cells(n, with_decode, eos_row=1):
    h = []
    for r, ln in enumerate(LENS):
        for c in range(8):
            if c < 8 - ln:
                h.append(f'<div class="c pad {n}-pad" style="left:{GX + c * P}px;top:{GY + r * RP}px;width:64px;height:70px"></div>')
            else:
                h.append(f'<div class="c {n}-pr" style="left:{GX + c * P}px;top:{GY + r * RP}px;width:64px;height:70px;background:{TINT[r]}"></div>')
        if with_decode:
            for k in range(4):
                c = 8 + k
                if r == eos_row and k == 1:
                    h.append(f'<div id="{n}-eos" class="c {n}-d{k}" style="left:{GX + c * P}px;top:{GY + r * RP}px;width:64px;height:70px;background:#F3EBDD;border:4px solid #14213D;font:900 28px/62px Inter;text-align:center">eos</div>')
                elif r == eos_row and k > 1:
                    h.append(f'<div class="c pad {n}-d{k} {n}-waste" style="left:{GX + c * P}px;top:{GY + r * RP}px;width:64px;height:70px"></div>')
                else:
                    h.append(f'<div class="c {n}-d{k}" style="left:{GX + c * P}px;top:{GY + r * RP}px;width:64px;height:70px;background:{TINT[r]};opacity:.75"></div>')
    return "\n      ".join(h)

RECT_FRAME = f'<div class="rf" style="left:{GX - 14}px;top:{GY - 14}px;width:{8 * P + 20}px;height:{4 * RP + 14}px"></div>'
S["rect"] = scene("rect", CELL + ".rf { position: absolute; border: 4px solid #14213D; border-radius: 14px; }\n", f"""
      {B3("rect")}
      <div id="rect-kick" class="kick">The naive batch</div>
      <div id="rect-ttl" class="ttl"><span class="g">Rectangle</span></div>
      <div class="lb" style="left:90px;top:500px;opacity:.62">4 prompts × tokens</div>
      <div id="rect-frame">{RECT_FRAME}</div>
      {rect_cells("rect", False)}
      <div id="rect-ml" class="lb" style="left:90px;top:960px">padding on the left</div>
      <div id="rect-mask" class="lb" style="left:90px;top:1020px">attention mask: pads → 0, ignored</div>
""", f"""
    {ENTER("rect")}
    {KICK("rect")}
    {CLIP("#rect-ttl", 0.25)}
    tl.fromTo(".rect-pr", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.25, stagger: 0.02, ease: "expo.out" }}, 0.5);
    tl.fromTo("#rect-frame", {{ opacity: 0, scale: 1.08 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }}, 1.45);
    tl.fromTo(".rect-pad", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.2, stagger: 0.04, ease: "back.out(2)" }}, 3.45);
    {CLIP("#rect-ml", 3.8, 0.35)}
    {CLIP("#rect-mask", 4.3, 0.4)}
    tl.to(".rect-pad", {{ opacity: 0.45, duration: 0.3 }}, 5.75);
""")

S["decode"] = scene("decode", CELL + ".rf { position: absolute; border: 4px solid #14213D; border-radius: 14px; }\n.colh { position: absolute; top: 500px; font: 700 30px/1 Inter; opacity: .62; }\n", f"""
      {B3("decode")}
      <div id="decode-kick" class="kick">Batched generation</div>
      <div id="decode-ttl" class="ttl" style="font-size:112px">Then <span class="g">decode</span></div>
      <div class="colh" style="left:90px">prompt · prefill</div><div class="colh" style="left:{GX + 8 * P}px">decode →</div>
      {RECT_FRAME}
      {rect_cells("decode", True)}
      <div id="decode-pf" style="position:absolute;left:{GX - 6}px;top:{GY - 6}px;width:{8 * P + 4}px;height:{4 * RP}px;border-radius:12px;background:#00C46A;opacity:0"></div>
      <div id="decode-wl" class="lb" style="left:90px;top:960px;color:{RED}">wasted until the longest finishes</div>
""", f"""
    tl.set(".decode-pad", {{ opacity: 0.45 }}, 0);
    {CLIP("#decode-ttl", 0.1)}
    tl.fromTo("#decode-pf", {{ opacity: 0 }}, {{ opacity: 0.55, duration: 0.2, yoyo: true, repeat: 1, repeatDelay: 0.3 }}, 0.25);
    {"".join(f'tl.fromTo(".decode-d{k}", {{ scale: 0 }}, {{ scale: 1, duration: 0.15, ease: "back.out(2)" }}, {t});' + chr(10) + "    " for k, t in enumerate([1.8, 2.4, 3.0, 3.6]))}
    tl.fromTo("#decode-eos", {{ borderColor: "#14213D" }}, {{ borderColor: "#D9442B", duration: 0.2 }}, 4.5);
    tl.to(".decode-waste", {{ scale: 1.15, duration: 0.2, yoyo: true, repeat: 1 }}, 5.4);
    {CLIP("#decode-wl", 4.4, 0.4)}
    {EXIT("decode", X("decode"))}
""")

# 6 swap: dynamic scheduling pads everyone else --------------------------------------------
sw = []
for r in range(4):
    for c in range(8):
        x, y = GX + c * P, GY + r * RP
        if r == 1:
            if c < 7:
                sw.append(f'<div class="c swap-new" style="left:{x}px;top:{y}px;width:64px;height:70px;background:#576A99;border:3px solid #14213D"></div>')
            else:
                sw.append(f'<div class="c swap-dec" style="left:{x}px;top:{y}px;width:64px;height:70px;background:#576A99;opacity:.75"></div>')
        elif c < 7:
            sw.append(f'<div class="c pad swap-pad" style="left:{x}px;top:{y}px;width:64px;height:70px"></div>')
        else:
            sw.append(f'<div class="c swap-dec" style="left:{x}px;top:{y}px;width:64px;height:70px;background:{TINT[r]};opacity:.75"></div>')
S["swap"] = scene("swap", CELL + "#swap-cnt { position: absolute; left: 90px; top: 960px; font: 900 72px/1 Inter; color: " + RED + "; }\n", f"""
      {B3("swap")}
      <div id="swap-kick" class="kick">Dynamic scheduling</div>
      <div id="swap-ttl" class="ttl" style="font-size:112px">Swap <span class="g">in</span></div>
      <div class="lb" style="left:90px;top:500px;opacity:.62">one step: new prompt prefills, the rest decode 1 token</div>
      {"".join(sw)}
      <div class="lb" style="left:{GX + 8 * P - 60}px;top:{GY + RP + 18}px">new</div>
      <div id="swap-cnt">padding: <span id="swap-n">0</span></div>
""", f"""
    {ENTER("swap")}
    {KICK("swap")}
    {CLIP("#swap-ttl", 0.2)}
    tl.fromTo(".swap-new", {{ x: 500, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, stagger: 0.05, ease: "power3.out" }}, 0.6);
    tl.fromTo(".swap-new", {{ borderColor: "#14213D" }}, {{ borderColor: "#00C46A", duration: 0.2, yoyo: true, repeat: 1 }}, 2.2);
    tl.fromTo(".swap-dec", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 0.75, scale: 1, duration: 0.15, ease: "back.out(2)" }}, 3.5);
    tl.fromTo(".swap-pad", {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1, duration: 0.18, stagger: 0.03, ease: "back.out(2)" }}, 4.4);
    tl.fromTo("#swap-cnt", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 4.4);
    tl.fromTo("#swap-n", {{ textContent: 0 }}, {{ textContent: 18, duration: 0.6, snap: {{ textContent: 1 }}, ease: "none" }}, 4.4);
    {EXIT("swap", X("swap"))}
""")

# 7 formula: (n-1)(B-1) -> 693 ---------------------------------------------------------
S["formula"] = scene("formula", """
.fm { position: absolute; left: 90px; font: 900 120px/1 Inter; letter-spacing: -0.03em; white-space: nowrap; }
.fv { position: absolute; left: 90px; font: 700 60px/1 Inter; white-space: nowrap; }
#formula-res { position: absolute; left: 80px; top: 960px; font: 900 260px/1 Inter; letter-spacing: -0.05em; color: """ + RED + """; }
""", f"""
      {B3("formula")}
      <div id="formula-kick" class="kick">Padding per swap</div>
      <div id="formula-a" class="fm" style="top:300px">(n − 1)</div>
      <div id="formula-b" class="fm" style="top:440px">× (B − 1)</div>
      <div id="formula-v1" class="fv" style="top:640px">B = 8 prompts</div>
      <div id="formula-v2" class="fv" style="top:730px">n = 100-token newcomer</div>
      <div id="formula-v3" class="fv" style="top:830px">99 × 7 =</div>
      <div id="formula-res"><span id="formula-n">0</span></div>
      <div id="formula-lb" class="lb" style="left:90px;top:1230px">padding tokens, for one swap</div>
""", f"""
    {ENTER("formula")}
    {KICK("formula")}
    {CLIP("#formula-a", 0.6, 0.4)}
    {CLIP("#formula-b", 1.9, 0.4)}
    {CLIP("#formula-v1", 3.9, 0.35)}
    {CLIP("#formula-v2", 4.6, 0.35)}
    {CLIP("#formula-v3", 5.6, 0.35)}
    tl.fromTo("#formula-res", {{ opacity: 0, scale: 0.7, transformOrigin: "0% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)" }}, 6.3);
    tl.fromTo("#formula-n", {{ textContent: 0 }}, {{ textContent: 693, duration: 0.6, snap: {{ textContent: 1 }}, ease: "power2.out" }}, 6.3);
    {CLIP("#formula-lb", 5.2, 0.35)}
    {EXIT("formula", X("formula"))}
""")

# 8 shapes: CUDA graphs / torch.compile pad to max ------------------------------------------
sh = []
for r, ln in enumerate([5, 9, 3, 7]):
    for c in range(12):
        x, y = GX + c * P, GY + 40 + r * RP
        if c < 12 - ln:
            sh.append(f'<div class="c pad sh-pad" style="left:{x}px;top:{y}px;width:64px;height:70px"></div>')
        else:
            sh.append(f'<div class="c" style="left:{x}px;top:{y}px;width:64px;height:70px;background:{TINT[r]}"></div>')
S["shapes"] = scene("shapes", CELL + """
.ch { position: absolute; top: 450px; height: 76px; padding: 0 26px; font: 700 36px/70px Inter; border: 4px solid #14213D; border-radius: 14px; background: #F3EBDD; white-space: nowrap; }
""", f"""
      {B3("shapes")}
      <div id="shapes-kick" class="kick">Fixed shapes</div>
      <div id="shapes-ttl" class="ttl" style="font-size:112px">Pad to <span class="g">max</span></div>
      <div id="shapes-c1" class="ch" style="left:90px">CUDA graphs</div>
      <div id="shapes-c2" class="ch" style="left:420px">torch.compile</div>
      {"".join(sh)}
      <div id="shapes-wl" class="lb" style="left:90px;top:1010px;color:{RED};font-size:44px">more waste</div>
""", f"""
    {ENTER("shapes")}
    {KICK("shapes")}
    {CLIP("#shapes-ttl", 0.3)}
    tl.fromTo("#shapes-c1", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "back.out(1.6)" }}, 0.2);
    tl.fromTo("#shapes-c2", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "back.out(1.6)" }}, 1.0);
    tl.fromTo(".sh-pad", {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1, duration: 0.18, stagger: 0.02, ease: "back.out(2)" }}, 3.4);
    {CLIP("#shapes-wl", 4.75, 0.35)}
    {EXIT("shapes", X("shapes"))}
""")

# 9 & 10: ragged row, then the block-diagonal mask -------------------------------------------
RX, RYROW, RW = 90, 700, 42
def ragged_tokens(n, final):
    h, k = [], 0
    for r, ln in enumerate(LENS):
        for j in range(ln):
            fx, fy = RX + k * RW, RYROW
            sx, sy = 90 + (8 - ln + j) * 52, 520 + r * 60
            if final:
                h.append(f'<div class="c {n}-t" style="left:{fx}px;top:{fy}px;width:38px;height:48px;background:{TINT[r]}"></div>')
            else:
                h.append(f'<div class="c {n}-t" data-dx="{fx - sx}" data-dy="{fy - sy}" style="left:{sx}px;top:{sy}px;width:38px;height:48px;background:{TINT[r]}"></div>')
            k += 1
        if not final:
            for j in range(8 - ln):
                h.append(f'<div class="c pad {n}-pad" style="left:{90 + j * 52}px;top:{520 + r * 60}px;width:46px;height:48px"></div>')
    return "\n      ".join(h)
S["ragged"] = scene("ragged", CELL, f"""
      {B3("ragged")}
      <div id="ragged-kick" class="kick">The fix</div>
      <div id="ragged-ttl" class="ttl" style="font-size:112px">Drop the <span class="g">axis</span></div>
      {ragged_tokens("ragged", False)}
      <div id="ragged-lb" class="lb" style="left:90px;top:780px">one row · 21 tokens · 0 padding</div>
""", f"""
    {ENTER("ragged")}
    {KICK("ragged")}
    {CLIP("#ragged-ttl", 0.35)}
    tl.to(".ragged-pad", {{ opacity: 0, scale: 0.2, duration: 0.25, stagger: 0.02, ease: "power2.in" }}, 0.9);
    tl.to(".ragged-t", {{ x: (i, el) => +el.dataset.dx, y: (i, el) => +el.dataset.dy, duration: 0.7, stagger: 0.02, ease: "power3.inOut" }}, 2.5);
    {CLIP("#ragged-lb", 2.9, 0.4)}
""")

mcells = []
owner = [r for r, ln in enumerate(LENS) for _ in range(ln)]
starts = [sum(LENS[:r]) for r in range(4)]
for i in range(21):
    for j in range(21):
        ok = owner[i] == owner[j] and j <= i
        bg = TINT[owner[i]] if ok else "rgba(20,33,61,.07)"
        cls = f"mk-b{owner[i]}" if ok else "mk-o"
        mcells.append(f'<div class="c {cls}" style="left:{RX + j * RW}px;top:{780 + i * 26}px;width:38px;height:22px;border-radius:4px;background:{bg}"></div>')
S["mask"] = scene("mask", CELL, f"""
      {B3("mask")}
      <div id="mask-kick" class="kick">The attention mask</div>
      <div id="mask-ttl" class="ttl" style="font-size:112px">Ragged <span class="g">batching</span></div>
      <div id="mask-np" class="lb" style="left:90px;top:420px;font-size:44px">each prompt sees only itself · no padding</div>
      {ragged_tokens("mask", True)}
      <div id="mask-m">{"".join(mcells)}</div>
""", f"""
    tl.fromTo(".mk-o", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0.3);
    {"".join(f'tl.fromTo(".mk-b{r}", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.2, stagger: 0.008, ease: "back.out(2)" }}, {t});' + chr(10) + "    " for r, t in enumerate([0.5, 0.85, 1.2, 1.55]))}
    {CLIP("#mask-ttl", 2.75)}
    {CLIP("#mask-np", 1.0, 0.4)}
    {EXIT("mask", X("mask"))}
""", origin="540px 1050px")

# 11 & 12: the token budget M, decode first, prefill chunks, refill ----------------------------
BX, BY, BW = 90, 700, 56
def budget(n, phase):
    h = [f'<div id="{n}-bar" class="bd-bar"></div>']
    for k in range(16):
        h.append(f'<div class="bd-s" style="left:{BX + k * BW}px"></div>')
    for k in range(3):
        style = f"left:{BX + k * BW}px;top:{BY + 6}px;width:50px;height:64px;background:{TINT[k]}"
        h.append(f'<div id="{n}-dec{k}" class="c {n}-dec" style="{style}"></div>')
    for k in range(13):
        h.append(f'<div class="c {n}-ch" style="left:{BX + (3 + k) * BW}px;top:{BY + 6}px;width:50px;height:64px;background:#00C46A;opacity:.85"></div>')
    for k in range(7):
        h.append(f'<div id="{n}-q{k}" class="c {n}-q" style="left:{BX + (9 + k) * BW}px;top:{BY + 200}px;width:50px;height:64px;background:#00C46A;opacity:.5"></div>')
    return "\n      ".join(h)
BUD_CSS = CELL + """
.bd-bar { position: absolute; left: 76px; top: 690px; width: 916px; height: 96px; border: 4px solid #14213D; border-radius: 14px; }
.bd-s { position: absolute; top: 706px; width: 50px; height: 64px; border-radius: 8px; background: rgba(20,33,61,.08); }
"""
S["budget"] = scene("budget", BUD_CSS, f"""
      {B3("budget")}
      <div id="budget-kick" class="kick">The scheduler</div>
      <div id="budget-ttl" class="ttl" style="font-size:112px">Budget: <span class="g">M</span></div>
      <div class="lb" style="left:90px;top:630px;opacity:.62">M tokens per step (set by GPU memory)</div>
      {budget("budget", 0)}
      <div id="budget-l1" class="lb" style="left:90px;top:820px">decoding prompts: 1 token each</div>
      <div id="budget-l2" class="lb" style="left:90px;top:970px">prefill chunk · rest waits</div>
""", f"""
    {ENTER("budget")}
    {KICK("budget")}
    {CLIP("#budget-ttl", 0.6)}
    tl.fromTo(".bd-s", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1, stagger: 0.03 }}, 0.8);
    tl.fromTo(".budget-dec", {{ y: -200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, stagger: 0.2, ease: "back.out(1.6)" }}, 2.4);
    {CLIP("#budget-l1", 3.7, 0.35)}
    tl.fromTo(".budget-ch", {{ y: 200, opacity: 0 }}, {{ y: 0, opacity: 0.85, duration: 0.3, stagger: 0.03, ease: "power3.out" }}, 4.9);
    tl.fromTo(".budget-q", {{ opacity: 0 }}, {{ opacity: 0.5, duration: 0.2, stagger: 0.03 }}, 5.1);
    {CLIP("#budget-l2", 5.3, 0.35)}
    tl.fromTo("#budget-bar", {{ borderColor: "#14213D" }}, {{ borderColor: "#00C46A", duration: 0.25 }}, 5.6);
""")
S["refill"] = scene("refill", BUD_CSS + "#refill-bar { border-color: #00C46A; }\n", f"""
      {B3("refill")}
      <div id="refill-kick" class="kick">The scheduler</div>
      <div id="refill-ttl" class="ttl" style="font-size:112px">Every <span class="g">step</span></div>
      <div class="lb" style="left:90px;top:630px;opacity:.62">M tokens per step (set by GPU memory)</div>
      {budget("refill", 1)}
      <div class="lb" style="left:90px;top:820px">decoding prompts: 1 token each</div>
      <div class="lb" style="left:90px;top:970px">prefill chunk · rest waits</div>
      <div id="refill-done" class="lb" style="left:90px;top:1070px;color:#D9442B">finished → leaves at once</div>
      <div id="refill-nx" class="lb" style="left:90px;top:1130px">next chunk takes the slot</div>
""", f"""
    {CLIP("#refill-ttl", 0.1)}
    tl.to("#refill-dec1", {{ y: -150, opacity: 0, duration: 0.4, ease: "power2.in" }}, 0.85);
    {CLIP("#refill-done", 1.0, 0.35)}
    tl.to("#refill-q0", {{ x: -{8 * BW}, y: -200, opacity: 0.85, duration: 0.5, ease: "power3.inOut" }}, 3.35);
    tl.to(".refill-q:not(#refill-q0)", {{ x: -{BW}, duration: 0.3, stagger: 0.03, ease: "power2.inOut" }}, 3.6);
    {CLIP("#refill-nx", 3.4, 0.35)}
    {EXIT("refill", X("refill"))}
""")

# 13 sum: three parts = continuous batching ---------------------------------------------------
S["sum"] = scene("sum", """
.sm-l { position: absolute; left: 90px; font: 900 76px/1 Inter; letter-spacing: -0.02em; white-space: nowrap; }
#sum-rule { position: absolute; left: 90px; top: 1000px; width: 900px; height: 8px; background: #14213D; transform-origin: 0 50%; }
#sum-res { position: absolute; left: 84px; top: 1050px; font: 900 96px/1.05 Inter; letter-spacing: -0.03em; }
""", f"""
      {B3("sum")}
      <div id="sum-kick" class="kick">Put together</div>
      <div id="sum-a" class="sm-l" style="top:470px">KV cache</div>
      <div id="sum-b" class="sm-l" style="top:590px">+ chunked prefill</div>
      <div id="sum-c" class="sm-l" style="top:710px">+ ragged batching</div>
      <div id="sum-d" class="sm-l" style="top:830px">+ dynamic scheduling</div>
      <div id="sum-rule"></div>
      <div id="sum-res">= <span class="g">continuous</span><br>batching</div>
""", f"""
    {ENTER("sum")}
    {KICK("sum")}
    {CLIP("#sum-a", 0.2, 0.35)}
    {CLIP("#sum-b", 1.25, 0.35)}
    {CLIP("#sum-c", 2.3, 0.35)}
    {CLIP("#sum-d", 3.3, 0.35)}
    tl.fromTo("#sum-rule", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "power3.inOut" }}, 4.3);
    {CLIP("#sum-res", 4.55, 0.5)}
    {EXIT("sum", X("sum"))}
""")

# 14 next ------------------------------------------------------------------------------------------
S["next"] = scene("next", """
#next-k { position: absolute; left: 90px; top: 214px; font: 700 48px/1 Inter; opacity: .62; }
#next-ep { position: absolute; left: 70px; top: 270px; font: 900 360px/1 Inter; letter-spacing: -0.06em; }
#next-t { position: absolute; left: 84px; top: 640px; font: 900 120px/1.02 Inter; letter-spacing: -0.045em; }
#next-ul { position: absolute; left: 90px; top: 900px; width: 640px; height: 18px; background: #00C46A; transform-origin: 0 50%; }
#next-s { position: absolute; left: 90px; top: 960px; font: 700 50px/1.2 Inter; }
#next-f { position: absolute; left: 90px; top: 1160px; font: 900 64px/1 Inter; letter-spacing: -0.02em; white-space: nowrap; }
""", f"""
      {B3("next")}
      <div id="next-k">Next episode</div>
      <div id="next-ep">Ep 4</div>
      <div id="next-t">Asynchronous<br>batching</div>
      <div id="next-ul"></div>
      <div id="next-s">Continuous batching, more efficient</div>
      <div id="next-f">Follow <span id="next-h" data-var-text="handle">@vr_waingankar</span> →</div>
""", f"""
    {ENTER("next")}
    tl.fromTo("#next-k", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, 0.15);
    tl.fromTo("#next-ep", {{ scale: 1.6, opacity: 0, transformOrigin: "0% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "expo.out" }}, 0.3);
    {CLIP("#next-t", 1.3, 0.5)}
    tl.fromTo("#next-ul", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power3.inOut" }}, 2.0);
    tl.fromTo("#next-s", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 2.2);
    {CLIP("#next-f", 2.85, 0.5)}
""")

os.makedirs(f"{OUT}/compositions", exist_ok=True)
for k, v in S.items():
    open(f"{OUT}/compositions/{k}.html", "w").write(v)
print("wrote", list(S))
