"""Generate ep01 scene files (plain HyperFrames compositions; edit the output freely afterwards)."""
import sys, os
OUT = sys.argv[1]

BASE = """#root { position: absolute; inset: 0; overflow: hidden; font-family: Inter, sans-serif; color: #14213D; }
.w { position: absolute; inset: 0; transform-origin: 540px 760px; }
.kick { position: absolute; left: 90px; top: 214px; font: 700 40px/1 Inter; color: #14213D; opacity: .62; white-space: nowrap; }
.ttl { position: absolute; left: 84px; top: 268px; font: 900 128px/1 Inter; letter-spacing: -0.035em; white-space: nowrap; }
.sub { position: absolute; left: 90px; top: 1168px; width: 900px; font: 700 44px/1.25 Inter; }
.big { position: absolute; right: -30px; top: 1270px; font: 900 760px/1 Inter; color: #14213D; opacity: .07; letter-spacing: -0.06em; }
.pn { position: absolute; background: #F3EBDD; border: 4px solid #14213D; border-radius: 18px; box-shadow: 0 10px 0 rgba(20,33,61,.12); }
.lb { position: absolute; font: 700 34px/1 Inter; white-space: nowrap; }
.dot { position: absolute; left: 0; top: 0; width: 36px; height: 36px; margin: -18px 0 0 -18px; border-radius: 50%; background: #00C46A; z-index: 50; }
.g { background: linear-gradient(transparent 64%, #00C46A 64%, #00C46A 92%, transparent 92%); }
.gpu { position: absolute; width: 300px; height: 170px; }
.gpu .die { position: absolute; left: 70px; top: 26px; width: 160px; height: 110px; background: #14213D; border-radius: 10px; }
.gpu .cell { position: absolute; width: 30px; height: 22px; border-radius: 4px; background: #2B3B60; }
.gpu .gl { position: absolute; left: 22px; top: 62px; font: 900 30px/1 Inter; }
.tok { position: absolute; width: 56px; height: 40px; border-radius: 8px; background: #14213D; }
"""

def gpu(id_, x, y, extra=""):
    cells = "".join(f'<div class="cell" style="left:{8 + c * 38}px;top:{8 + r * 32}px"></div>' for r in range(3) for c in range(4))
    return f'<div id="{id_}" class="gpu pn" style="left:{x}px;top:{y}px;{extra}"><div class="die">{cells}</div></div>'

def gauge(id_, x, y, w):
    h = round(w * 0.6)
    return f"""<svg id="{id_}" style="position:absolute;left:{x}px;top:{y}px" width="{w}" height="{h}" viewBox="0 0 400 240">
  <path d="M40 200 A160 160 0 0 1 86.9 86.9" fill="none" stroke="#D9442B" stroke-width="26"/>
  <path d="M86.9 86.9 A160 160 0 0 1 313.1 86.9" fill="none" stroke="#14213D" stroke-opacity=".25" stroke-width="26"/>
  <path d="M313.1 86.9 A160 160 0 0 1 360 200" fill="none" stroke="#00C46A" stroke-width="26"/>
  <line id="{id_}-n" x1="200" y1="200" x2="200" y2="62" stroke="#14213D" stroke-width="12" stroke-linecap="round"/>
  <circle cx="200" cy="200" r="18" fill="#14213D"/></svg>"""

def scene(name, css, markup, script, origin=None):
    o = f"\n#{name}-w {{ transform-origin: {origin}; }}" if origin else ""
    return f"""<template>
  <style>
{BASE}{o}
{css.strip()}
  </style>
  <div id="root" data-composition-id="{name}" data-width="1080" data-height="1920" data-layout-allow-overflow>
    <div id="{name}-w" class="w">
{markup.strip()}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{script.strip()}
    window.__timelines["{name}"] = tl;
  </script>
</template>
"""

ENTER = lambda n: f'tl.fromTo("#{n}-w", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.5, ease: "expo.out" }}, 0);'
EXIT = lambda n, t: f'tl.to("#{n}-w", {{ scale: 6, opacity: 0, duration: 0.5, ease: "power2.in" }}, {t});'
BIG = lambda n: f'<div id="{n}-big" class="big" data-layout-ignore>0</div>'
S = {}

# 0 hook ------------------------------------------------------------------
nums = ["0.12", "-0.87", "1.04", "0.33", "-0.25", "0.91", "-1.10", "0.07", "0.58", "-0.46", "0.76", "-0.02",
        "0.19", "-0.64", "1.22", "0.41", "-0.93", "0.05", "0.68", "-0.31"]
cells = "".join(f'<div class="hk-n" style="left:{24 + (i % 4) * 82}px;top:{70 + (i // 4) * 58}px">{v}</div>' for i, v in enumerate(nums))
S["hook"] = scene("hook", """
#hook-l1 { position: absolute; left: 84px; top: 230px; font: 900 128px/1 Inter; letter-spacing: -0.035em; white-space: nowrap; }
#hook-l2 { position: absolute; left: 84px; top: 380px; font: 900 128px/1 Inter; letter-spacing: -0.035em; white-space: nowrap; }
#hook-q { display: inline-block; transform-origin: 50% 80%; }
#hook-qbar { position: absolute; left: 84px; top: 510px; width: 790px; height: 18px; background: #00C46A; transform-origin: 0 50%; }
#hook-wt { left: 90px; top: 620px; width: 380px; height: 400px; }
.hk-n { position: absolute; font: 700 28px/1 Inter; opacity: .8; }
#hook-plus { position: absolute; left: 500px; top: 760px; font: 900 110px/1 Inter; }
""", f"""
      <div id="hook-l1">Weights + GPU</div>
      <div id="hook-l2">= inference<span id="hook-q">?</span></div>
      <div id="hook-qbar"></div>
      <div id="hook-wt" class="pn"><div class="lb" style="left:24px;top:22px">weights</div>{cells}</div>
      <div id="hook-plus">+</div>
      {gpu("hook-gpu", 640, 740)}
      <div class="lb" style="left:640px;top:940px">one GPU</div>
""", f"""
    tl.fromTo("#hook-wt .hk-n", {{ opacity: 0.8 }}, {{ opacity: 0.25, duration: 0.2, stagger: {{ each: 0.04, from: "random", yoyo: true, repeat: 1 }} }}, 0.55);
    tl.fromTo("#hook-wt", {{ y: 0 }}, {{ y: -16, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }}, 0.75);
    tl.fromTo("#hook-gpu", {{ y: 0 }}, {{ y: -16, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }}, 2.2);
    tl.fromTo("#hook-gpu .cell", {{ backgroundColor: "#2B3B60" }}, {{ backgroundColor: "#00C46A", duration: 0.12, stagger: 0.03 }}, 2.25);
    tl.to("#hook-gpu .cell", {{ backgroundColor: "#2B3B60", duration: 0.3 }}, 2.8);
    tl.fromTo("#hook-q", {{ scale: 1 }}, {{ scale: 1.25, duration: 0.3, ease: "back.out(2)" }}, 3.0);
    tl.fromTo("#hook-qbar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "power3.inOut" }}, 2.9);
    {EXIT("hook", 3.77)}
""")

# 1 phases ----------------------------------------------------------------
dots = "".join(f'<div class="ph-d" style="left:{90 + (i % 6) * 60}px;top:{470 + (i // 6) * 60}px"></div>' for i in range(18))
S["phases"] = scene("phases", """
#phases-top { position: absolute; left: 0; top: 180px; width: 1080px; height: 560px; background: #14213D; }
#phases-bot { position: absolute; left: 0; top: 760px; width: 1080px; height: 560px; }
.ph-t { position: absolute; left: 90px; font: 900 104px/1 Inter; letter-spacing: -0.03em; }
#phases-tt { top: 230px; color: #E6D8BF; }
#phases-it { top: 800px; }
.ph-d { position: absolute; width: 28px; height: 28px; border-radius: 6px; background: #E6D8BF; }
#phases-wa { left: 680px; top: 430px; width: 300px; height: 230px; background: #2B3B60; border-color: #E6D8BF; }
#phases-wb { left: 90px; top: 960px; width: 300px; height: 230px; }
.ph-row { position: absolute; left: 26px; width: 248px; height: 14px; border-radius: 7px; background: #E6D8BF; transform-origin: 0 50%; }
#phases-wb .ph-row { background: #14213D; }
#phases-arrow { position: absolute; left: 420px; top: 1064px; width: 120px; height: 8px; background: #14213D; }
#phases-ans { left: 570px; top: 990px; width: 420px; height: 170px; }
#phases-ul { position: absolute; left: 90px; top: 912px; width: 470px; height: 16px; background: #00C46A; transform-origin: 0 50%; }
.ph-l { position: absolute; font: 700 34px/1 Inter; white-space: nowrap; }
""", f"""
      <div id="phases-top"></div>
      <div id="phases-bot"></div>
      <div id="phases-tt" class="ph-t">Training</div>
      <div class="ph-l" style="left:90px;top:360px;color:#E6D8BF;opacity:.8">data → weights</div>
      <div id="phases-dots">{dots}</div>
      <div id="phases-wa" class="pn">{''.join(f'<div class="ph-row" style="top:{30 + r * 40}px"></div>' for r in range(5))}</div>
      <div id="phases-it" class="ph-t">Inference</div>
      <div id="phases-ul"></div>
      <div id="phases-wb" class="pn">{''.join(f'<div class="ph-row" style="top:{30 + r * 40}px"></div>' for r in range(5))}</div>
      <div id="phases-arrow"></div>
      <div id="phases-ans" class="pn">{''.join(f'<div class="tok" style="left:{26 + i * 66}px;top:64px"></div>' for i in range(6))}</div>
      <div class="ph-l" style="left:570px;top:1200px">served in production</div>
""", f"""
    {ENTER("phases")}
    tl.fromTo("#phases-dots .ph-d", {{ x: 0, opacity: 1 }}, {{ x: 560, opacity: 0, duration: 0.6, stagger: 0.04, ease: "power2.in" }}, 1.9);
    tl.fromTo("#phases-wa .ph-row", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, stagger: 0.08, ease: "power3.out" }}, 2.6);
    tl.to("#phases-top, #phases-tt, #phases-wa", {{ opacity: 0.35, duration: 0.3 }}, 3.55);
    tl.fromTo("#phases-ul", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.35, ease: "power3.inOut" }}, 3.55);
    tl.fromTo("#phases-ans .tok", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.12, stagger: 0.06 }}, 3.9);
    {EXIT("phases", 4.33)}
""", origin="540px 1080px")

# 2 classic ---------------------------------------------------------------
S["classic"] = scene("classic", """
#classic-cpu { left: 90px; top: 560px; width: 400px; height: 400px; }
.cl-pin { position: absolute; width: 16px; height: 34px; background: #14213D; border-radius: 4px; }
.cl-node { position: absolute; width: 60px; height: 60px; border-radius: 50%; border: 4px solid #14213D; background: #F3EBDD; }
.cl-edge { position: absolute; height: 5px; background: #14213D; transform-origin: 0 50%; }
#classic-ok { position: absolute; left: 640px; top: 900px; font: 900 64px/1 Inter; color: #00C46A; white-space: nowrap; }
""", f"""
      {BIG("classic")}
      <div id="classic-kick" class="kick">Before generative AI</div>
      <div id="classic-ttl" class="ttl">Classic <span class="g">ML</span></div>
      <div id="classic-cpu" class="pn">
        {''.join(f'<div class="cl-pin" style="left:{60 + i * 60}px;top:-40px"></div><div class="cl-pin" style="left:{60 + i * 60}px;top:400px"></div>' for i in range(5))}
        <div class="cl-edge" style="left:200px;top:110px;width:120px;transform:rotate(130deg)"></div>
        <div class="cl-edge" style="left:200px;top:110px;width:120px;transform:rotate(50deg)"></div>
        <div class="cl-edge" style="left:122px;top:200px;width:90px;transform:rotate(120deg)"></div>
        <div class="cl-edge" style="left:122px;top:200px;width:90px;transform:rotate(60deg)"></div>
        <div class="cl-node" style="left:170px;top:80px"></div>
        <div class="cl-node" style="left:92px;top:172px"></div>
        <div class="cl-node" style="left:248px;top:172px"></div>
        <div class="cl-node" style="left:42px;top:262px"></div>
        <div class="cl-node" style="left:142px;top:262px"></div>
        <div id="classic-cl" class="lb" style="left:150px;top:346px">CPU</div>
      </div>
      {gauge("classic-g", 580, 560, 410)}
      <div class="lb" style="left:640px;top:830px">response speed</div>
      <div id="classic-ok">instant</div>
      <div id="classic-sub" class="sub">Small model · cheap CPU · simple stack</div>
      <div id="classic-dot" class="dot"></div>
""", f"""
    {ENTER("classic")}
    tl.fromTo("#classic-kick", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, 0.15);
    tl.fromTo("#classic-ttl", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.45, ease: "power3.inOut" }}, 0.25);
    tl.set("#classic-g-n", {{ rotation: -80, svgOrigin: "200 200" }}, 0);
    tl.fromTo("#classic-cpu .cl-node", {{ scale: 0 }}, {{ scale: 1, duration: 0.3, stagger: 0.07, ease: "back.out(1.6)" }}, 0.5);
    tl.fromTo("#classic-dot", {{ x: 1000, y: 760, scale: 0 }}, {{ scale: 1, duration: 0.15 }}, 2.6);
    tl.to("#classic-dot", {{ keyframes: [{{ x: 290, y: 640 }}, {{ x: 200, y: 850 }}], duration: 0.45, ease: "power2.in" }}, 2.75);
    tl.to("#classic-dot", {{ scale: 0, duration: 0.1 }}, 3.2);
    tl.to("#classic-g-n", {{ rotation: 72, duration: 0.45, svgOrigin: "200 200", ease: "back.out(1.4)" }}, 3.1);
    tl.fromTo("#classic-ok", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.3, ease: "power3.out" }}, 3.2);
    tl.fromTo("#classic-sub", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power3.inOut" }}, 1.3);
    tl.fromTo("#classic-cl", {{ scale: 1 }}, {{ scale: 1.3, duration: 0.15, yoyo: true, repeat: 1 }}, 4.3);
    {EXIT("classic", 4.40)}
""")

# 3 stall -----------------------------------------------------------------
rows = "".join(f'<div class="st-r" style="top:{24 + r * 36}px"></div>' for r in range(9))
S["stall"] = scene("stall", """
#stall-wb { left: 90px; top: 500px; width: 420px; height: 370px; }
.st-r { position: absolute; left: 24px; width: 364px; height: 18px; border-radius: 9px; background: #14213D; opacity: .8; }
#stall-toks { position: absolute; left: 600px; top: 520px; width: 400px; height: 60px; }
.st-q { position: absolute; width: 44px; height: 44px; border-radius: 50%; background: #D9442B; }
""", f"""
      {BIG("stall")}
      <div id="stall-kick" class="kick">Now</div>
      <div id="stall-ttl" class="ttl">Generative <span class="g">AI</span></div>
      <div id="stall-wb" class="pn"><div class="lb" style="left:24px;top:-50px">weights</div>{rows}</div>
      {gpu("stall-gpu", 150, 920)}
      <div class="lb" style="left:600px;top:470px">tokens</div>
      <div id="stall-toks">{''.join(f'<div class="tok" style="left:{i * 66}px;top:10px"></div>' for i in range(6))}</div>
      {gauge("stall-g", 600, 640, 380)}
      <div class="lb" style="left:600px;top:880px">response speed</div>
      <div class="lb" style="left:600px;top:950px">requests waiting</div>
      <div id="stall-q">{''.join(f'<div class="st-q" style="left:{600 + (i % 6) * 64}px;top:{1010 + (i // 6) * 60}px"></div>' for i in range(12))}</div>
      <div id="stall-sub" class="sub">Weights + GPUs ≠ fast, reliable inference</div>
""", f"""
    {ENTER("stall")}
    tl.fromTo("#stall-kick", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, 0.15);
    tl.fromTo("#stall-ttl", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.45, ease: "power3.inOut" }}, 0.25);
    tl.set("#stall-g-n", {{ rotation: 10, svgOrigin: "200 200" }}, 0);
    tl.fromTo("#stall-wb .st-r", {{ scaleX: 0, transformOrigin: "0 50%" }}, {{ scaleX: 1, duration: 0.3, stagger: 0.06, ease: "power3.out" }}, 0.6);
    tl.fromTo("#stall-gpu", {{ y: 160, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.4)" }}, 3.3);
    tl.fromTo("#stall-wb", {{ y: 0 }}, {{ y: 30, duration: 0.25, ease: "power2.in" }}, 3.7);
    tl.fromTo("#stall-toks .tok", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, stagger: (i) => [0, 0.5, 1.3, 1.5, 2.2, 2.6][i] }}, 4.2);
    tl.to("#stall-g-n", {{ keyframes: [{{ rotation: -40 }}, {{ rotation: -20 }}, {{ rotation: -75 }}], duration: 1.2, svgOrigin: "200 200", ease: "power1.inOut" }}, 4.25);
    tl.fromTo("#stall-q .st-q", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.08, ease: "back.out(2)" }}, 5.35);
    tl.fromTo("#stall-sub", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power3.inOut" }}, 1.0);
    {EXIT("stall", 6.40)}
""")

# 4-7 the stack (one frame that rebuilds) -----------------------------------
STACK_CSS = """
.ttl.sm { font-size: 112px; }
.slot { position: absolute; left: 90px; width: 900px; border: 4px dashed rgba(20,33,61,.35); border-radius: 18px; }
#S-rt { left: 90px; top: 880px; width: 900px; height: 250px; }
#S-tl { left: 90px; top: 450px; width: 900px; height: 120px; }
.inst { position: absolute; top: 610px; width: 280px; height: 230px; }
.inst .mini { position: absolute; left: 60px; top: 70px; width: 160px; height: 100px; background: #14213D; border-radius: 10px; }
.layer-n { position: absolute; left: 26px; top: 20px; font: 900 34px/1 Inter; white-space: nowrap; }
.trk { position: absolute; top: 54px; width: 170px; height: 10px; border-radius: 5px; background: #14213D; opacity: .3; }
.knob { position: absolute; top: 40px; width: 38px; height: 38px; border-radius: 50%; background: #14213D; }
#S-up { position: absolute; left: 880px; top: 845px; width: 26px; height: 26px; border-radius: 50%; background: #00C46A; }
"""

def stack_markup(n, built):
    """built: set of layers already locked in when the scene starts (rt, inf, tl)."""
    h = []
    h.append(f'<div class="slot" style="top:440px;height:140px"></div><div class="slot" style="top:600px;height:250px"></div><div class="slot" style="top:870px;height:270px"></div>'.replace('class="slot"', f'class="slot {n}-slot"'))
    h.append(f'<div id="{n}-rt" class="pn"><div class="layer-n">1 · Runtime</div></div>')
    h.append(gpu(f"{n}-gpu", 390, 940))
    labels = ["Cluster", "Region", "Cloud"]
    for i, x in enumerate([90, 400, 710]):
        h.append(f'<div class="inst pn {n}-inst" style="left:{x}px"><div class="layer-n">{labels[i]}</div><div class="mini"></div></div>')
    h.append(f'<div id="{n}-up"></div>')
    knobs = "".join(f'<div class="trk" style="left:{270 + i * 205}px"></div><div class="knob {n}-knob" style="left:{270 + i * 205}px"></div>' for i in range(3))
    h.append(f'<div id="{n}-tl" class="pn"><div class="layer-n" style="top:42px">3 · Tooling</div>{knobs}</div>')
    css = STACK_CSS.replace("#S-", f"#{n}-")
    mk = "\n      ".join(h)
    if "rt" not in built: mk = mk.replace(f'id="{n}-rt" class="pn"', f'id="{n}-rt" class="pn" style="opacity:0"')
    if "inf" not in built:
        mk = mk.replace(f'class="inst pn {n}-inst" style="', f'class="inst pn {n}-inst" style="opacity:0;').replace(f'<div id="{n}-up"></div>', f'<div id="{n}-up" style="opacity:0"></div>')
    if "tl" not in built: mk = mk.replace(f'<div id="{n}-tl" class="pn">', f'<div id="{n}-tl" class="pn" style="opacity:0">')
    return css, mk, ""

def stack_scene(n, built, title, sub, script, kick="Three layers", enter=False, exit_t=None, origin=None, extra_css="", extra_markup=""):
    css, mk, hide = stack_markup(n, built)
    markup = f"""
      {BIG(n)}
      <div id="{n}-kick" class="kick">{kick}</div>
      <div id="{n}-ttl" class="ttl sm">{title}</div>
      {mk}
      <div id="{n}-sub" class="sub">{sub}</div>
      {extra_markup}
"""
    s = hide + "\n    " + (ENTER(n) if enter else "") + "\n    " + script.strip()
    if exit_t is not None:
        s += "\n    " + EXIT(n, exit_t)
    return scene(n, css + extra_css, markup, s, origin=origin)

S["runtime"] = stack_scene("runtime", set(), '<span class="g">Runtime</span>', "One model · one GPU instance · max speed", """
    tl.fromTo("#runtime-kick", { opacity: 0 }, { opacity: 0.62, duration: 0.3 }, 0.15);
    tl.fromTo(".runtime-slot", { opacity: 0, scaleY: 0.6 }, { opacity: 1, scaleY: 1, duration: 0.3, stagger: 0.12, ease: "back.out(1.6)" }, 0.7);
    tl.fromTo("#runtime-ttl", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.45, ease: "power3.inOut" }, 1.95);
    tl.fromTo("#runtime-rt", { opacity: 0, scale: 1.12 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.4)" }, 2.0);
    tl.fromTo("#runtime-gpu", { y: 0 }, { y: -14, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }, 2.8);
    tl.fromTo("#runtime-gpu .cell", { backgroundColor: "#2B3B60" }, { backgroundColor: "#00C46A", duration: 0.1, stagger: 0.05 }, 4.0);
    tl.fromTo("#runtime-sub", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power3.inOut" }, 2.6);
""", enter=True)

S["infra"] = stack_scene("infra", {"rt"}, '<span class="g">Infrastructure</span>', "Clusters · regions · clouds, no silos", """
    tl.set("#infra-gpu .cell", { backgroundColor: "#00C46A" }, 0);
    tl.fromTo("#infra-ttl", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.45, ease: "power3.inOut" }, 0.1);
    tl.fromTo(".infra-inst", { opacity: 0, y: 200, scale: 0.5 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, stagger: (i) => [0.0, 1.8, 2.45][i], ease: "back.out(1.4)" }, 0.3);
    tl.fromTo("#infra-sub", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power3.inOut" }, 0.6);
    tl.fromTo("#infra-up", { opacity: 0, scale: 0 }, { opacity: 1, scale: 1.4, duration: 0.25, ease: "back.out(2)" }, 3.35);
    tl.to("#infra-up", { scale: 1, duration: 0.2 }, 3.6);
""", kick="Three layers · 2 of 3")

S["tooling"] = stack_scene("tooling", {"rt", "inf"}, '<span class="g">Tooling</span>', "Control for engineers, without the toil", """
    tl.set("#tooling-gpu .cell", { backgroundColor: "#00C46A" }, 0);
    tl.fromTo("#tooling-ttl", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.45, ease: "power3.inOut" }, 0.1);
    tl.fromTo("#tooling-tl", { opacity: 0, y: -120 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.4)" }, 0.2);
    tl.fromTo(".tooling-knob", { x: 0 }, { x: (i) => [100, 50, 132][i], duration: 0.4, stagger: 0.12, ease: "power3.inOut" }, 1.25);
    tl.fromTo("#tooling-sub", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power3.inOut" }, 0.5);
""", kick="Three layers · 3 of 3")

S["flow"] = stack_scene("flow", {"rt", "inf", "tl"}, 'Together', "", """
    tl.set("#flow-gpu .cell", { backgroundColor: "#00C46A" }, 0);
    tl.set(".flow-knob", { x: (i) => [100, 50, 132][i] }, 0);
    tl.fromTo("#flow-ttl", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.4, ease: "power3.inOut" }, 0.1);
    tl.fromTo("#flow-dot", { x: 540, y: 380, scale: 0 }, { scale: 1, duration: 0.15 }, 0.6);
    tl.to("#flow-dot", { keyframes: [{ x: 540, y: 510 }, { x: 540, y: 725 }, { x: 540, y: 1010 }], duration: 0.7, ease: "power1.inOut" }, 0.75);
    tl.fromTo("#flow-stream .tok", { x: 0, opacity: 0 }, { x: -260, opacity: 1, duration: 0.5, stagger: 0.06, ease: "none" }, 1.4);
""", kick="Three layers", exit_t=1.90, origin="540px 1010px",
   extra_css="#flow-stream { position: absolute; left: 600px; top: 1180px; width: 400px; height: 60px; overflow: hidden; }\n#flow-sub { display: none; }",
   extra_markup='<div id="flow-stream">' + "".join(f'<div class="tok" style="left:{300 + i * 66}px;top:10px;background:#00C46A"></div>' for i in range(8)) + '</div>\n      <div class="lb" style="left:90px;top:1192px">tokens streaming</div>\n      <div id="flow-dot" class="dot"></div>')

# 8 runtime stack ---------------------------------------------------------
S["stack"] = scene("stack", """
.sl { position: absolute; left: 90px; width: 900px; height: 96px; }
.sl .lb { left: 30px; top: 30px; }
.eng { position: absolute; top: 690px; width: 284px; height: 110px; }
.eng .lb { left: 26px; top: 38px; }
#stack-fa { position: absolute; left: 560px; top: 940px; width: 400px; height: 76px; background: #00C46A; border: 4px solid #14213D; border-radius: 14px; }
#stack-fa .lb { left: 22px; top: 20px; }
""", f"""
      {BIG("stack")}
      <div id="stack-kick" class="kick">Inside the runtime</div>
      <div id="stack-ttl" class="ttl">The <span class="g">stack</span></div>
      <div id="stack-gpu" class="sl pn" style="top:1040px;background:#14213D"><div class="lb" style="color:#E6D8BF">GPU</div></div>
      <div id="stack-cuda" class="sl pn" style="top:930px"><div class="lb">CUDA</div></div>
      <div id="stack-pt" class="sl pn" style="top:820px"><div class="lb">PyTorch</div></div>
      <div id="stack-e0" class="eng pn" style="left:90px"><div class="lb">vLLM</div></div>
      <div id="stack-e1" class="eng pn" style="left:398px"><div class="lb">SGLang</div></div>
      <div id="stack-e2" class="eng pn" style="left:706px"><div class="lb">TensorRT-LLM</div></div>
      <div class="lb" style="left:90px;top:640px;opacity:.62">inference engines</div>
      <div id="stack-fa"><div class="lb">⚡ FlashAttention</div></div>
      <div id="stack-sub" class="sub">From the kernel up to the engine</div>
""", f"""
    {ENTER("stack")}
    tl.fromTo("#stack-kick", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, 0.15);
    tl.fromTo("#stack-ttl", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.45, ease: "power3.inOut" }}, 0.3);
    tl.fromTo("#stack-gpu", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(1.4)" }}, 0.9);
    tl.fromTo("#stack-cuda", {{ y: -500, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.5)" }}, 1.8);
    tl.fromTo("#stack-pt", {{ y: -500, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.5)" }}, 2.35);
    tl.fromTo("#stack-e0, #stack-e1, #stack-e2", {{ y: -500, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, stagger: (i) => [0, 0.88, 2.02][i], ease: "back.out(1.5)" }}, 4.1);
    tl.fromTo("#stack-fa", {{ scale: 0, opacity: 0, transformOrigin: "0% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, 8.5);
    tl.fromTo("#stack-sub", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power3.inOut" }}, 6.9);
    {EXIT("stack", 9.20)}
""")

# 9 dials -----------------------------------------------------------------
names = ["Batching", "Caching", "Quantization", "Speculation", "Parallelism", "Disaggregation"]
dm = ""
for i, nm in enumerate(names):
    x, y = 90 + (i % 3) * 315, 480 + (i // 3) * 340
    dm += f'<div class="dl pn" style="left:{x}px;top:{y}px">{gauge(f"dials-g{i}", 25, 30, 220)}<div class="dl-l">{nm}</div></div>\n      '
S["dials"] = scene("dials", """
.dl { position: absolute; width: 270px; height: 300px; }
.dl-l { position: absolute; left: 0; right: 0; top: 200px; text-align: center; font: 700 30px/1 Inter; white-space: nowrap; }
.ttl.sm { font-size: 112px; }
""", f"""
      {BIG("dials")}
      <div id="dials-kick" class="kick">The runtime's toolkit</div>
      <div id="dials-ttl" class="ttl sm">Six <span class="g">techniques</span></div>
      {dm}
      <div id="dials-sub" class="sub">One episode each, starting next</div>
""", f"""
    {ENTER("dials")}
    tl.fromTo("#dials-kick", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, 0.15);
    tl.fromTo("#dials-ttl", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.45, ease: "power3.inOut" }}, 0.3);
    tl.fromTo(".dl", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, stagger: 0.06, ease: "back.out(1.6)" }}, 0.5);
    tl.set("#dials-w line", {{ rotation: -80, svgOrigin: "200 200" }}, 0);
    {"".join(f'tl.to("#dials-g{i}-n", {{ rotation: 70, duration: 0.4, svgOrigin: "200 200", ease: "back.out(1.6)" }}, {t});' + chr(10) + "    " for i, t in enumerate([1.7, 2.25, 2.9, 3.85, 4.75, 5.5]))}
    tl.fromTo("#dials-sub", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power3.inOut" }}, 4.4);
    {EXIT("dials", 6.57)}
""")

# 10 next -----------------------------------------------------------------
S["next"] = scene("next", """
#next-k { position: absolute; left: 90px; top: 214px; font: 700 48px/1 Inter; opacity: .62; }
#next-ep { position: absolute; left: 70px; top: 270px; font: 900 400px/1 Inter; letter-spacing: -0.06em; }
#next-t { position: absolute; left: 84px; top: 690px; font: 900 150px/1 Inter; letter-spacing: -0.045em; }
#next-ul { position: absolute; left: 90px; top: 860px; width: 640px; height: 18px; background: #00C46A; transform-origin: 0 50%; }
#next-s { position: absolute; left: 90px; top: 930px; font: 700 50px/1.2 Inter; }
#next-f { position: absolute; left: 90px; top: 1160px; font: 900 64px/1 Inter; letter-spacing: -0.02em; white-space: nowrap; }
""", f"""
      {BIG("next")}
      <div id="next-k">Next episode</div>
      <div id="next-ep">Ep 2</div>
      <div id="next-t">Batching</div>
      <div id="next-ul"></div>
      <div id="next-s">Requests woven together, token by token</div>
      <div id="next-f">Follow <span id="next-h" data-var-text="handle">@vr_waingankar</span> →</div>
""", f"""
    {ENTER("next")}
    tl.fromTo("#next-k", {{ opacity: 0 }}, {{ opacity: 0.62, duration: 0.3 }}, 0.2);
    tl.fromTo("#next-ep", {{ scale: 1.6, opacity: 0, transformOrigin: "0% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "expo.out" }}, 0.4);
    tl.fromTo("#next-t", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power3.inOut" }}, 2.55);
    tl.fromTo("#next-ul", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power3.inOut" }}, 2.85);
    tl.fromTo("#next-s", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 2.9);
    tl.fromTo("#next-f", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "power3.inOut" }}, 3.45);
""")

os.makedirs(f"{OUT}/compositions", exist_ok=True)
for k, v in S.items():
    open(f"{OUT}/compositions/{k}.html", "w").write(v)
print("wrote", list(S))
