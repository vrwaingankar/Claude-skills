import sys, json
P=sys.argv[1]; L=json.load(open(sys.argv[2]))
names=["hook","intro","recap","phases","classic","stall","runtime","infra","tooling","flow","stack","dials","next"]
starts=L["scene_starts"]; total=L["total"]
f=lambda x: (f"{x:.3f}".rstrip("0").rstrip(".") if x%1 else f"{x:.1f}")
hosts=[]
for i,n in enumerate(names):
    d=(starts[i+1] if i+1<len(names) else total)-starts[i]
    hosts.append(f'      <div id="{n}" data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-start="{f(starts[i])}" data-duration="{f(round(d,3))}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>')
st=dict(zip(names,starts)); sfx=[]; k=[0]
def add(id_,file,t,dur,vol,extra=""):
    k[0]+=1; sfx.append(f'      <audio id="{id_}" class="clip" src="assets/sfx/{file}" data-start="{t:.2f}" data-duration="{dur}" data-track-index="{9+k[0]}" data-volume="{vol}"{extra}></audio>')
takes=[("whoosh.mp3",0.57),("whoosh-short.mp3",0.57)]
for i,n in enumerate(["intro","recap","phases","classic","stall","runtime","stack","dials","next"]):
    fl,d=takes[i%2]; add(f"sfx-w{i+1}",fl,st[n]-0.35,d,0.2)
add("sfx-ok","click.mp3",st["classic"]+3.1,0.37,0.35)
add("sfx-glitch","glitch-1.mp3",st["stall"]+2.9,1.6,0.22,' data-fade-out="0.4"')
add("sfx-lock1","impact-bass-2.mp3",st["runtime"]+1.9,1.2,0.3,' data-fade-out="0.4"')
for j,t in enumerate([0.3,2.1,2.75]): add(f"sfx-inst{j+1}","click-soft.mp3",st["infra"]+t,0.37,0.3)
add("sfx-up","ping.mp3",st["infra"]+3.5,0.5,0.22,' data-fade-out="0.2"')
add("sfx-lock3","impact-bass-2.mp3",st["tooling"]+0.25,1.2,0.3,' data-fade-out="0.4"')
add("sfx-riser","riser.mp3",st["flow"]+1.55-1.9,1.9,0.2,' data-fade-out="0.2"')
add("sfx-hit","impact-bass-1.mp3",st["flow"]+1.55,2.0,0.3)
for j,t in enumerate([1.74,2.3,2.96,3.9,4.82,5.58]): add(f"sfx-d{j+1}","click-soft.mp3",st["dials"]+t,0.37,0.3)
add("sfx-pop","pop.mp3",st["next"]+0.4,0.72,0.3)
idx=open(f"{P}/index.html").read()
head=idx[:idx.index('      <div id="ground"></div>')+len('      <div id="ground"></div>\n')]
import re
head=re.sub(r'(id="root"[^>]*data-duration=")[0-9.]+', rf'\g<1>{f(total)}', head)
tail='''    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
'''
vo=f'      <audio id="vo" class="clip" src="assets/vo.m4a" data-start="0" data-duration="{f(total)}" data-track-index="2" data-volume="1"></audio>'
open(f"{P}/index.html","w").write(head+"\n".join(hosts)+"\n"+vo+"\n"+"\n".join(sfx)+"\n"+tail)
