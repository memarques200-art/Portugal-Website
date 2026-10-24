import sys, json, os, io
from wm import search, fetch
from PIL import Image, ImageDraw
# key: (query, minw, landscape_only)
H=2400
Q = {
 "hero-home": ("Porto Ribeira Douro sunset", H, True),
 "hero-geo": ("Farolim de Felgueiras waves", 1600, True),
 "hero-hist": ("Torre de Belém", H, True),
 "hero-inst": ("Palácio de São Bento Lisboa", H, True),
 "hero-soc": ("Alfama Lisboa", H, True),
 "hero-cult": ("São Bento railway station azulejos", H, True),
 "hero-sport": ("Nazaré wave surfing", 2000, True),
 "hero-reg": ("Douro valley vineyards", H, True),
 "hero-concl": ("Cabo da Roca sunset", H, True),
 "bridge-alps": ("Matterhorn reflection lake", H, True),
 "j-geo": ("Ponta da Piedade Lagos", 1000, False),
 "j-hist": ("Mosteiro dos Jerónimos", 1000, False),
 "j-soc": ("Lisbon tram 28", 1000, False),
 "j-cult": ("azulejos Porto church", 1000, False),
 "j-gastro": ("pastel de nata", 1000, False),
 "j-moi": ("Serra do Caramulo", 1000, False),
 "geo-north": ("Peneda-Gerês National Park", 1200, False),
 "geo-south": ("Alentejo landscape plain", 1200, False),
 "geo-climate": ("Köppen climate Portugal map", 600, False),
 "geo-relief": ("Serra da Estrela landscape", 1200, False),
 "geo-acores": ("Sete Cidades lagoa", 1200, False),
 "geo-volcano": ("Capelinhos 1957 eruption", 600, False),
 "geo-madeira": ("Madeira cliffs Ponta de São Lourenço", 1200, False),
 "geo-map": ("Iberian Peninsula satellite", 1800, True),
 "hist-flag": ("flag of Portugal waving", 1000, False),
 "hist-guimaraes": ("Castelo de Guimarães", 1000, False),
 "hist-windsor": ("João I Philippa of Lancaster marriage", 600, False),
 "hist-tea": ("Catherine of Braganza portrait", 800, False),
 "hist-routes": ("Portuguese discoveries map", 1200, True),
 "st-cantino": ("Cantino planisphere", 1200, False),
 "st-nanban": ("Nanban byobu Portuguese ship", 1200, False),
 "st-1755": ("1755 Lisbon earthquake engraving", 800, False),
 "st-mendes": ("Aristides de Sousa Mendes", 400, False),
 "st-salazar": ("António de Oliveira Salazar", 600, False),
 "st-macau": ("Ruins of St. Paul's Macau", 1200, False),
 "inst-belem": ("Palácio de Belém Lisboa", 1000, False),
 "inst-praca": ("Praça do Comércio Lisboa", 1200, False),
 "inst-tc": ("Palácio Ratton Tribunal Constitucional", 600, False),
 "inst-1974": ("Revolução dos Cravos 25 de Abril 1974", 600, False),
}
Q.update({
 "w-batalha": ("Mosteiro da Batalha", 1600, True),
 "w-aveiro": ("Aveiro moliceiros canal", 1600, True),
 "w-salinas": ("Salinas de Aveiro", 1200, False),
 "w-pena": ("Palácio da Pena Sintra", 1600, True),
 "w-vgama": ("Ponte Vasco da Gama", 1600, True),
 "w-expo": ("Expo 98 Lisboa Parque das Nações", 1200, False),
 "w-oceanario": ("Oceanário de Lisboa", 1200, False),
 "w-alqueva": ("Barragem do Alqueva lago", 1600, True),
 "w-eusebio": ("Eusébio estátua", 600, False),
 "w-eusebio2": ("Eusébio 1966 Benfica", 400, False),
 "w-jeronimos": ("Mosteiro dos Jerónimos fachada", 1600, True),
 "w-douro": ("Douro Valley vineyards Pinhão", 1600, True),
 "rbar": ("Red Bull Air Race Porto", 1200, True),
 "smf-castle": ("Castelo de Santa Maria da Feira", 2000, True),
 "smf-viagem": ("Feira Medieval de SM", 1200, False),
 "smf-viagem2": ("Viagem Medieval Terra de Santa Maria", 800, False),
 "naz-dec": ("Waves in Nazaré in December 2025", 3000, True),
 "smf-castle": ("Castelo de Santa Maria da Feira", 2000, True),
 "smf-viagem": ("Feira Medieval de SM", 1200, False),
 "smf-viagem2": ("Viagem Medieval Terra de Santa Maria", 800, False),
 "naz-dec": ("Waves in Nazaré in December 2025", 3000, True),
 "x-south": ("Alentejo montado landscape", 1000, False),
 "x-1974": ("25 de Abril de 2024 cravos", 1000, False),
 "x-celeste": ("Celeste dos Cravos", 1000, False),
 "x-marchas": ("Marchas Populares Lisboa", 800, False),
 "e-fatima2": ("Basílica de Nossa Senhora do Rosário Fátima", 1000, False),
 "c-santoantonio2": ("Festas de Lisboa arraial sardinhas", 600, False),
 "f-alheira2": ("alheira de Mirandela enchido", 400, False),
 "inst-1974b": ("Carnation Revolution Lisbon 1974 soldiers crowd", 400, False),
 "geo-south2": ("Alentejo planície", 1200, False),
 "hero-geo2": ("Praia da Marinha Algarve cliffs", 2400, True),
 "hero-geo3": ("Serra da Estrela panorama", 2400, True),
 "f-bacalhau": ("Bacalhau à Brás", 800, False),
 "f-nata": ("pastéis de nata", 800, False),
 "f-francesinha": ("Francesinha", 800, False),
 "f-sardinhas": ("sardinhas assadas", 800, False),
 "f-caldo": ("caldo verde soup", 800, False),
 "f-leitao": ("leitão da Bairrada", 800, False),
 "f-polvo": ("polvo à lagareiro", 600, False),
 "f-cataplana": ("cataplana", 800, False),
 "f-bifana": ("bifana sandwich", 600, False),
 "f-queijo": ("Queijo Serra da Estrela", 800, False),
 "f-alheira": ("alheira", 600, False),
 "f-ovos": ("ovos moles de Aveiro", 600, False),
 "c-fado": ("Amália Rodrigues", 400, False),
 "c-azulejo": ("Capela das Almas Porto azulejos", 800, False),
 "c-manuelino": ("Jerónimos cloister", 1000, False),
 "c-pessoa": ("Fernando Pessoa statue A Brasileira", 800, False),
 "c-santoantonio": ("Marchas populares Lisboa Santo António", 800, False),
 "c-saojoao": ("São João Porto festa", 800, False),
 "c-diaportugal": ("Padrão dos Descobrimentos", 1000, False),
 "s-ronaldo": ("Cristiano Ronaldo Portugal", 800, False),
 "s-luz": ("Estádio da Luz", 1200, False),
 "s-dragao": ("Estádio do Dragão", 1200, False),
 "s-eusebio": ("Eusébio statue Estádio da Luz", 600, False),
 "s-hockey": ("hóquei em patins Portugal", 600, False),
 "s-euro2016": ("Portugal Euro 2016 celebration Lisbon", 600, False),
 "r-porto": ("Porto Ribeira", 1200, False),
 "r-coimbra": ("Universidade de Coimbra torre", 1200, False),
 "r-lisboa": ("Lisbon Alfama view miradouro", 1200, False),
 "r-evora": ("Templo romano de Évora", 1200, False),
 "r-algarve": ("Benagil cave Algarve", 1200, False),
 "r-acores": ("Pico mountain Azores", 1200, False),
 "r-madeira": ("Pico do Arieiro Madeira", 1200, False),
 "r-caramulo": ("Caramulo", 800, False),
 "r-caramulo2": ("Museu do Caramulo", 600, False),
 "e-cork": ("cork oak harvest bark", 800, False),
 "e-wind": ("wind farm Portugal", 1000, False),
 "e-fatima": ("Santuário de Fátima", 1000, False),
 "e-cafe": ("A Brasileira café Lisboa", 800, False),
})
os.makedirs("sheets", exist_ok=True)
keys = sys.argv[1:] or list(Q)
res = {}
if os.path.exists("cands.json"): res = json.load(open("cands.json"))
for k in keys:
    if os.path.exists(f"sheets/{k}.jpg"): continue
    q, minw, land = Q[k]
    if k in res: c = res[k]
    else:
        ok = lambda x: (not land or x["w"] > x["h"]*1.25) and x["thumb"]
        c = [x for x in search(q + ' incategory:"Quality_images"', n=12, minw=minw) if ok(x)][:5] if not k.startswith(("smf","naz","rbar")) else [] if not k.startswith(("smf","naz","rbar")) else []
        if len(c) < 3:
            seen = {x["title"] for x in c}
            c += [x for x in search(q, n=12, minw=minw) if ok(x) and x["title"] not in seen][:(10 if k.startswith(("smf","naz","rbar")) else 5)-len(c)]
    res[k] = c
    json.dump(res, open("cands.json","w"), indent=1)
    W = Image.new("RGB", (5*260, 2*230), "white"); d = ImageDraw.Draw(W)
    for i, x in enumerate(c):
        try:
            fetch(x["thumb"], "/tmp/_t.jpg"); im = Image.open("/tmp/_t.jpg").convert("RGB"); im.thumbnail((250, 190))
            W.paste(im, ((i%5)*260, (i//5)*230))
        except Exception as e: print('thumb fail', k, i, e, flush=True)
        d.rectangle(((i%5)*260, (i//5)*230+192, (i%5)*260+250, (i//5)*230+228), fill="white")
        d.text(((i%5)*260+2, (i//5)*230+194), f"{i} {x['w']}x{x['h']} {x['lic'][:8]}", fill="black")
        d.text(((i%5)*260+2, (i//5)*230+208), x["title"][5:45], fill="black")
    W.save(f"sheets/{k}.jpg", quality=80)
    print("done", k, len(c), flush=True)
