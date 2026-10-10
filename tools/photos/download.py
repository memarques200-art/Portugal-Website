import json, os, sys, io
from PIL import Image
from wm import info, fetch
OUT = "/home/user/Portugal-Website/images/photos"
os.makedirs(OUT, exist_ok=True)
picks = json.load(open("picks.json")); cands = json.load(open("cands.json"))
credf = os.path.join(OUT, "credits.json")
cred = json.load(open(credf)) if os.path.exists(credf) else {}
for key, sel in picks.items():
    if sel is None: continue
    ext = "png" if key in ("geo-climate", "hist-routes") else "jpg"
    fname = f"{key}.{ext}"
    if fname in cred and os.path.exists(os.path.join(OUT, fname)): continue
    if isinstance(sel, dict): c = {"title": sel["title"]}
    else:
        src, idx = (sel.split(":")[0], int(sel.split(":")[1])) if isinstance(sel, str) else (key, sel)
        c = cands[src][idx]
    hero = key.startswith("hero-") or key == "bridge-alps"
    tw = 3840 if hero else 1280
    try:
        meta = info(c["title"], tw)
        fetch(meta["url"], "/tmp/_dl")
    except Exception as e:
        print("FAILED", key, e, flush=True); continue
    im = Image.open("/tmp/_dl"); im.load()
    maxw = 2560 if hero else 1100
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    if ext == "jpg":
        im.convert("RGB").save(os.path.join(OUT, fname), quality=80, optimize=True, progressive=True)
    else:
        im.save(os.path.join(OUT, fname), optimize=True)
    cred[fname] = {k: meta[k] for k in ("title", "page", "artist", "lic", "w", "h")}
    json.dump(cred, open(credf, "w"), indent=1, ensure_ascii=False)
    print("saved", fname, im.size, os.path.getsize(os.path.join(OUT, fname)) // 1024, "KB", flush=True)
