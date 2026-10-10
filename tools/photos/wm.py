import json, sys, urllib.request, urllib.parse, re, html
import time, urllib.error
UA = {"User-Agent": "PortugalPresentationSite/1.0 (https://github.com/memarques200-art/Portugal-Website)"}
API = "https://commons.wikimedia.org/w/api.php"
def get(params):
    params = {**params, "format": "json"}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers=UA)
    for i in range(30):
        try:
            time.sleep(1.2)
            return json.load(urllib.request.urlopen(req, timeout=30))
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(11)
    raise RuntimeError("rate limited")
def clean(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
def search(q, n=12, minw=0):
    r = get({"action":"query","generator":"search","gsrsearch":"filetype:bitmap "+q,"gsrnamespace":6,"gsrlimit":n,
             "prop":"imageinfo","iiprop":"url|size|extmetadata|mime","iiurlwidth":330})
    pages = sorted(r.get("query",{}).get("pages",{}).values(), key=lambda p:p.get("index",0))
    out=[]
    for p in pages:
        ii=p["imageinfo"][0]; m=ii.get("extmetadata",{})
        if ii["width"]<minw: continue
        out.append(dict(title=p["title"], w=ii["width"], h=ii["height"], thumb=ii.get("thumburl"),
            lic=clean(m.get("LicenseShortName",{}).get("value")), artist=clean(m.get("Artist",{}).get("value"))[:60],
            cats=clean(m.get("Categories",{}).get("value"))[:0]))
    return out
def info(title, width):
    r = get({"action":"query","titles":title,"prop":"imageinfo","iiprop":"url|size|extmetadata","iiurlwidth":width})
    p = next(iter(r["query"]["pages"].values())); ii=p["imageinfo"][0]; m=ii.get("extmetadata",{})
    return dict(title=p["title"], w=ii["width"], h=ii["height"], url=ii["thumburl"] if ii["width"]>width else ii["url"],
        page=ii["descriptionurl"], lic=clean(m.get("LicenseShortName",{}).get("value")),
        artist=clean(m.get("Artist",{}).get("value")), credit=clean(m.get("Credit",{}).get("value")))
def fetch(url, path):
    url = url.replace("https://thumb.wikimedia.org/", "https://upload.wikimedia.org/").split("?")[0]
    req = urllib.request.Request(url, headers=UA)
    for i in range(30):
        try:
            time.sleep(1.5)
            open(path,"wb").write(urllib.request.urlopen(req, timeout=60).read()); return
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(11)
    raise RuntimeError("rate limited")
if __name__=="__main__":
    for q in sys.argv[1:]:
        print("==", q)
        for c in search(q, minw=1200):
            print(f"  {c['w']}x{c['h']} | {c['lic'][:14]:14} | {c['title'][5:90]}")
