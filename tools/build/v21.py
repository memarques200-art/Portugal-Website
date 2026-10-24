# Dad's notes, round 3: home / geography / history changes applied to the base page
import re

ISLANDS = '''    <section class="geo-volcanic isl-sec">
      <div class="wrap">
        <div class="sec-head">
          <span class="sec-eyebrow" i18n="geo_volc_eyebrow"></span>
          <h2 class="sec-title" i18n="geo_volc_title"></h2>
          <p class="sec-lead" i18n="geo_volc_body"></p>
        </div>
        <div class="isl-grid">
          <article class="isl-card">
            <div class="isl-photos">
              <figure><img src="images/luis/sete-cidades.jpg" alt="Sete Cidades, São Miguel" loading="lazy"><figcaption i18n="isl_az_cap1"></figcaption></figure>
              <figure><img src="images/photos/x-acores2.jpg" alt="Lagoa do Fogo, São Miguel" loading="lazy"><figcaption i18n="isl_az_cap2"></figcaption></figure>
            </div>
            <div class="isl-body">
              <span class="isl-label" i18n="geo_volc_acores_label"></span>
              <p i18n="geo_volc_acores_desc"></p>
              <div class="isl-facts">
                <div><b>9</b><span i18n="isl_az_f1"></span></div>
                <div><b>1427</b><span i18n="isl_az_f2"></span></div>
                <div><b>2 351 m</b><span i18n="isl_az_f3"></span></div>
              </div>
            </div>
          </article>
          <article class="isl-card">
            <div class="isl-photos">
              <figure><img src="images/photos/x-madeira1.jpg" alt="Pico do Arieiro, Madère" loading="lazy"><figcaption i18n="isl_md_cap1"></figcaption></figure>
              <figure><img src="images/photos/x-madeira2.jpg" alt="Ponta de São Lourenço, Madère" loading="lazy"><figcaption i18n="isl_md_cap2"></figcaption></figure>
            </div>
            <div class="isl-body">
              <span class="isl-label" i18n="geo_volc_madeira_label"></span>
              <p i18n="geo_volc_madeira_desc"></p>
              <div class="isl-facts">
                <div><b>2</b><span i18n="isl_md_f1"></span></div>
                <div><b>1419</b><span i18n="isl_md_f2"></span></div>
                <div><b>1976</b><span i18n="isl_md_f3"></span></div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>
'''

FS_BTN = '''      <button class="fs-btn" id="fsBtn" type="button" hidden>
        <svg class="fs-in" viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>
        <svg class="fs-out" viewBox="0 0 24 24"><path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5"/></svg>
        <span data-i18n="fs_label">Plein écran</span>
      </button>
'''

FS_JS = '''<script>
  // cinema mode: hide the browser bars (Fullscreen API, needs a click)
  (function(){
    const d = document, el = d.documentElement, btn = d.getElementById('fsBtn');
    const req = el.requestFullscreen || el.webkitRequestFullscreen;
    if (!req) return;
    btn.hidden = false;
    const isFs = () => !!(d.fullscreenElement || d.webkitFullscreenElement);
    const enter = () => { if (!isFs()) { const p = req.call(el); if (p && p.catch) p.catch(() => {}); } };
    const exit = () => (d.exitFullscreen || d.webkitExitFullscreen).call(d);
    btn.addEventListener('click', () => isFs() ? exit() : enter());
    const sync = () => d.body.classList.toggle('is-fs', isFs());
    d.addEventListener('fullscreenchange', sync); d.addEventListener('webkitfullscreenchange', sync);
    // starting the presentation from the home page also goes full screen
    const start = d.querySelector('#view-home .cta-button');
    if (start) start.addEventListener('click', enter);
  })();
</script>
'''

THANKS_BAR = '''  <div class="thanks-bar">
    <div class="wrap"><span i18n="merci_bar"></span> <a href="https://www.loja-europeixe.ch/" target="_blank" rel="noopener">Europeixe</a> · <a href="https://share.google/KC0aDwi6yydgWgbBS" target="_blank" rel="noopener">Nortejo</a></div>
  </div>
'''

def apply(html, render, FR=None, keys=()):
    def sub1(old, new):
        nonlocal html
        assert html.count(old) == 1, (html.count(old), old[:80])
        html = html.replace(old, new)
    # islands: one section, two photos per archipelago
    a = html.index('    <section class="geo-volcanic">')
    b = html.index('</section>', a) + len('</section>\n')
    html = html[:a] + render(ISLANDS) + html[b:]
    # Asterix: note under the caption
    sub1('même dans Astérix&nbsp;!</span></div>',
         'même dans Astérix&nbsp;!</span>' + render('<span class="geo-extras-book-note" i18n="geo_ext_book_note"></span>') + '</div>')
    # founding of Portugal: Afonso Henriques instead of the castle
    sub1('src="images/photos/hist-guimaraes.jpg" alt="Château de Guimarães et statue de Dom Afonso Henriques"',
         'src="images/photos/x-afonso.jpg" alt="Statue de Dom Afonso Henriques, Guimarães"')
    # conclusion: close-up portrait for the round photo
    sub1('<img class="concl-portrait" src="images/luis.jpg"', '<img class="concl-portrait" src="images/luis-round.jpg"')
    # geography: Douro train photo for the north
    sub1('src="images/photos/geo-north.jpg"', 'src="images/luis/douro-train.jpg"')
    # full-screen ("cinema") button in the nav
    sub1('      <div class="lang-toggle" id="langToggle">', FS_BTN + '      <div class="lang-toggle" id="langToggle">')
    sub1('</body>', FS_JS + '</body>')
    # thank-you line at the bottom of every page
    sub1('  </main>\n', '  </main>\n' + render(THANKS_BAR))
    # refresh the French text baked into the base page for every key we overrode
    for k in keys:
        html = re.sub(r'(<(\w+)[^>]*\sdata-i18n="%s"[^>]*>).*?(</\2>)' % k, lambda m: m.group(1) + FR[k] + m.group(3), html, flags=re.S)
    return html
