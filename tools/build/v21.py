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
    # refresh the French text baked into the base page for every key we overrode
    for k in keys:
        html = re.sub(r'(<(\w+)[^>]*\sdata-i18n="%s"[^>]*>).*?(</\2>)' % k, lambda m: m.group(1) + FR[k] + m.group(3), html, flags=re.S)
    return html
