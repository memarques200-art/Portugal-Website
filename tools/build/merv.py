import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, 'map.json')))
W, H = M['W'], M['H']
VB = (25, 15, 335, H - 15)  # cropped to mainland Portugal; arrow runs to the right edge

# (text key, pin key, photo(s), seven-wonders badge, extra); the number shown is the position in this list
ITEMS = [
    ('m1', 'douro',     ['photos/w-douro.jpg'], False, 'video'),
    ('mP', 'porto',     ['photos/x-dluis.jpg', 'photos/x-caves.jpg'], False, 'caves'),
    ('m2', 'aveiro',    ['photos/w-aveiro.jpg', 'luis/salinas-aveiro.jpg'], False, 'salt'),
    ('m3', 'batalha',   ['photos/w-batalha.jpg'], True, None),
    ('m4', 'sintra',    ['photos/w-pena.jpg'], True, None),
    ('m5', 'belem',     ['photos/hero-hist.jpg'], True, None),
    ('m6', 'jeronimos', ['photos/w-jeronimos.jpg'], True, None),
    ('m7', 'vgama',     ['photos/w-vgama.jpg', 'photos/w-expo.jpg', 'photos/w-oceanario.jpg'], False, 'expo'),
    ('m8', 'alqueva',   ['photos/w-alqueva.jpg'], False, None),
    ('m9', 'benagil',   ['luis/benagil.jpg'], False, None),
]
# small manual offsets so the Lisbon pins don't sit on top of each other
NUDGE = {'sintra': (-6, -6), 'belem': (-8, 10), 'jeronimos': (10, 12), 'vgama': (12, -10)}

# lon/lat -> map coordinates, fitted on known pins (equirectangular projection)
_GEO = {'porto': (-8.611, 41.150), 'benagil': (-8.427, 37.088), 'alqueva': (-7.496, 38.197), 'lisboa': (-9.139, 38.722)}
def _fit(idx_ll, idx_xy):
    pts = [(_GEO[k][idx_ll], M['pins'][k][idx_xy]) for k in _GEO]
    n = len(pts); mx = sum(a for a, _ in pts) / n; my = sum(b for _, b in pts) / n
    a = sum((u - mx) * (v - my) for u, v in pts) / sum((u - mx) ** 2 for u, _ in pts)
    return a, my - a * mx
_AX, _BX = _fit(0, 0); _AY, _BY = _fit(1, 1)
def ll(lon, lat): return _AX * lon + _BX, _AY * lat + _BY

# N222 along the Douro: Gaia -> Castelo de Paiva -> Cinfães -> Resende -> Régua -> Pinhão -> S. João da Pesqueira -> Foz Côa -> Almendra
ROAD = [(-8.611, 41.124), (-8.48, 41.075), (-8.27, 41.04), (-8.09, 41.07), (-7.96, 41.10), (-7.79, 41.155),
        (-7.67, 41.165), (-7.55, 41.19), (-7.40, 41.15), (-7.25, 41.10), (-7.14, 41.08), (-7.05, 40.99)]
_RP = [ll(*p) for p in ROAD]
ROAD_D = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in _RP)
ROAD_PIN = [round(_RP[5][0], 1), round(_RP[5][1], 1)]

def pin_xy(key):
    x, y = M['pins'][key]; dx, dy = NUDGE.get(key, (0, 0))
    return x + dx, y + dy

def svg():
    pins = []
    for i, (_, key, *_r) in enumerate(ITEMS, 1):
        x, y = pin_xy(key)
        pins.append(f'<g class="mpin" data-i="{i}" transform="translate({x:.1f},{y:.1f})"><circle class="mpin-halo" r="15"/><circle class="mpin-dot" r="9"/><text y="3.6" text-anchor="middle">{i}</text></g>')
    cities = []
    for key, name, dx in []:
        x, y = M['pins'][key]
        cities.append(f'<text class="mcity" x="{x+dx:.1f}" y="{y+4:.1f}">{name}</text>')
    return f'''<svg class="merv-svg" viewBox="{VB[0]} {VB[1]} {VB[2]} {VB[3]}" role="img" aria-label="Carte du Portugal">
          <defs><marker id="mArrowHead" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="marrow-head"/></marker></defs>
          <path class="mland-es" d="{M['es']}"/>
          <path class="mland-pt" d="{M['pt']}"/>
          <text class="mlabel-sea" x="32" y="{H*0.80:.0f}">OCEANO</text>
          <text class="mlabel-sea" x="32" y="{H*0.80+16:.0f}">ATLÂNTICO</text>
          {''.join(cities)}
          <path id="mRoad" class="mroad" d="{ROAD_D}"/>
          <path id="mArrow" class="marrow" d="" marker-end="url(#mArrowHead)"/>
          {''.join(pins)}
        </svg>'''

def item(i, k, key, photos, seven, extra):
    if extra == 'video':
        media = f'''<a class="merv-photo merv-video" href="https://youtu.be/zbUbmYi2fHk" target="_blank" rel="noopener"><img src="images/{photos[0]}" alt="" loading="lazy"><span class="video-play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span><span class="video-label"><span class="yt-badge">YouTube</span><span i18n="merv_video_watch"></span></span></a>'''
    else:
        media = f'<div class="merv-photo" data-opt-photo="{photos[0]}"><img src="images/{photos[0]}" alt="" loading="lazy"></div>'
    facts = f'<ul class="merv-facts"><li i18n="{k}_f1"></li><li i18n="{k}_f2"></li></ul>'
    badge = '<span class="merv-badge" i18n="merv_7m"></span>' if seven else ''
    more = ''
    if extra == 'salt':
        more = f'<figure class="merv-sub" data-opt-photo="{photos[1]}"><img src="images/{photos[1]}" alt="" loading="lazy"><figcaption i18n="{k}_salt_cap"></figcaption></figure>'
    if extra == 'caves':
        more = f'<figure class="merv-sub" data-opt-photo="{photos[1]}"><img src="images/{photos[1]}" alt="" loading="lazy"><figcaption i18n="{k}_caves_cap"></figcaption></figure>'
    if extra == 'expo':
        more = f'''<div class="merv-duo">
            <figure class="merv-sub" data-opt-photo="{photos[1]}"><img src="images/{photos[1]}" alt="" loading="lazy"><figcaption i18n="m7_expo_cap"></figcaption></figure>
            <div class="merv-ocean"><figure class="merv-sub" data-opt-photo="{photos[2]}"><img src="images/{photos[2]}" alt="" loading="lazy"></figure><h4 i18n="m7_ocean_t"></h4><p i18n="m7_ocean"></p></div>
          </div>'''
    if extra == 'cmp':
        K = 3.6  # px per km, both lakes on the same scale
        L1, L2 = 83 * K, 73 * K
        R1 = 62; R2 = R1 * math.sqrt(250 / 580)
        more = f'''<div class="merv-cmp">
            <h4 i18n="m8_cmp_title"></h4>
            <span class="cmp-sub" i18n="m8_len_t"></span>
            <svg viewBox="0 0 420 118" class="cmp-svg" role="img" aria-label="Longueur : Alqueva 83 km, Léman 73 km">
              <text x="10" y="16" class="cmp-lbl2" data-i18n="m8_alqueva">Lac d'Alqueva</text>
              <rect x="10" y="22" width="{L1:.0f}" height="28" rx="14" class="cmp-alq"/><text x="{10+L1+8:.0f}" y="42" class="cmp-num2">83 km</text>
              <text x="10" y="76" class="cmp-lbl2" data-i18n="m8_leman">Lac Léman</text>
              <rect x="10" y="82" width="{L2:.0f}" height="28" rx="14" class="cmp-leman"/><text x="{10+L2+8:.0f}" y="102" class="cmp-num2">73 km</text>
            </svg>
            <span class="cmp-sub" i18n="m8_area_t"></span>
            <svg viewBox="0 0 420 140" class="cmp-svg" role="img" aria-label="Surface : Léman 580 km², Alqueva 250 km²">
              <circle cx="110" cy="70" r="{R1}" class="cmp-leman"/><text x="110" y="66" text-anchor="middle" class="cmp-num">580 km²</text><text x="110" y="86" text-anchor="middle" class="cmp-lbl" data-i18n="m8_leman">Lac Léman</text>
              <circle cx="{230+R2:.1f}" cy="{70+R1-R2:.1f}" r="{R2:.1f}" class="cmp-alq"/><text x="{230+R2:.1f}" y="{70+R1-R2+5:.1f}" text-anchor="middle" class="cmp-num">250 km²</text><text x="{230+2*R2+10:.1f}" y="{70+R1-R2+5:.1f}" class="cmp-lbl2" data-i18n="m8_alqueva">Lac d'Alqueva</text>
            </svg>
            <p i18n="m8_cmp_text"></p>
          </div>'''
    return f'''
        <article class="merv-item" data-i="{i}" id="merv-{i}">
          <div class="merv-head"><span class="merv-num">{i}</span><div><span class="merv-place" i18n="{k}_place"></span><h3 class="merv-name" i18n="{k}_name"></h3></div></div>
          {media}
          {badge}
          <p class="merv-text" i18n="{k}_text"></p>
          {facts}
          {more}
        </article>'''

def view():
    return f'''
    <div class="view" id="view-merveilles">
    <section class="page-hero">
      <div class="page-hero-media">
        <img src="images/photos/hero-merv.jpg" alt="Palácio da Pena, Sintra">
      </div>
      <div class="page-hero-content">
        <div class="page-hero-eyebrow">07 <span>/ 08</span></div>
        <h1 class="page-hero-title" i18n="merv_hero_title"></h1>
        <p class="page-hero-subtitle" i18n="merv_hero_subtitle"></p>
        <div class="page-hero-divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
        <p class="page-hero-text" i18n="merv_hero_text"></p>
      </div>
    </section>

    <section class="sec merv-sec">
      <div class="wrap">
        <div class="sec-head">
          <span class="sec-eyebrow" i18n="merv_map_eyebrow"></span>
          <h2 class="sec-title" i18n="merv_map_title"></h2>
          <p class="sec-lead" i18n="merv_map_lead"></p>
        </div>
        <div class="merv-grid">
          <div class="merv-map-col"><div class="merv-map">
        {svg()}
          </div></div>
          <div class="merv-list">{''.join(item(i, *it) for i, it in enumerate(ITEMS, 1))}
        <article class="merv-item merv-road" data-i="road" id="merv-road">
          <div class="merv-head"><span class="merv-num merv-num--road">N222</span><div><span class="merv-place" i18n="road_place"></span><h3 class="merv-name" i18n="road_name"></h3></div></div>
          <div class="merv-photo" data-opt-photo="photos/z-n222.jpg"><img src="images/photos/z-n222.jpg" alt="Estrada Nacional 222" loading="lazy"></div>
          <p class="merv-text" i18n="road_text"></p>
          <ul class="merv-facts"><li i18n="road_f1"></li><li i18n="road_f2"></li><li i18n="road_f3"></li></ul>
          <figure class="merv-sub" data-opt-photo="photos/z-n222b.jpg"><img src="images/photos/z-n222b.jpg" alt="Estrada Nacional 222" loading="lazy"><figcaption i18n="road_cap"></figcaption></figure>
        </article>
          </div>
        </div>
      </div>
    </section>

    @@cta:merv:conclusion@@
    </div>
'''

PIN_JS = json.dumps({**{str(i): [round(pin_xy(k)[0], 1), round(pin_xy(k)[1], 1)] for i, (_, k, *_r) in enumerate(ITEMS, 1)}, 'road': ROAD_PIN})
ARROW_X = VB[0] + VB[2] - 4
