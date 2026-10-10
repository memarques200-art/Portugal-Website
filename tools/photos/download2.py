import json, os, re, urllib.request, urllib.error, time, threading
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from wm import info, UA
OUT = "/home/user/Portugal-Website/images/photos"
picks = json.load(open("picks.json")); cands = json.load(open("cands.json"))
credf = os.path.join(OUT, "credits.json")
cred = json.load(open(credf)) if os.path.exists(credf) else {}
lock = threading.Lock()
def get(url):
    for i in range(12):
        try:
            req = urllib.request.Request(url, headers=UA)
            return urllib.request.urlopen(req, timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(10); continue
            if e.code in (400, 404): return None
            raise
    return None
def job(key, sel):
    ext = "png" if key in ("geo-climate", "hist-routes") else "jpg"
    fname = f"{key}.{ext}"
    if fname in cred and os.path.exists(os.path.join(OUT, fname)): return
    if isinstance(sel, dict):
        m = info(sel["title"], 1280); c = {"title": m["title"], "thumb": m["url"], "w": m["w"], "lic": m["lic"], "artist": m["artist"]}
    else:
        src, idx = (sel.split(":")[0], int(sel.split(":")[1])) if isinstance(sel, str) else (key, sel)
        c = cands[src][idx]
    base = c["thumb"].replace("https://thumb.wikimedia.org/", "https://upload.wikimedia.org/").split("?")[0]
    hero = key.startswith("hero-") or key == "bridge-alps"
    data = None
    for w in ([3840, 1920] if hero else [1280, 960]) + [500]:
        if "/thumb/" in base:
            url = re.sub(r"/\d+px-", f"/{w}px-", base)
        else:
            url = base
        data = get(url)
        if data: break
    if not data:
        print("FAILED", key, flush=True); return
    p = f"/tmp/_dl_{key}"; open(p, "wb").write(data)
    im = Image.open(p); im.load()
    maxw = 2560 if hero else 1100
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    if ext == "jpg": im.convert("RGB").save(os.path.join(OUT, fname), quality=80, optimize=True, progressive=True)
    else: im.save(os.path.join(OUT, fname), optimize=True)
    with lock:
        cred[fname] = {"title": c["title"], "page": "https://commons.wikimedia.org/wiki/" + c["title"].replace(" ", "_"),
                       "artist": c.get("artist", ""), "lic": c.get("lic", ""), "w": im.width, "h": im.height}
        json.dump(cred, open(credf, "w"), indent=1, ensure_ascii=False)
    print("saved", fname, im.size, flush=True)
with ThreadPoolExecutor(4) as ex:
    list(ex.map(lambda kv: job(*kv), picks.items()))
print("ALL DONE", flush=True)
