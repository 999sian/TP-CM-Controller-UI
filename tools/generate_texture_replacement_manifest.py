#!/usr/bin/env python3
from __future__ import annotations
import argparse, struct, tarfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MASK=(1<<64)-1
P1,P2,P3,P4,P5=(11400714785074694791,14029467366897019727,1609587929392839161,9650029242287828579,2870177450012600261)

# group, display name, resource path, note
ENTRIES=[
("PlayStation","Cross","res/buttons/cross.bti",""),("PlayStation","Circle","res/buttons/circle.bti",""),
("PlayStation","Square","res/buttons/square.bti",""),("PlayStation","Triangle","res/buttons/triangle.bti",""),
("PlayStation","R1","res/buttons/r1.bti",""),("PlayStation","R1 HUD","res/buttons/r1_hud.bti",""),
("PlayStation","L3","res/buttons/l3.bti",""),("PlayStation","Animated analog base","res/buttons/animated_analog_base.bti",""),
("PlayStation","Skill L3 overlay","res/buttons/skill_l3.bti",""),("PlayStation","Shop L3 overlay","res/buttons/shop_l3_right.bti",""),
("PlayStation","R3","res/buttons/r3.bti",""),("PlayStation","L2","res/buttons/l2.bti",""),
("PlayStation","R2","res/buttons/r2.bti",""),("PlayStation","Options","res/buttons/options.bti",""),
("PlayStation","D-Pad","res/buttons/dpad.bti",""),
("Xbox","A","res/xbox/cross.bti",""),("Xbox","B","res/xbox/circle.bti",""),
("Xbox","X","res/xbox/square.bti",""),("Xbox","Y","res/xbox/triangle.bti",""),
("Xbox","RB","res/xbox/r1.bti",""),("Xbox","RB HUD","res/xbox/r1_hud.bti",""),
("Xbox","L3","res/xbox/l3.bti",""),("Xbox","Animated analog base","res/xbox/animated_analog_base.bti","Shared with Switch."),
("Xbox","Skill L3 overlay","res/xbox/skill_l3.bti","Shared with Switch."),
("Xbox","Shop L3 overlay","res/xbox/shop_l3_right.bti","Shared with Switch."),
("Xbox","R3","res/xbox/r3.bti",""),("Xbox","LT","res/xbox/l2.bti",""),
("Xbox","RT","res/xbox/r2.bti",""),("Xbox","Menu","res/xbox/options.bti",""),
("Xbox","D-Pad","res/xbox/dpad.bti",""),
("Nintendo Switch","A","res/switch/a.bti",""),("Nintendo Switch","B","res/switch/b.bti",""),
("Nintendo Switch","Y","res/switch/y.bti",""),("Nintendo Switch","X","res/switch/x.bti",""),
("Nintendo Switch","R","res/switch/r.bti",""),("Nintendo Switch","R HUD","res/switch/r.bti","Same texture as R."),
("Nintendo Switch","L Stick","res/switch/l_stick.bti",""),
("Nintendo Switch","Animated analog base","res/xbox/animated_analog_base.bti","Shared with Xbox."),
("Nintendo Switch","Skill stick overlay","res/xbox/skill_l3.bti","Shared with Xbox."),
("Nintendo Switch","Shop stick overlay","res/xbox/shop_l3_right.bti","Shared with Xbox."),
("Nintendo Switch","R Stick","res/switch/r_stick.bti",""),("Nintendo Switch","ZL","res/switch/zl.bti",""),
("Nintendo Switch","ZR","res/switch/zr.bti",""),("Nintendo Switch","+","res/switch/plus.bti",""),
("Nintendo Switch","D-Pad","res/switch/dpad.bti",""),
("Shared UI","Menu ornament","res/ornament/menu_ornament.bti",""),
("Shared UI","HUD ornament","res/ornament/hud_ornament.bti",""),
]
LAYOUT={0:(8,8,32),1:(8,4,32),2:(8,4,32),3:(4,4,32),4:(4,4,32),5:(4,4,32),6:(4,4,64),8:(8,8,32),9:(8,4,32),10:(4,4,32),14:(8,8,32)}
PALETTED={8,9,10}

def rol(x,n): return ((x<<n)|(x>>(64-n)))&MASK
def rnd(a,v): return rol((a+v*P2)&MASK,31)*P1&MASK
def merge(a,v): return ((a^rnd(0,v))*P1+P4)&MASK
def xxh64(b):
    n=len(b); i=0
    if n>=32:
        v1=(P1+P2)&MASK; v2=P2; v3=0; v4=(-P1)&MASK
        while i<=n-32:
            v1=rnd(v1,int.from_bytes(b[i:i+8],"little")); i+=8
            v2=rnd(v2,int.from_bytes(b[i:i+8],"little")); i+=8
            v3=rnd(v3,int.from_bytes(b[i:i+8],"little")); i+=8
            v4=rnd(v4,int.from_bytes(b[i:i+8],"little")); i+=8
        h=(rol(v1,1)+rol(v2,7)+rol(v3,12)+rol(v4,18))&MASK
        for v in (v1,v2,v3,v4): h=merge(h,v)
    else: h=P5
    h=(h+n)&MASK
    while i+8<=n:
        h^=rnd(0,int.from_bytes(b[i:i+8],"little")); h=(rol(h,27)*P1+P4)&MASK; i+=8
    if i+4<=n:
        h^=int.from_bytes(b[i:i+4],"little")*P1&MASK; h=(rol(h,23)*P2+P3)&MASK; i+=4
    while i<n:
        h^=b[i]*P5&MASK; h=rol(h,11)*P1&MASK; i+=1
    h^=h>>33; h=h*P2&MASK; h^=h>>29; h=h*P3&MASK; h^=h>>32
    return h&MASK

def read(path):
    p=ROOT/path
    if p.exists(): return p.read_bytes()
    if path.startswith("res/switch/"):
        name=Path(path).name
        for a in sorted((ROOT/"assets/switch").glob("*.tar.gz")):
            with tarfile.open(a,"r:gz") as t:
                for m in t.getmembers():
                    if m.isfile() and Path(m.name).name==name:
                        f=t.extractfile(m)
                        if f: return f.read()
    raise FileNotFoundError(path)

def info(path):
    b=read(path)
    if len(b)<32: raise ValueError(f"{path}: short BTI")
    fmt=b[0]; w=struct.unpack_from(">H",b,2)[0]; h=struct.unpack_from(">H",b,4)[0]
    off=struct.unpack_from(">I",b,0x1c)[0]
    bw,bh,bs=LAYOUT[fmt]
    size=((w+bw-1)//bw)*((h+bh-1)//bh)*bs
    if off<32 or off+size>len(b): raise ValueError(f"{path}: invalid BTI image range")
    hx=xxh64(b[off:off+size])
    name=f"tex1_{w}x{h}_{hx:016x}"
    if fmt in PALETTED: name+="_$"
    return f"{name}_{fmt}.png"

def render():
    rows=[(g,n,p,note,info(p)) for g,n,p,note in ENTRIES]
    counts={}
    for *_,fn in rows: counts[fn]=counts.get(fn,0)+1
    out=[
"# Custom Texture Replacements","",
"TP Classic Modern Controller UI supports Dusklight's native user texture replacement system.",
"Create a PNG or DDS replacement, use the filename below, and place it in the user's `texture_replacements/` folder.","",
"Enable **Texture Replacements** in Dusklight's graphics settings.","",
"> Generated from the exact BTI resources shipped by the mod.",
"> After changing a BTI run `python tools/generate_texture_replacement_manifest.py --write`.","",
"## Notes","",
"- Dusklight matches the original texture by dimensions, GX format and XXH64 content hash.",
"- Replacement images may be higher resolution; keep the same aspect ratio for predictable HUD geometry.",
"- Removing the replacement restores the texture bundled with the mod.",
"- The mod intentionally keeps these as normal `res/` BTIs, not mod-owned `textures/` replacements, so the user's native replacements can win.",
"- If a base BTI changes, its replacement filename can change. CI verifies this manifest.",
"- Shared entries use the same source hash, so one replacement affects every context sharing that filename.",""
]
    groups=[]
    for g,*_ in rows:
        if g not in groups: groups.append(g)
    for g in groups:
        out += [f"## {g}","","| Texture | Replacement filename | Base resource | Notes |","| --- | --- | --- | --- |"]
        for gg,n,p,note,fn in rows:
            if gg!=g: continue
            extra=note
            if counts[fn]>1: extra=(extra+" Shared replacement hash.").strip()
            out.append(f"| {n} | `{fn}` | `{p}` | {extra} |")
        out.append("")
    return "\n".join(out)

def main():
    ap=argparse.ArgumentParser(); x=ap.add_mutually_exclusive_group()
    x.add_argument("--write",action="store_true"); x.add_argument("--check",action="store_true")
    a=ap.parse_args(); text=render(); dst=ROOT/"docs/texture-replacements.md"
    if a.write:
        dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(text,encoding="utf-8",newline="\n"); print(f"Wrote {dst.relative_to(ROOT)}"); return 0
    if a.check:
        if not dst.exists() or dst.read_text(encoding="utf-8")!=text:
            print("texture replacement manifest is out of date; run the generator with --write"); return 1
        print("texture replacement manifest is current"); return 0
    print(text,end=""); return 0

if __name__=="__main__": raise SystemExit(main())
