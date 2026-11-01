"""Shared helpers for reel-series scene generators: series CSS, GPU card, gauge, scene wrapper, enter/exit zoom."""
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
