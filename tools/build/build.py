import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n_new import T
from i18n_more import T2
T = {**T, **T2}

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1]
html = open(SRC).read()

def sub1(old, new):
    global html
    assert html.count(old) == 1, (html.count(old), old[:80])
    html = html.replace(old, new)

# ---------------- icons ----------------
def svg(body, sw=1.4):
    return f'<svg viewBox="0 0 24 24" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
ICONS = {
 "flag": svg('<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>'),
 "book": svg('<path d="M4 5.5A2.5 2.5 0 016.5 3H20v15H6.5A2.5 2.5 0 004 20.5v-15z"/><path d="M4 20.5A2.5 2.5 0 016.5 18H20v3H6.5"/><path d="M9 7h7M9 10.5h5"/>'),
 "people": svg('<circle cx="8.5" cy="8" r="3"/><circle cx="16" cy="9" r="2.4"/><path d="M2.5 20c0-3.6 2.7-6 6-6s6 2.4 6 6M14.5 20c0-2.8 1.8-4.8 4-4.8s4 2 4 4.8"/>'),
 "clock": svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
 "stars": svg('<circle cx="12" cy="12" r="9" stroke-dasharray="1.5 3.2"/><path d="M12 8.2l1.1 2.3 2.5.3-1.8 1.7.5 2.5-2.3-1.2-2.3 1.2.5-2.5-1.8-1.7 2.5-.3z"/>'),
 "crown": svg('<path d="M3 8l4.5 4L12 5l4.5 7L21 8l-2 11H5L3 8z"/><path d="M5 16h14"/>'),
 "columns": svg('<path d="M3 21h18M4 21V10M20 21V10M2 10l10-6 10 6M8 10v11M12 10v11M16 10v11"/>'),
 "briefcase": svg('<rect x="3" y="7" width="18" height="13" rx="1.5"/><path d="M8 7V5a2 2 0 012-2h4a2 2 0 012 2v2M3 12h18"/>'),
 "scales": svg('<path d="M12 3v18M7 21h10M4 7h16M6 7l-3 7a3 3 0 006 0L6 7zM18 7l-3 7a3 3 0 006 0l-3-7z"/>'),
 "city": svg('<path d="M3 21h18M5 21V9l5-3v15M10 21V4l6 3v14M16 21V11l3 1.5V21"/><path d="M7 12h1M7 15h1M12 9h2M12 12h2M12 15h2"/>'),
 "bridge": svg('<path d="M2 16h20M4 16V9M20 16V9M2 9c4 0 6 4 10 4s6-4 10-4M8 16v-3.5M12 16v-3M16 16v-3.5"/>'),
 "heart": svg('<path d="M12 20s-7.5-4.6-7.5-10a4.5 4.5 0 018.5-2 4.5 4.5 0 018.5 2c0 5.4-7.5 10-7.5 10z"/>'),
 "speech": svg('<path d="M4 4h13a3 3 0 013 3v7a3 3 0 01-3 3H10l-4 4v-4H4a3 3 0 01-3-3V7a3 3 0 013-3z"/>'),
 "family": svg('<circle cx="7" cy="6" r="2.4"/><circle cx="17" cy="6" r="2.4"/><circle cx="12" cy="12" r="1.9"/><path d="M3 20v-5a4 4 0 018 0M13 15a4 4 0 018 0v5M9.5 21v-2.5a2.5 2.5 0 015 0V21"/>'),
 "hands": svg('<path d="M2 12l4-4 4 2 3-2 4 1 5 3"/><path d="M6 8l5 6a1.5 1.5 0 002.2 0l.3-.3M9.5 15.5l1.5 1.5a1.5 1.5 0 002.1 0L19 11M2 12l5 5"/>'),
 "coffee": svg('<path d="M4 9h12v5a5 5 0 01-5 5H9a5 5 0 01-5-5V9zM16 10h1.5a2.5 2.5 0 010 5H16M3 21h14"/><path d="M8 3c-.8 1 .8 2 0 3M12 3c-.8 1 .8 2 0 3"/>'),
 "church": svg('<path d="M12 2v4M10 4h4M7 21V11l5-4 5 4v10M3 21h18M10 21v-4a2 2 0 014 0v4"/>'),
 "guitar": svg('<circle cx="9" cy="15" r="5"/><circle cx="9" cy="15" r="1.6"/><path d="M12.5 11.5L20 4M18 3l3 3"/>'),
 "tile": svg('<rect x="3" y="3" width="18" height="18" rx="1"/><path d="M12 3v18M3 12h18"/><circle cx="12" cy="12" r="3"/><path d="M3 3l4 4M21 3l-4 4M3 21l4-4M21 21l-4-4"/>'),
 "arch": svg('<path d="M4 21V10a8 8 0 0116 0v11M8 21v-9a4 4 0 018 0v9M2 21h20"/>'),
 "glass": svg('<path d="M7 3h10l-.5 6a4.5 4.5 0 01-9 0L7 3zM12 13.5V21M8 21h8M7.3 7h9.4"/>'),
 "trophy": svg('<path d="M8 4h8v5a4 4 0 01-8 0V4zM8 6H5a2.5 2.5 0 003 4M16 6h3a2.5 2.5 0 01-3 4M12 13v4M8.5 21h7M9.5 17h5l.5 4h-6z"/>'),
 "star": svg('<path d="M12 2l2.6 6.6L21 9.5l-5 4.6L17.5 21 12 17.3 6.5 21 8 14.1l-5-4.6 6.4-.9z"/>'),
 "ball": svg('<circle cx="12" cy="12" r="9"/><path d="M12 7.5l3.3 2.4-1.3 3.9H10l-1.3-3.9L12 7.5zM12 3v4.5M20.5 9.5l-4 1.5M3.5 9.5l4 1.5M15 18.5l-1-4.7M9 18.5l1-4.7"/>', 1.2),
 "wave": svg('<path d="M2 18c2 1.5 4 1.5 6 0s4-1.5 6 0 4 1.5 6 0"/><path d="M3 13c1-5 5-8 10-8 3 0 5 1.5 5 4-2-1-4 0-4 2 0 1.5 1 2 2 2"/>'),
 "skate": svg('<path d="M5 4h4l1 9h7a3 3 0 013 3H5V4z"/><circle cx="8" cy="19.5" r="1.5"/><circle cx="17" cy="19.5" r="1.5"/>'),
 "medal": svg('<circle cx="12" cy="15" r="5"/><path d="M8.5 11.5L5 3h4l3 6 3-6h4l-3.5 8.5M12 13v4"/>'),
 "chart": svg('<path d="M3 3v18h18"/><path d="M7 15l4-5 3 3 5-7"/>'),
 "wind": svg('<path d="M12 12v10M12 12l-1.5-9h3L12 12zM12 12l8 3.5-1.5 2.6L12 12zM12 12l-8 3.5 1.5 2.6L12 12z"/><path d="M8 22h8"/>'),
 "tree": svg('<path d="M12 21v-7M12 14c-4 0-7-2.5-7-6a7 7 0 0114 0c0 3.5-3 6-7 6zM12 14l-3-3M12 12l3-3M8 21h8"/>'),
 "carnation": '''<svg viewBox="0 0 200 260" aria-hidden="true">
   <path d="M100 250 C 98 200, 104 160, 100 110" stroke="#7FA88F" stroke-width="5" fill="none" stroke-linecap="round"/>
   <path d="M100 190 C 80 180, 64 160, 62 140 C 82 146, 96 164, 100 190z" fill="#5E8C72"/>
   <path d="M101 170 C 120 160, 134 142, 136 124 C 116 130, 104 148, 101 170z" fill="#5E8C72"/>
   <path d="M86 118 L 114 118 L 108 132 L 92 132 Z" fill="#5E8C72"/>
   <g fill="#C8423C">
     <path d="M100 30 c 8 10 22 4 26 16 c 12 2 16 14 8 22 c 8 8 2 22 -10 22 c -4 12 -18 14 -24 6 c -6 8 -20 6 -24 -6 c -12 0 -18 -14 -10 -22 c -8 -8 -4 -20 8 -22 c 4 -12 18 -6 26 -16z"/>
   </g>
   <g fill="#E05A50">
     <path d="M100 48 c 6 7 15 3 18 11 c 8 2 10 10 5 15 c 5 6 1 15 -7 15 c -3 8 -12 9 -16 4 c -4 5 -13 4 -16 -4 c -8 0 -12 -9 -7 -15 c -5 -5 -3 -13 5 -15 c 3 -8 12 -4 18 -11z"/>
   </g>
   <circle cx="100" cy="80" r="9" fill="#A83232"/>
 </svg>''',
}
def icon_sub(m):
    return ICONS[m.group(1)]

def cta(prefix, target):
    return f'''<section class="cta-section">
      <div class="wrap cta-content">
        <h3 class="cta-title" i18n="{prefix}_cta_title"></h3>
        <a class="cta-button" href="#{target}" data-view="{target}">
          <span i18n="{prefix}_cta_button"></span>
          <span class="cta-arrow">
            <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </span>
        </a>
      </div>
    </section>'''

def render(tpl):
    tpl = re.sub(r'@@cta:(\w+):(\w+)@@', lambda m: cta(m.group(1), m.group(2)), tpl)
    tpl = re.sub(r'@@(\w+)@@', icon_sub, tpl)
    def fill(m):
        tag, pre, key, post = m.groups()
        return f'<{tag}{pre} data-i18n="{key}"{post}>{FR[key]}</{tag}>'
    out = re.sub(r'<(\w+)([^>]*?) i18n="(\w+)"([^>]*)></\1>', fill, tpl)
    assert ' i18n="' not in out, re.findall(r'.{60} i18n=".{40}', out)[:3]
    return out

# ---------------- I18N merge ----------------
m = re.search(r'const I18N = (\{.*?\});\n', html)
I18N = json.loads(m.group(1))
for k, (fr, it, de) in T.items():
    I18N["fr"][k] = fr; I18N["it"][k] = it; I18N["de"][k] = de
FR = I18N["fr"]
for _l in I18N: I18N[_l].pop('concl_quote', None)

# ---------------- head ----------------
sub1('<title>Portugal — Une présentation</title>',
     '<title>Portugal — Une présentation</title>\n<meta name="description" content="Une présentation du Portugal par Luís Marques : géographie, histoire, institutions, société, culture, sport et régions.">\n<link rel="icon" href="images/crest.png">')

# ---------------- CSS ----------------
css = open(os.path.join(HERE, 'new.css')).read()
sub1('  .view{display:none;}', css + '\n  .view{display:none;}')

# ---------------- NAV ----------------
nav_old = re.search(r'<ul class="nav-links">.*?</ul>', html, re.S).group(0)
nav_new = '''<ul class="nav-links" id="navLinks">
        <li><a href="#home" class="nav-link active" data-view="home" data-i18n="nav_home">Accueil</a></li>
        <li><a href="#geographie" class="nav-link" data-view="geographie" data-i18n="nav_geo">Géographie</a></li>
        <li><a href="#histoire" class="nav-link" data-view="histoire" data-i18n="nav_hist">Histoire</a></li>
        <li><a href="#institutions" class="nav-link" data-view="institutions" data-i18n="nav_inst">Institutions</a></li>
        <li><a href="#societe" class="nav-link" data-view="societe" data-i18n="nav_soc">Société</a></li>
        <li><a href="#culture" class="nav-link" data-view="culture" data-i18n="nav_cult">Culture</a></li>
        <li><a href="#sport" class="nav-link" data-view="sport" data-i18n="nav_sport">Sport</a></li>
        <li><a href="#regions" class="nav-link" data-view="regions" data-i18n="nav_reg">Régions</a></li>
        <li><a href="#conclusion" class="nav-link" data-view="conclusion" data-i18n="nav_concl">Conclusion</a></li>
      </ul>'''
html = html.replace(nav_old, nav_new)
sub1('<a href="#" class="brand" data-view="home">', '<a href="#home" class="brand" data-view="home">')
sub1('<button class="nav-burger" aria-label="Menu">', '<button class="nav-burger" id="navBurger" aria-label="Menu" aria-expanded="false" aria-controls="navLinks">')

# home cards / CTA hrefs -> real hashes
html = re.sub(r'href="#" (class="(?:card|cta-button)") data-view="(\w+)"', r'href="#\2" \1 data-view="\2"', html)

# journey cards become links
JMAP = {"Géographie":"geographie","Histoire":"histoire","Institutions":"institutions","Société":"societe",
        "Culture":"culture","Gastronomie":"culture","Régions":"regions","Portugal & moi":"conclusion"}
def jcard(m):
    src, alt = m.group(1), m.group(2); v = JMAP[alt]
    return f'<a class="journey-card" href="#{v}" data-view="{v}">\n              <img src="{src}" alt="{alt}">'
html, n = re.subn(r'<div class="journey-card">\n\s*<img src="([^"]+)" alt="([^"]+)">', jcard, html)
assert n == 8, n
html, n = re.subn(r'(<span class="journey-label"[^>]*>[^<]*</span>\n\s*</div>\n\s*)</div>', r'\1</a>', html)
assert n == 8, n

# existing text fixes (visible FR text must match the dictionary)
for k in ("closing_quote", "geo_volc_acores_caption", "hist_c4_desc"):
    html, n = re.subn(r'(data-i18n="%s">)(.*?)(</p>)' % k, lambda m: m.group(1) + FR[k] + m.group(3), html, flags=re.S)
    assert n == 1, k

# Cabo da Roca fact
sub1('''vieilles de 175 millions d'années&nbsp;!</span>
            </li>''', '''vieilles de 175 millions d'années&nbsp;!</span>
            </li>
            <li>
              <span class="geo-extras-icon"><svg viewBox="0 0 24 24"><path d="M12 22s7-7.5 7-13a7 7 0 10-14 0c0 5.5 7 13 7 13z" stroke-width="1.4"/><circle cx="12" cy="9" r="2.4" stroke-width="1.4"/></svg></span>
              <span data-i18n="geo_ext_fact4">''' + FR["geo_ext_fact4"] + '''</span>
            </li>''')

# Windsor link
sub1('<a class="hist-card-link" href="#" data-i18n="hist_c3_link">',
     '<a class="hist-card-link" href="https://fr.wikipedia.org/wiki/Trait%C3%A9_de_Windsor_(1386)" target="_blank" rel="noopener" data-i18n="hist_c3_link">')

# ---------------- HISTOIRE timeline + CTA ----------------
years = ["1143","1297","1415","1494","1498","1500","1640","1755","1822","1910","1974","1986","1999","2002","2007"]
items = "\n".join(
    f'          <div class="tl-item{" tl-item--key" if y in ("1143","1974") else ""}"><span class="tl-year">{y}</span><p class="tl-text" i18n="hist_tl_{y}"></p></div>'
    for y in years)
SKEYS = ['st-cantino','st-nanban','st-1755','st-mendes','st-salazar','st-macau']
stories = '\n'.join(f'          <article class="story"><figure class="story-photo"><img src="images/photos/{SKEYS[i-1]}.jpg" alt="" loading="lazy"><figcaption i18n="hist_s{i}_cap"></figcaption></figure><div class="story-body"><span class="story-num">0{i}</span><h3 class="story-title" i18n="hist_s{i}_title"></h3><p class="story-text" i18n="hist_s{i}_text"></p></div></article>' for i in range(1,7))
timeline = f'''
    <section class="sec sec--white">
      <div class="wrap">
        <div class="sec-head">
          <span class="sec-eyebrow" i18n="hist_tl_eyebrow"></span>
          <h2 class="sec-title" i18n="hist_tl_title"></h2>
        </div>
        <div class="tl">
{items}
        </div>
      </div>
    </section>

    <section class="sec sec--ivory">
      <div class="wrap">
        <div class="sec-head">
          <span class="sec-eyebrow" i18n="hist_st_eyebrow"></span>
          <h2 class="sec-title" i18n="hist_st_title"></h2>
        </div>
        <div class="story-grid">
{stories}
        </div>
      </div>
    </section>

''' + open(os.path.join(HERE, 'smf_section.html')).read() + '''
    @@cta:hist:institutions@@
'''
sub1('''    </section>
    </div>
  </main>''', '    </section>\n' + render(timeline) + '    </div>\n' + render(open(os.path.join(HERE, 'views.html')).read()) + '  </main>')

# ---------------- SCRIPT ----------------
script = '''  <script>
    const nav = document.getElementById('siteNav');
    const onScroll = () => {
      if (window.scrollY > 40) nav.classList.add('scrolled');
      else nav.classList.remove('scrolled');
    };
    window.addEventListener('scroll', onScroll);
    onScroll();

    const navLinks = document.getElementById('navLinks');
    const burger = document.getElementById('navBurger');
    function closeMenu(){
      navLinks.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
    }
    burger.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = navLinks.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    function showView(name, push){
      const target = document.getElementById('view-' + name);
      if(!target){ return; }
      document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
      target.classList.add('active');
      document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
      document.querySelectorAll('.nav-link[data-view="' + name + '"]').forEach(l => l.classList.add('active'));
      closeMenu();
      if(push !== false && location.hash !== '#' + name){
        history.pushState(null, '', '#' + name);
      }
      window.scrollTo({top: 0, left: 0, behavior: 'auto'});
    }
    document.querySelectorAll('[data-view]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        showView(el.getAttribute('data-view'));
      });
    });
    function viewFromHash(){
      const name = location.hash.replace('#', '') || 'home';
      showView(document.getElementById('view-' + name) ? name : 'home', false);
    }
    window.addEventListener('popstate', viewFromHash);
    viewFromHash();

    // Arrow keys move between pages during the presentation
    const ORDER = ['home','geographie','histoire','institutions','societe','culture','sport','regions','conclusion'];
    document.addEventListener('keydown', (e) => {
      if(e.altKey || e.ctrlKey || e.metaKey) return;
      const current = (document.querySelector('.view.active') || {}).id || 'view-home';
      const i = ORDER.indexOf(current.replace('view-', ''));
      if(e.key === 'ArrowRight' && i < ORDER.length - 1) showView(ORDER[i + 1]);
      if(e.key === 'ArrowLeft' && i > 0) showView(ORDER[i - 1]);
    });

    const I18N = ''' + json.dumps(I18N, ensure_ascii=False, indent=1) + ''';

    function applyLanguage(lang){
      const dict = I18N[lang] || I18N.fr;
      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if(dict[key] !== undefined){
          el.innerHTML = dict[key];
        }
      });
      document.getElementById('langCurrent').textContent = lang.toUpperCase();
      document.querySelectorAll('.lang-option').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
      });
      document.documentElement.setAttribute('lang', lang);
      try { localStorage.setItem('lang', lang); } catch(e) {}
    }

    const langToggle = document.getElementById('langToggle');
    const langMenu = document.getElementById('langMenu');
    langToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      langMenu.classList.toggle('open');
    });
    document.addEventListener('click', () => {
      langMenu.classList.remove('open');
      closeMenu();
    });
    document.querySelectorAll('.lang-option').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        applyLanguage(btn.getAttribute('data-lang'));
        langMenu.classList.remove('open');
      });
    });

    // Reveal on scroll
    try {
      const sel = '.info-card, .dish-card, .region-card, .story, .pas-card, .fam-photo, .fest-card, .pillar, .step, .tl-item, .world-item, .pio-item, .card, .journey-card, .smf-photo, .video-frame, .life-photos figure';
      if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.documentElement.classList.add('js-reveal');
        const io = new IntersectionObserver((es) => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), {rootMargin: '0px 0px -8% 0px'});
        document.querySelectorAll(sel).forEach(el => { el.classList.add('rv'); io.observe(el); });
      }
    } catch(e) {}

    // Revolution songs: Spotify 30-second previews (track ids) or Spotify search fallback
    const SONGS = {
      adeus:    { spotify: '6ThJAONKSkyQxnfLmmtpIh', search: 'E Depois do Adeus Paulo de Carvalho' },
      grandola: { spotify: '7b0AYk76LUIOoE3IzbugaJ', search: 'Grândola Vila Morena Zeca Afonso' }
    };
    document.querySelectorAll('.song-card').forEach(card => {
      const s = SONGS[card.dataset.song];
      card.querySelector('.song-btn').addEventListener('click', () => {
        if (!s.spotify) { window.open('https://open.spotify.com/search/' + encodeURIComponent(s.search), '_blank', 'noopener'); return; }
        const player = card.querySelector('.song-player');
        if (card.classList.contains('playing')) { player.innerHTML = ''; card.classList.remove('playing'); return; }
        document.querySelectorAll('.song-card.playing').forEach(c => { c.classList.remove('playing'); c.querySelector('.song-player').innerHTML = ''; });
        player.innerHTML = '<iframe src="https://open.spotify.com/embed/track/' + s.spotify + '?utm_source=generator&theme=0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>';
        card.classList.add('playing');
      });
    });

    let savedLang = null;
    try { savedLang = localStorage.getItem('lang'); } catch(e) {}
    if(savedLang && savedLang !== 'fr' && I18N[savedLang]) applyLanguage(savedLang);

  </script>'''
s0 = html.index('  <script>'); s1 = html.index('  </script>') + len('  </script>')
html = html[:s0] + script + html[s1:]

# ---------------- optional personal photos: drop blocks whose image is missing ----------------
import os as _o2
_root = _o2.path.dirname(_o2.path.abspath(SRC))
def _drop(m):
    return m.group(0) if _o2.path.exists(_o2.path.join(_root, "images/luis", m.group(2))) else ""
html = re.sub(r'\n\s*<(article|figure|section) [^>]*data-opt="([^"]+)".*?</\1>', _drop, html, flags=re.S)
html = html.replace(' class="fam-grid">', ' class="fam-grid fam-n%d">' % len(re.findall(r'class="fam-photo', html)), 1)

# ---------------- real photos replace AI images ----------------
SWAP = {
 "images/hero-porto.jpg": "images/photos/hero-home.jpg",
 "images/journey-geo.jpg": "images/photos/j-geo.jpg",
 "images/journey-hist.jpg": "images/photos/j-hist.jpg",
 "images/journey-inst.jpg": "images/photos/inst-saobento.jpg",
 "images/journey-soc.jpg": "images/photos/j-soc.jpg",
 "images/journey-cult.jpg": "images/photos/j-cult.jpg",
 "images/journey-gastro.jpg": "images/photos/f-nata.jpg",
 "images/journey-reg.jpg": "images/photos/r-douro.jpg",
 "images/journey-moi.jpg": "images/photos/j-moi.jpg",
 "images/bridge-alps.jpg": "images/photos/bridge-alps.jpg",
 "images/geo-hero.jpg": "images/photos/hero-geo.jpg",
 "images/geo-north.jpg": "images/photos/geo-north.jpg",
 "images/geo-south.jpg": "images/photos/geo-south.jpg",
 "images/geo-climate-map.jpg": "images/photos/geo-climate.png",
 "images/geo-relief.jpg": "images/photos/geo-relief.jpg",
 "images/geo-acores.jpg": "images/photos/geo-acores.jpg",
 "images/geo-volcano.jpg": "images/photos/geo-volcano.jpg",
 "images/geo-madeira.jpg": "images/photos/geo-madeira.jpg",
 "images/hist-hero.jpg": "images/photos/hero-hist.jpg",
 "images/hist-flag.jpg": "images/photos/hist-flag.jpg",
 "images/hist-guimaraes.jpg": "images/photos/hist-guimaraes.jpg",
 "images/hist-windsor.jpg": "images/photos/hist-windsor.jpg",
 "images/hist-tea.jpg": "images/photos/hist-tea.jpg",
 "images/hist-routes-map.jpg": "images/photos/hist-routes.png",
}
import os as _os
ROOT = _os.path.dirname(_os.path.abspath(SRC))
for old, new in SWAP.items():
    if _os.path.exists(_os.path.join(ROOT, new)):
        html = html.replace('src="%s"' % old, 'src="%s"' % new)
missing = sorted(set(re.findall(r'src="(images/photos/[^"]+)"', html)) - {p for p in set(re.findall(r'src="(images/photos/[^"]+)"', html)) if _os.path.exists(_os.path.join(ROOT, p))})
if missing: print("MISSING PHOTOS:", missing)

# credits
CRED = _os.path.join(ROOT, "images/photos/credits.json")
if _os.path.exists(CRED):
    import html as _h
    cred = json.load(open(CRED))
    used = set(re.findall(r'src="images/photos/([^"]+)"', html))
    items = "\n".join(
        f'          <li><a href="{c["page"]}" target="_blank" rel="noopener">{_h.escape(c["title"][5:])}</a> — {_h.escape(c["artist"][:80])}, {_h.escape(c["lic"])}</li>'
        for f, c in sorted(cred.items()) if f in used)
    block = f'''
  <footer class="credits">
    <div class="wrap">
      <details>
        <summary data-i18n="credits_title">{FR["credits_title"]}</summary>
        <p style="margin-top:10px;" data-i18n="credits_intro">{FR["credits_intro"]}</p>
        <ol>
{items}
        </ol>
      </details>
    </div>
  </footer>
'''
    sub1('  </main>\n', '  </main>\n' + block)

# sanity: every data-i18n key exists in every language
keys = set(re.findall(r'data-i18n="(\w+)"', html))
for lang in ("fr", "it", "de"):
    missing = keys - set(I18N[lang])
    assert not missing, (lang, missing)
open(SRC, 'w').write(html)
print("ok", len(keys), "keys")
