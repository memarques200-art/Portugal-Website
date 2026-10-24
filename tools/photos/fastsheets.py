import json, os, sys, io
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw
from wm import search
from download2 import get
Q = {
 "w-vgama": ("Ponte Vasco da Gama", 1600, True),
 "w-expo": ("Expo 98 Lisboa Parque das Nações", 1200, False),
 "w-oceanario": ("Oceanário de Lisboa", 1200, False),
 "w-alqueva": ("Barragem do Alqueva lago", 1600, True),
 "w-eusebio": ("Eusébio estátua", 600, False),
 "w-eusebio2": ("Eusébio 1966 Benfica", 400, False),
 "w-jeronimos": ("Mosteiro dos Jerónimos fachada", 1600, True),
 "w-douro": ("Douro Valley vineyards Pinhão", 1600, True),
}
res = json.load(open("cands.json"))
def one(k):
    q, minw, land = Q[k]
    c = [x for x in search(q, n=14, minw=minw) if (not land or x["w"] > x["h"]*1.25) and x["thumb"]][:8]
    res[k] = c
    thumbs = {}
    def th(i):
        u = c[i]["thumb"].replace("https://thumb.wikimedia.org/", "https://upload.wikimedia.org/").split("?")[0]
        d = get(u)
        if d: thumbs[i] = d
    with ThreadPoolExecutor(4) as ex: list(ex.map(th, range(len(c))))
    W = Image.new("RGB", (4*260, 2*230), "white"); dr = ImageDraw.Draw(W)
    for i, x in enumerate(c):
        if i in thumbs:
            im = Image.open(io.BytesIO(thumbs[i])).convert("RGB"); im.thumbnail((250, 190)); W.paste(im, ((i%4)*260, (i//4)*230))
        dr.text(((i%4)*260+2, (i//4)*230+194), f"{i} {x['w']}x{x['h']} {x['lic'][:10]}", fill="black")
        dr.text(((i%4)*260+2, (i//4)*230+208), x["title"][5:45], fill="black")
    W.save(f"sheets/{k}.jpg", quality=80)
    print("done", k, len(c), flush=True)
for k in Q: one(k)
json.dump(res, open("cands.json", "w"), indent=1)
