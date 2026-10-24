import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, 'map.json')))
W, H = M['W'], M['H']
VB = (25, 15, 335, H - 15)  # cropped to mainland Portugal; arrow runs to the right edge

# (index, pin key, photo(s), seven-wonders badge, extra)
ITEMS = [
    (1, 'douro',     ['photos/w-douro.jpg'], False, 'video'),
    (2, 'aveiro',    ['photos/w-aveiro.jpg', 'photos/w-salinas.jpg'], False, 'salt'),
    (3, 'batalha',   ['photos/w-batalha.jpg'], True, None),
    (4, 'sintra',    ['photos/w-pena.jpg'], True, None),
    (5, 'belem',     ['photos/hero-hist.jpg'], True, None),
    (6, 'jeronimos', ['photos/w-jeronimos.jpg'], True, None),
    (7, 'vgama',     ['photos/w-vgama.jpg', 'photos/w-expo.jpg', 'photos/w-oceanario.jpg'], False, 'expo'),
    (8, 'alqueva',   ['photos/w-alqueva.jpg'], False, 'cmp'),
    (9, 'benagil',   ['photos/r-algarve.jpg'], False, None),
]
# small manual offsets so the Lisbon pins don't sit on top of each other
NUDGE = {'sintra': (-6, -6), 'belem': (-8, 10), 'jeronimos': (10, 12), 'vgama': (12, -10)}

def pin_xy(key):
    x, y = M['pins'][key]; dx, dy = NUDGE.get(key, (0, 0))
    return x + dx, y + dy

def svg():
    pins = []
    for i, key, *_ in ITEMS:
        x, y = pin_xy(key)
        pins.append(f'<g class="mpin" data-i="{i}" transform="translate({x:.1f},{y:.1f})"><circle class="mpin-halo" r="15"/><circle class="mpin-dot" r="9"/><text y="3.6" text-anchor="middle">{i}</text></g>')
    cities = []
    for key, name, dx in [('porto', 'Porto', -40)]:
        x, y = M['pins'][key]
        cities.append(f'<text class="mcity" x="{x+dx:.1f}" y="{y+4:.1f}">{name}</text>')
    return f'''<svg class="merv-svg" viewBox="{VB[0]} {VB[1]} {VB[2]} {VB[3]}" role="img" aria-label="Carte du Portugal">
          <defs><marker id="mArrowHead" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="marrow-head"/></marker></defs>
          <path class="mland-es" d="{M['es']}"/>
          <path class="mland-pt" d="{M['pt']}"/>
          <text class="mlabel-sea" x="32" y="{H*0.80:.0f}">OCEANO</text>
          <text class="mlabel-sea" x="32" y="{H*0.80+16:.0f}">ATLÂNTICO</text>
          {''.join(cities)}
          <path id="mArrow" class="marrow" d="" marker-end="url(#mArrowHead)"/>
          {''.join(pins)}
        </svg>'''

def item(i, key, photos, seven, extra):
    k = f'm{i}'
    if extra == 'video':
        media = f'''<a class="merv-photo merv-video" href="https://youtu.be/zbUbmYi2fHk" target="_blank" rel="noopener"><img src="images/{photos[0]}" alt="" loading="lazy"><span class="video-play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span><span class="video-label"><span class="yt-badge">YouTube</span><span i18n="merv_video_watch"></span></span></a>'''
    else:
        media = f'<div class="merv-photo" data-opt-photo="{photos[0]}"><img src="images/{photos[0]}" alt="" loading="lazy"></div>'
    facts = f'<ul class="merv-facts"><li i18n="{k}_f1"></li><li i18n="{k}_f2"></li></ul>'
    badge = '<span class="merv-badge" i18n="merv_7m"></span>' if seven else ''
    more = ''
    if extra == 'salt':
        more = f'<figure class="merv-sub" data-opt-photo="{photos[1]}"><img src="images/{photos[1]}" alt="" loading="lazy"><figcaption i18n="m2_salt_cap"></figcaption></figure>'
    if extra == 'expo':
        more = f'''<div class="merv-duo">
            <figure class="merv-sub" data-opt-photo="{photos[1]}"><img src="images/{photos[1]}" alt="" loading="lazy"><figcaption i18n="m7_expo_cap"></figcaption></figure>
            <div class="merv-ocean"><figure class="merv-sub" data-opt-photo="{photos[2]}"><img src="images/{photos[2]}" alt="" loading="lazy"></figure><h4 i18n="m7_ocean_t"></h4><p i18n="m7_ocean"></p></div>
          </div>'''
    if extra == 'cmp':
        R1 = 92; R2 = R1 * math.sqrt(250 / 580)
        more = f'''<div class="merv-cmp">
            <h4 i18n="m8_cmp_title"></h4>
            <svg viewBox="0 0 420 210" class="cmp-svg" role="img" aria-label="Léman 580 km², Alqueva 250 km²">
              <circle cx="110" cy="105" r="{R1}" class="cmp-leman"/><text x="110" y="100" text-anchor="middle" class="cmp-num">580 km²</text><text x="110" y="122" text-anchor="middle" class="cmp-lbl" data-i18n="m8_leman">Lac Léman</text>
              <circle cx="{215+R2+20:.1f}" cy="{105+R1-R2:.1f}" r="{R2:.1f}" class="cmp-alq"/><text x="{215+R2+20:.1f}" y="{100+R1-R2:.1f}" text-anchor="middle" class="cmp-num">250 km²</text><text x="{215+R2+20:.1f}" y="{122+R1-R2:.1f}" text-anchor="middle" class="cmp-lbl" data-i18n="m8_alqueva">Lac d'Alqueva</text>
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
          <div class="merv-list">{''.join(item(*it) for it in ITEMS)}
          </div>
        </div>
      </div>
    </section>

    @@cta:merv:conclusion@@
    </div>
'''

PIN_JS = json.dumps({str(i): [round(pin_xy(k)[0], 1), round(pin_xy(k)[1], 1)] for i, k, *_ in ITEMS})
ARROW_X = VB[0] + VB[2] - 4
