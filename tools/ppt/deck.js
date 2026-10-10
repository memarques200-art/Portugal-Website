const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { applyTheme } = require("/root/.claude/skills/synced/cae8f933-5e8e-4955-8e22-986853ff417a_b41ccf13-d79a-4d11-a292-fa69b1e7569b/pptx/scripts/apply_theme.js");

const F = JSON.parse(fs.readFileSync(__dirname + "/fr.json", "utf8"));
const CRED = JSON.parse(fs.readFileSync("/home/user/Portugal-Website/images/photos/credits.json", "utf8"));
const IMG = "/home/user/Portugal-Website/images/";
const P = (f) => IMG + "photos/" + f;
const L = (f) => IMG + "luis/" + f;
const OUT = process.argv[2] || "Portugal-Presentation.pptx";

const COL = { green: "174A3A", greenDk: "0F2E25", red: "A83232", gold: "B8955A", azul: "1E4F8F", ink: "17211D", grey: "4A524E", tint: "F1F4F2", tintBlue: "EAF0F8", white: "FFFFFF" };
const THEME = {
  name: "Portugal",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: { dk1: COL.ink, lt1: COL.white, dk2: COL.green, lt2: COL.tint, accent1: COL.green, accent2: COL.red, accent3: COL.gold, accent4: COL.azul, accent5: "5E2230", accent6: "7FA88F", hlink: COL.azul, folHlink: "5E2230" },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = "Portugal — Une présentation";
pres.author = "Luís Marques";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const W = 13.333, H = 7.5, MX = 0.6;

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: COL.white },
  objects: [
    { text: { text: "PORTUGAL · Luís Marques", options: { x: MX, y: 7.02, w: 6, h: 0.3, fontSize: 10, color: "8A918D", fontFace: "Calibri", charSpacing: 2 } } },
  ],
  slideNumber: { x: 12.2, y: 7.02, w: 0.6, h: 0.3, fontSize: 10, color: "8A918D", fontFace: "Calibri", align: "right" },
});
pres.defineSlideMaster({ title: "BLEED", background: { color: COL.greenDk } });
pres.defineSlideMaster({
  title: "DARK",
  background: { color: COL.green },
  slideNumber: { x: 12.2, y: 7.02, w: 0.6, h: 0.3, fontSize: 10, color: "B9C9C1", fontFace: "Calibri", align: "right" },
});

let section = "";
function sec(t) { section = t; pres.addSection({ title: t }); }
function add(master) { return pres.addSlide({ masterName: master || "CONTENT", sectionTitle: section }); }

function tb(s, text, o) { s.addText(text, Object.assign({ isTextBox: true, fontFace: "Calibri", color: COL.ink, valign: "top", margin: 0 }, o)); }
function head(s, eyebrow, title, opt = {}) {
  const dark = opt.dark;
  tb(s, eyebrow, { x: MX, y: 0.45, w: 12, h: 0.3, fontSize: 12, bold: true, charSpacing: 3, color: dark ? "F2C14E" : COL.red });
  tb(s, title, { x: MX, y: 0.75, w: opt.w || 12, h: 0.75, fontSize: opt.size || 34, bold: true, fontFace: "Cambria", color: dark ? COL.white : COL.green });
}
function img(s, path, x, y, w, h, o = {}) {
  s.addImage(Object.assign({ path, x, y, w, h, sizing: { type: "cover", w, h } }, o));
}
function shadow() { return { type: "outer", color: "000000", opacity: 0.18, blur: 8, offset: 3, angle: 90 }; }
function card(s, x, y, w, h, fill) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill || COL.tint }, line: { color: fill || COL.tint }, rectRadius: 0.08, shadow: shadow() });
}
function caption(s, text, x, y, w) {
  s.addShape(pres.shapes.RECTANGLE, { x, y: y - 0.42, w, h: 0.42, fill: { color: "000000", transparency: 45 }, line: { color: "000000", transparency: 100 } });
  tb(s, text, { x: x + 0.12, y: y - 0.38, w: w - 0.24, h: 0.34, fontSize: 11, color: COL.white, valign: "middle", bold: true });
}
function dot(s, x, y, color, label) {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.5, h: 0.5, fill: { color }, line: { color } });
  if (label) tb(s, label, { x, y, w: 0.5, h: 0.5, fontSize: 14, bold: true, color: COL.white, align: "center", valign: "middle", fontFace: "Cambria" });
}
function link(s, text, url, x, y, w, color) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.5, fill: { color: color || COL.red }, line: { color: color || COL.red }, rectRadius: 0.25 });
  s.addText([{ text, options: { hyperlink: { url }, color: COL.white, bold: true } }], { isTextBox: true, x, y, w, h: 0.5, fontSize: 14, align: "center", valign: "middle", fontFace: "Calibri", margin: 0 });
}
const ACC = [COL.green, COL.red, COL.azul, COL.gold];

// full-bleed hero divider
function divider(num, titleKey, subKey, textKey, photo, pos) {
  const s = add("BLEED");
  img(s, photo, 0, 0, W, H);
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 7.4, h: H, fill: { color: "08140F", transparency: 30 }, line: { color: "08140F", transparency: 100 } });
  tb(s, num + " / 08", { x: 0.9, y: 2.0, w: 5, h: 0.4, fontSize: 16, bold: true, color: "F2C14E", charSpacing: 3 });
  tb(s, F[titleKey], { x: 0.9, y: 2.45, w: 6.3, h: 1.4, fontSize: 60, bold: true, fontFace: "Cambria", color: COL.white, fit: "shrink" });
  tb(s, F[subKey], { x: 0.9, y: 3.95, w: 6.0, h: 1.0, fontSize: 24, fontFace: "Cambria", italic: true, color: COL.white });
  if (textKey) tb(s, F[textKey], { x: 0.9, y: 5.0, w: 5.6, h: 1.1, fontSize: 15, color: "E6ECE8" });
  s.addNotes(F[subKey] + ". " + (textKey ? F[textKey] : ""));
  return s;
}
function stat(s, x, y, w, big, label, color, dark) {
  tb(s, big, { x, y, w, h: 0.75, fontSize: 36, bold: true, fontFace: "Cambria", color: color || COL.green });
  tb(s, label, { x, y: y + 0.75, w, h: 0.6, fontSize: 13, bold: true, color: dark ? "E6ECE8" : COL.grey });
}

// =====================================================================
sec("Accueil");
{ // 1 title
  const s = add("BLEED");
  img(s, P("hero-home.jpg"), 0, 0, W, H);
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 7.6, h: H, fill: { color: "08140F", transparency: 35 }, line: { color: "08140F", transparency: 100 } });
  tb(s, "BIENVENUE AU", { x: 0.9, y: 1.9, w: 6, h: 0.4, fontSize: 16, bold: true, color: "F2C14E", charSpacing: 4 });
  tb(s, "Portugal", { x: 0.9, y: 2.3, w: 6.5, h: 1.6, fontSize: 96, bold: true, fontFace: "Cambria", color: COL.white });
  tb(s, F.hero_subtitle, { x: 0.9, y: 3.95, w: 6.2, h: 0.6, fontSize: 26, fontFace: "Cambria", color: COL.white });
  tb(s, F.hero_quote, { x: 0.9, y: 4.65, w: 5.8, h: 1.2, fontSize: 17, italic: true, fontFace: "Cambria", color: "E6ECE8" });
  tb(s, "Luís Marques", { x: 0.9, y: 6.2, w: 5, h: 0.4, fontSize: 16, bold: true, color: COL.white });
  s.addNotes("Bienvenue. " + F.hero_quote);
}
{ // 2 qui suis-je
  const s = add();
  img(s, IMG + "luis.jpg", MX, 0.6, 4.1, 6.2, { rounding: false });
  tb(s, F.intro_eyebrow, { x: 5.3, y: 0.7, w: 7, h: 0.3, fontSize: 12, bold: true, charSpacing: 3, color: COL.red });
  tb(s, "Faisons connaissance", { x: 5.3, y: 1.0, w: 7.4, h: 0.8, fontSize: 38, bold: true, fontFace: "Cambria", color: COL.green });
  tb(s, F.intro_subtitle, { x: 5.3, y: 1.8, w: 7, h: 0.5, fontSize: 22, italic: true, fontFace: "Cambria", color: COL.gold });
  const items = [[F.stat1_label, "Caramulo, Viseu"], [F.stat2_label, "2013 — " + F.stat2_sub], [F.stat3_label, F.stat3_value], [F.stat4_label, "Voyages · Sport · Gastronomie · Culture"]];
  items.forEach(([lab, val], i) => {
    const x = 5.3 + (i % 2) * 3.8, y = 2.65 + Math.floor(i / 2) * 2.05;
    card(s, x, y, 3.55, 1.8);
    dot(s, x + 0.25, y + 0.25, ACC[i]);
    tb(s, lab, { x: x + 0.25, y: y + 0.88, w: 3.1, h: 0.3, fontSize: 12, bold: true, charSpacing: 2, color: COL.red });
    tb(s, val, { x: x + 0.25, y: y + 1.18, w: 3.1, h: 0.55, fontSize: 16, bold: true, color: COL.ink });
  });
  s.addNotes("Je suis Luís Marques, originaire de Caramulo (Viseu). Arrivé en Suisse en 2013. " + F.stat3_value + ".");
}
{ // 3 coup d'oeil
  const s = add();
  head(s, "EN BREF", F.glance_title, { w: 7.6 });
  const t = [[F.glance_capital_label, "Lisbonne"], [F.glance_pop_label, F.glance_pop_value], [F.glance_area_label, "92 212 km²"], [F.glance_lang_label, F.glance_lang_value], [F.glance_currency_label, "Euro (€)"], [F.glance_sea_label, F.glance_sea_value]];
  t.forEach(([lab, val], i) => {
    const x = MX + (i % 3) * 2.55, y = 1.95 + Math.floor(i / 3) * 2.35;
    card(s, x, y, 2.35, 2.1);
    dot(s, x + 0.25, y + 0.25, ACC[i % 4]);
    tb(s, lab, { x: x + 0.25, y: y + 0.95, w: 1.95, h: 0.3, fontSize: 13, color: COL.grey });
    tb(s, val, { x: x + 0.25, y: y + 1.25, w: 1.95, h: 0.7, fontSize: 18, bold: true, color: COL.ink, fit: "shrink" });
  });
  img(s, P("j-geo.jpg"), 8.6, 0.6, 4.13, 6.2);
  caption(s, "Ponta da Piedade, Algarve", 8.6, 6.8, 4.13);
  s.addNotes("Capitale Lisbonne, environ 10,6 millions d'habitants, 92 212 km², langue portugaise, euro, façade sur l'océan Atlantique.");
}
{ // 4 parcours (journey)
  const s = add();
  head(s, "PROGRAMME", F.journey_title);
  const j = [["01", F.journey_geo, P("j-geo.jpg")], ["02", F.journey_hist, P("j-hist.jpg")], ["03", F.journey_inst, P("inst-saobento.jpg")], ["04", F.journey_soc, P("j-soc.jpg")], ["05", "Culture & gastronomie", P("j-cult.jpg")], ["06", "Sport", P("hero-sport.jpg")], ["07", F.journey_reg, P("r-douro.jpg")], ["08", "Conclusion", L("caramulo-vue.jpg")]];
  j.forEach(([n, t, ph], i) => {
    const x = MX + (i % 4) * 3.07, y = 1.85 + Math.floor(i / 4) * 2.55;
    img(s, ph, x, y, 2.87, 2.3);
    s.addShape(pres.shapes.RECTANGLE, { x, y: y + 1.45, w: 2.87, h: 0.85, fill: { color: "000000", transparency: 40 }, line: { color: "000000", transparency: 100 } });
    tb(s, n, { x: x + 0.18, y: y + 1.5, w: 1, h: 0.3, fontSize: 13, bold: true, color: "F2C14E", fontFace: "Cambria" });
    tb(s, t, { x: x + 0.18, y: y + 1.8, w: 2.6, h: 0.4, fontSize: 18, bold: true, color: COL.white, fontFace: "Cambria" });
  });
}
{ // 5 bridge
  const s = add("BLEED");
  img(s, P("bridge-alps.jpg"), 0, 0, W, H);
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: H, fill: { color: "08140F", transparency: 45 }, line: { color: "08140F", transparency: 100 } });
  img(s, IMG + "flag-pt.jpg", 4.6, 2.0, 0.8, 0.8, { rounding: true });
  img(s, IMG + "flag-ch.jpg", 7.93, 2.0, 0.8, 0.8, { rounding: true });
  tb(s, "Portugal  —  Suisse", { x: 1, y: 2.9, w: W - 2, h: 0.9, fontSize: 44, bold: true, fontFace: "Cambria", color: COL.white, align: "center" });
  tb(s, F.bridge_subtitle, { x: 1, y: 3.85, w: W - 2, h: 0.6, fontSize: 24, italic: true, fontFace: "Cambria", color: "F2C14E", align: "center" });
  tb(s, F.bridge_text, { x: 2.4, y: 4.6, w: W - 4.8, h: 1.2, fontSize: 18, color: COL.white, align: "center" });
}

// =====================================================================
sec("01 Géographie");
divider("01", "geo_hero_title", "geo_hero_subtitle", "geo_hero_text", P("hero-geo.jpg"));
{
  const s = add();
  head(s, F.geo_loc_eyebrow, "À l'extrémité sud-ouest de l'Europe", { w: 6.4, size: 26 });
  img(s, IMG + "geo-map-europe.jpg", 7.1, 0.6, 5.63, 6.2);
  tb(s, F.geo_loc_body, { x: MX, y: 1.7, w: 6.0, h: 1.1, fontSize: 16, color: COL.ink });
  const st = [["561 km", "du nord au sud"], ["218 km", "d'est en ouest"], ["832 km", "de côte atlantique"], ["1 993 m", "Serra da Estrela, point culminant du continent"], ["2 351 m", "Pico (Açores), point culminant du pays"]];
  st.forEach(([b, l], i) => {
    const x = MX + (i % 3) * 2.05, y = 3.15 + Math.floor(i / 3) * 1.75;
    stat(s, x, y, 1.95, b, l, ACC[i % 4]);
  });
  s.addNotes(F.geo_loc_body);
}
{
  const s = add();
  head(s, F.geo_dual_eyebrow, "Deux visages, un même pays");
  img(s, P("geo-north.jpg"), MX, 1.75, 6.0, 3.0); caption(s, F.geo_dual_f1_label, MX, 4.75, 6.0);
  img(s, P("geo-south.jpg"), 6.73, 1.75, 6.0, 3.0); caption(s, F.geo_dual_f2_label, 6.73, 4.75, 6.0);
  tb(s, F.geo_dual_f1_desc + "  " + F.geo_cr_f1_desc, { x: MX, y: 5.0, w: 6.0, h: 0.9, fontSize: 15 });
  tb(s, F.geo_dual_f2_desc + "  " + F.geo_cr_f2_desc, { x: 6.73, y: 5.0, w: 6.0, h: 0.9, fontSize: 15 });
  tb(s, F.geo_cr_climate_body, { x: MX, y: 6.05, w: 12.1, h: 0.7, fontSize: 14, italic: true, color: COL.grey });
  s.addNotes(F.geo_cr_climate_body);
}
{
  const s = add();
  head(s, F.geo_volc_eyebrow, "Madère et Açores, terres de volcans");
  tb(s, F.geo_volc_body, { x: MX, y: 1.65, w: 12, h: 0.7, fontSize: 16 });
  const v = [[P("geo-acores.jpg"), F.geo_volc_acores_label, F.geo_volc_acores_desc], [P("geo-volcano.jpg"), "CAPELINHOS (1957-1958)", F.geo_volc_acores_caption], [P("geo-madeira.jpg"), F.geo_volc_madeira_label, F.geo_volc_madeira_desc]];
  v.forEach(([ph, t, d], i) => {
    const x = MX + i * 4.1;
    img(s, ph, x, 2.55, 3.9, 2.6);
    tb(s, t, { x, y: 5.3, w: 3.9, h: 0.35, fontSize: 14, bold: true, color: COL.red, charSpacing: 1 });
    tb(s, d, { x, y: 5.65, w: 3.9, h: 1.2, fontSize: 14 });
  });
}
{
  const s = add();
  head(s, F.geo_ext_footer, "Petits faits étonnants", { w: 7.2 });
  const facts = [F.geo_ext_fact1, F.geo_ext_fact2, F.geo_ext_fact3, F.geo_ext_fact4];
  facts.forEach((f, i) => {
    const y = 1.8 + i * 1.2;
    dot(s, MX, y + 0.05, ACC[i], String(i + 1));
    tb(s, f, { x: MX + 0.75, y, w: 6.2, h: 1.0, fontSize: 16 });
  });
  card(s, 8.1, 0.6, 4.63, 6.2, COL.tintBlue);
  tb(s, F.geo_ext_luis_eyebrow, { x: 8.4, y: 0.85, w: 4.1, h: 0.3, fontSize: 11, bold: true, color: COL.azul, charSpacing: 2 });
  tb(s, F.geo_ext_luis_title, { x: 8.4, y: 1.15, w: 4.1, h: 0.5, fontSize: 22, bold: true, fontFace: "Cambria", color: COL.ink });
  tb(s, F.geo_ext_luis_desc, { x: 8.4, y: 1.7, w: 4.1, h: 0.9, fontSize: 14 });
  s.addImage({ path: IMG + "asterix.jpg", x: 9.55, y: 2.7, w: 1.75, h: 2.33, sizing: { type: "contain", w: 1.75, h: 2.33 } });
  tb(s, F.geo_ext_book_caption, { x: 8.4, y: 5.25, w: 4.1, h: 0.6, fontSize: 13, italic: true, fontFace: "Cambria", align: "center", color: COL.grey });
}

// =====================================================================
sec("02 Histoire");
divider("02", "hist_hero_title", "hist_hero_subtitle", "hist_hero_text", P("hero-hist.jpg"));
{
  const s = add();
  head(s, "SYMBOLES & ALLIANCES", "Une identité forgée au fil des siècles");
  const c = [[P("hist-flag.jpg"), F.hist_c1_title, F.hist_c1_desc], [P("hist-guimaraes.jpg"), F.hist_c2_title, F.hist_c2_desc], [P("hist-windsor.jpg"), F.hist_c3_title, F.hist_c3_desc], [P("hist-tea.jpg"), F.hist_c4_title, F.hist_c4_desc]];
  c.forEach(([ph, t, d], i) => {
    const x = MX + i * 3.07;
    card(s, x, 1.75, 2.87, 5.05, COL.white);
    img(s, ph, x, 1.75, 2.87, 2.0);
    tb(s, t, { x: x + 0.2, y: 3.9, w: 2.5, h: 0.65, fontSize: 18, bold: true, fontFace: "Cambria", color: COL.green });
    tb(s, d, { x: x + 0.2, y: 4.6, w: 2.5, h: 2.1, fontSize: 13, fit: "shrink" });
  });
}
{
  const s = add();
  img(s, P("hist-routes.png"), 4.6, 0.6, 8.13, 6.2, { sizing: { type: "contain", w: 8.13, h: 6.2 } });
  head(s, "LES DÉCOUVERTES", "Un empire de routes maritimes", { w: 4.2 });
  tb(s, F.hist_routes_desc, { x: MX, y: 2.4, w: 3.8, h: 1.0, fontSize: 16 });
  ["Afrique", "Inde", "Brésil", "Chine", "Japon"].forEach((p, i) => {
    dot(s, MX, 3.6 + i * 0.6, ACC[i % 4]);
    tb(s, p, { x: MX + 0.7, y: 3.6 + i * 0.6, w: 3, h: 0.5, fontSize: 17, bold: true, valign: "middle" });
  });
}
{
  const s = add();
  head(s, F.hist_tl_eyebrow, F.hist_tl_title);
  const yrs = [["1143", "hist_tl_1143"], ["1415", "hist_tl_1415"], ["1494", "hist_tl_1494"], ["1498", "hist_tl_1498"], ["1500", "hist_tl_1500"], ["1755", "hist_tl_1755"], ["1910", "hist_tl_1910"], ["1974", "hist_tl_1974"], ["1986", "hist_tl_1986"], ["1999", "hist_tl_1999"]];
  [0, 1].forEach((row) => {
    const y = 2.1 + row * 2.45;
    s.addShape(pres.shapes.LINE, { x: MX, y: y + 0.25, w: 12.1, h: 0, line: { color: "C9CFCB", width: 2 } });
    yrs.slice(row * 5, row * 5 + 5).forEach(([yr, k], i) => {
      const x = MX + i * 2.45, key = yr === "1143" || yr === "1974";
      s.addShape(pres.shapes.OVAL, { x: x + 0.05, y: y + 0.1, w: 0.3, h: 0.3, fill: { color: key ? COL.red : COL.white }, line: { color: key ? COL.red : COL.gold, width: 2.5 } });
      tb(s, yr, { x, y: y + 0.5, w: 2.3, h: 0.55, fontSize: 26, bold: true, fontFace: "Cambria", color: key ? COL.red : COL.azul });
      tb(s, F[k], { x, y: y + 1.05, w: 2.25, h: 1.2, fontSize: 12 });
    });
  });
  s.addNotes(yrs.map(([y, k]) => y + " : " + F[k]).join("\n"));
}
{
  const s = add();
  head(s, F.hist_st_eyebrow, F.hist_st_title);
  const st = [["st-cantino.jpg", F.hist_s1_title, "1494 : le traité de Tordesillas partage le monde. C'est pour cela que le Brésil parle portugais."],
    ["st-nanban.jpg", F.hist_s2_title, "1543 : armes à feu, pain (« pan » vient de « pão ») et peut-être la tempura."],
    ["st-1755.jpg", F.hist_s3_title, "1755 : séisme et tsunami. Pombal reconstruit avec l'une des premières constructions parasismiques."],
    ["st-mendes.jpg", F.hist_s4_title, "1940 : le consul Sousa Mendes défie Salazar et sauve des milliers de réfugiés."],
    ["st-salazar.jpg", F.hist_s5_title, "1926-1974 : censure, police politique, émigration « a salto » vers la France."],
    ["st-macau.jpg", F.hist_s6_title, "Guerres coloniales, indépendances, puis Macao rendue à la Chine en 1999."]];
  st.forEach(([ph, t, d], i) => {
    const x = MX + (i % 3) * 4.1, y = 1.7 + Math.floor(i / 3) * 2.65;
    img(s, P(ph), x, y, 1.75, 2.35);
    tb(s, "0" + (i + 1), { x: x + 1.95, y, w: 1, h: 0.3, fontSize: 13, bold: true, color: COL.gold, fontFace: "Cambria" });
    tb(s, t, { x: x + 1.95, y: y + 0.3, w: 1.95, h: 0.75, fontSize: 16, bold: true, fontFace: "Cambria", color: COL.green });
    tb(s, d, { x: x + 1.95, y: y + 1.05, w: 1.95, h: 1.3, fontSize: 12 });
  });
  s.addNotes([1, 2, 3, 4, 5, 6].map((i) => F["hist_s" + i + "_title"] + " — " + F["hist_s" + i + "_text"]).join("\n\n"));
}
{
  const s = add();
  img(s, P("smf-castle.jpg"), 0, 0, 6.2, H);
  tb(s, F.smf_eyebrow, { x: 6.75, y: 0.6, w: 6, h: 0.5, fontSize: 12, bold: true, charSpacing: 2, color: COL.red });
  tb(s, F.smf_title, { x: 6.75, y: 1.05, w: 6, h: 0.9, fontSize: 24, bold: true, fontFace: "Cambria", color: COL.green });
  tb(s, F.smf_text, { x: 6.75, y: 2.0, w: 6, h: 1.25, fontSize: 15 });
  tb(s, "Viagem Medieval", { x: 6.75, y: 3.3, w: 6, h: 0.5, fontSize: 22, bold: true, fontFace: "Cambria", color: COL.azul });
  tb(s, F.smf_viagem_text, { x: 6.75, y: 3.8, w: 6, h: 1.4, fontSize: 14 });
  [["650 000", F.smf_f1], ["12", F.smf_f2], ["1996", F.smf_f3]].forEach(([b, l], i) => stat(s, 6.75 + i * 2.0, 5.2, 1.9, b, l, ACC[i]));
  link(s, "▶  Regarder la vidéo", "https://youtu.be/s8ip94klcQs", 6.75, 6.45, 2.8);
  s.addNotes("Santa Maria da Feira : " + F.smf_text + " " + F.smf_viagem_text);
}

// =====================================================================
sec("03 Institutions");
divider("03", "inst_hero_title", "inst_hero_subtitle", "inst_hero_text", P("hero-inst.jpg"));
{
  const s = add();
  head(s, F.inst_pow_eyebrow, F.inst_pow_title);
  tb(s, F.inst_pow_lead, { x: MX, y: 1.55, w: 12, h: 0.45, fontSize: 15, color: COL.grey });
  const c = [["inst-belem.jpg", "inst_p1"], ["inst-saobento.jpg", "inst_p2"], ["inst-praca.jpg", "inst_p3"], ["inst-tc.jpg", "inst_p4"]];
  c.forEach(([ph, k], i) => {
    const x = MX + i * 3.07;
    card(s, x, 2.15, 2.87, 4.65, COL.white);
    img(s, P(ph), x, 2.15, 2.87, 1.65);
    tb(s, F[k + "_tag"], { x: x + 0.2, y: 3.95, w: 2.5, h: 0.3, fontSize: 11, bold: true, color: ACC[i], charSpacing: 2 });
    tb(s, F[k + "_title"], { x: x + 0.2, y: 4.25, w: 2.5, h: 0.65, fontSize: 17, bold: true, fontFace: "Cambria", color: COL.ink });
    tb(s, F[k + "_who"], { x: x + 0.2, y: 4.95, w: 2.5, h: 0.65, fontSize: 13, bold: true, color: COL.green });
    tb(s, F[k + "_desc"], { x: x + 0.2, y: 5.6, w: 2.5, h: 1.1, fontSize: 11, color: COL.grey, fit: "shrink" });
  });
}
{
  const s = add("DARK");
  head(s, "25 · IV · 1974", F.inst_rev_title, { dark: true, w: 6.5 });
  tb(s, F.inst_rev_text, { x: MX, y: 1.75, w: 6.3, h: 3.6, fontSize: 15, color: COL.white });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: MX, y: 5.55, w: 6.3, h: 0.6, fill: { color: COL.red }, line: { color: COL.red }, rectRadius: 0.3 });
  tb(s, F.inst_rev_note, { x: MX + 0.2, y: 5.55, w: 5.9, h: 0.6, fontSize: 13, bold: true, color: COL.white, valign: "middle" });
  img(s, P("inst-1974.jpg"), 7.4, 0.6, 5.33, 3.4);
  tb(s, F.inst_rev_cap, { x: 7.4, y: 4.05, w: 5.33, h: 0.5, fontSize: 10, color: "B9C9C1" });
  tb(s, F.inst_rev_songs.toUpperCase(), { x: 7.4, y: 4.7, w: 5.3, h: 0.3, fontSize: 12, bold: true, color: "F2C14E", charSpacing: 2 });
  [["22:55", "« E Depois do Adeus »", "Paulo de Carvalho", "https://open.spotify.com/track/6ThJAONKSkyQxnfLmmtpIh"], ["00:20", "« Grândola, Vila Morena »", "Zeca Afonso", "https://open.spotify.com/track/7b0AYk76LUIOoE3IzbugaJ"]].forEach(([t, song, a, url], i) => {
    const y = 5.1 + i * 0.85;
    tb(s, t, { x: 7.4, y, w: 1.2, h: 0.6, fontSize: 24, bold: true, fontFace: "Cambria", color: "F2C14E" });
    s.addText([{ text: "▶ " + song, options: { hyperlink: { url }, color: COL.white, bold: true } }, { text: "\n" + a + " (cliquer pour écouter)", options: { color: "B9C9C1", fontSize: 11 } }], { isTextBox: true, x: 8.65, y, w: 4.1, h: 0.75, fontSize: 16, fontFace: "Calibri", margin: 0, valign: "top" });
  });
  s.addNotes(F.inst_rev_text);
}
{
  const s = add();
  head(s, "PORTUGAL — SUISSE", F.inst_cmp_title);
  const hdr = (t) => ({ text: t, options: { bold: true, color: COL.white, fill: { color: COL.green }, fontSize: 15 } });
  const rows = [[hdr(""), hdr("🇵🇹  Portugal"), hdr("🇨🇭  Suisse")]];
  for (let i = 1; i <= 6; i++) {
    const shade = i % 2 ? COL.tint : COL.white;
    rows.push([{ text: F["inst_cmp_r" + i].toUpperCase(), options: { bold: true, color: COL.red, fontSize: 12, fill: { color: shade } } }, { text: F["inst_cmp_r" + i + "_pt"], options: { fill: { color: shade } } }, { text: F["inst_cmp_r" + i + "_ch"], options: { fill: { color: shade } } }]);
  }
  s.addTable(rows, { x: MX, y: 1.8, w: 12.1, colW: [2.5, 4.8, 4.8], fontSize: 15, fontFace: "Calibri", color: COL.ink, border: { type: "solid", pt: 0.5, color: "D5DAD7" }, rowH: 0.62, valign: "middle", margin: 0.1 });
}
{
  const s = add();
  head(s, F.inst_pio_eyebrow, F.inst_pio_title);
  [["1867", F.inst_pio1], ["2001", F.inst_pio2], ["2010", F.inst_pio3], ["7e", F.inst_pio4]].forEach(([b, t], i) => {
    const x = MX + i * 3.07;
    card(s, x, 1.75, 2.87, 2.75);
    tb(s, b, { x: x + 0.2, y: 1.9, w: 2.5, h: 0.75, fontSize: 38, bold: true, fontFace: "Cambria", color: ACC[i] });
    tb(s, t, { x: x + 0.2, y: 2.7, w: 2.5, h: 1.7, fontSize: 12, fit: "shrink" });
  });
  tb(s, F.inst_world_title, { x: MX, y: 4.8, w: 12, h: 0.5, fontSize: 22, bold: true, fontFace: "Cambria", color: COL.green });
  [["OTAN", F.inst_w1_desc], ["Union européenne", F.inst_w2_desc], ["ONU", F.inst_w3_desc], ["CPLP", F.inst_w4_desc]].forEach(([b, t], i) => {
    const x = MX + i * 3.07;
    tb(s, b, { x, y: 5.4, w: 2.9, h: 0.45, fontSize: 18, bold: true, fontFace: "Cambria", color: COL.gold });
    tb(s, t, { x, y: 5.85, w: 2.87, h: 1.0, fontSize: 12 });
  });
}
// =====================================================================
sec("04 Société");
divider("04", "soc_hero_title", "soc_hero_subtitle", "soc_hero_text", P("hero-soc.jpg"));
{
  const s = add();
  head(s, F.soc_life_eyebrow, F.soc_life_title);
  [["10,6 M", F.soc_stat1], ["≈ 2,9 M", "Région de Lisbonne"], ["≈ 1,7 M", "Région de Porto"], ["≈ 81 ans", "Espérance de vie"], ["≈ 260 M", "Lusophones dans le monde"]].forEach(([b, l], i) => stat(s, MX + i * 2.45, 1.7, 2.3, b, l, ACC[i % 4]));
  const c = [[null, F.soc_l1_title, F.soc_l1_desc], [null, F.soc_l2_title, F.soc_l2_desc], [P("e-cafe.jpg"), F.soc_l3_title, F.soc_l3_desc], [P("e-fatima.jpg"), F.soc_l4_title, F.soc_l4_desc]];
  c.forEach(([ph, t, d], i) => {
    const x = MX + i * 3.07;
    card(s, x, 3.3, 2.87, 3.5, COL.white);
    if (ph) img(s, ph, x, 3.3, 2.87, 1.5); else { s.addShape(pres.shapes.RECTANGLE, { x, y: 3.3, w: 2.87, h: 1.5, fill: { color: i ? COL.tintBlue : COL.tint }, line: { color: COL.tint } }); dot(s, x + 1.18, 3.8, ACC[i]); }
    tb(s, t, { x: x + 0.2, y: 4.95, w: 2.5, h: 0.45, fontSize: 18, bold: true, fontFace: "Cambria", color: COL.green });
    tb(s, d, { x: x + 0.2, y: 5.4, w: 2.5, h: 1.3, fontSize: 13 });
  });
}
{
  const s = add();
  head(s, F.soc_lang_eyebrow, F.soc_lang_title, { w: 7.2, size: 26 });
  tb(s, F.soc_lang_body, { x: MX, y: 1.7, w: 7.0, h: 1.0, fontSize: 15 });
  card(s, MX, 2.9, 7.0, 1.9, COL.tintBlue);
  tb(s, "Saudade", { x: MX + 0.3, y: 3.0, w: 6.4, h: 0.8, fontSize: 40, italic: true, bold: true, fontFace: "Cambria", color: COL.azul });
  tb(s, F.soc_saudade_text, { x: MX + 0.3, y: 3.8, w: 6.4, h: 0.95, fontSize: 13 });
  tb(s, F.soc_dia_title, { x: MX, y: 5.05, w: 7, h: 0.45, fontSize: 20, bold: true, fontFace: "Cambria", color: COL.green });
  stat(s, MX, 5.5, 3.3, "≈ 2 M", "Portugais nés au Portugal vivant à l'étranger", COL.red);
  stat(s, MX + 3.6, 5.5, 3.4, "≈ 250 000", "Portugais en Suisse (j'en fais partie depuis 2013)", COL.azul);
  card(s, 8.2, 0.6, 4.53, 6.2);
  tb(s, F.soc_words_title, { x: 8.5, y: 0.85, w: 4, h: 0.5, fontSize: 18, bold: true, fontFace: "Cambria" });
  [["Olá", F.soc_w1], ["Bom dia", F.soc_w2], ["Obrigado / Obrigada", F.soc_w3], ["Até logo", F.soc_w4]].forEach(([pt, fr], i) => {
    const y = 1.6 + i * 1.25;
    tb(s, pt, { x: 8.5, y, w: 4, h: 0.55, fontSize: 24, italic: true, bold: true, fontFace: "Cambria", color: COL.azul });
    tb(s, fr, { x: 8.5, y: y + 0.55, w: 4, h: 0.4, fontSize: 15, color: COL.grey });
  });
  s.addNotes(F.soc_dia_text + " " + F.soc_dia_ch_text);
}
{
  const s = add();
  head(s, F.soc_eco_eyebrow, F.soc_eco_title);
  const c = [[null, F.soc_eco1_title, F.soc_eco1], [P("e-wind.jpg"), F.soc_eco2_title, F.soc_eco2], [P("e-cork.jpg"), F.soc_eco3_title, F.soc_eco3], [null, F.soc_eco4_title, F.soc_eco4]];
  c.forEach(([ph, t, d], i) => {
    const x = MX + i * 3.07;
    card(s, x, 1.75, 2.87, 5.05, COL.white);
    if (ph) img(s, ph, x, 1.75, 2.87, 2.0); else { s.addShape(pres.shapes.RECTANGLE, { x, y: 1.75, w: 2.87, h: 2.0, fill: { color: i ? COL.tintBlue : COL.tint }, line: { color: COL.tint } }); tb(s, i ? "1,5 M" : "78 Md €", { x, y: 2.35, w: 2.87, h: 0.8, fontSize: 36, bold: true, fontFace: "Cambria", color: ACC[i], align: "center" }); }
    tb(s, t, { x: x + 0.2, y: 3.9, w: 2.5, h: 0.7, fontSize: 18, bold: true, fontFace: "Cambria", color: COL.green });
    tb(s, d, { x: x + 0.2, y: 4.65, w: 2.5, h: 2.05, fontSize: 13 });
  });
}
// =====================================================================
sec("05 Culture");
divider("05", "cult_hero_title", "cult_hero_subtitle", "cult_hero_text", P("hero-cult.jpg"));
{
  const s = add();
  head(s, F.cult_arts_eyebrow, F.cult_arts_title);
  [["c-fado.jpg", "cult_a1"], ["c-azulejo.jpg", "cult_a2"], ["c-manuelino.jpg", "cult_a3"], ["c-pessoa.jpg", "cult_a4"]].forEach(([ph, k], i) => {
    const x = MX + i * 3.07;
    card(s, x, 1.75, 2.87, 5.05, COL.white);
    img(s, P(ph), x, 1.75, 2.87, 2.3);
    tb(s, F[k + "_title"], { x: x + 0.2, y: 4.2, w: 2.5, h: 0.5, fontSize: 19, bold: true, fontFace: "Cambria", color: COL.green });
    tb(s, F[k + "_desc"], { x: x + 0.2, y: 4.75, w: 2.5, h: 1.95, fontSize: 13 });
  });
}
{
  const s = add();
  head(s, F.cult_food_eyebrow, F.cult_food_title);
  const d = [["f-bacalhau", "Bacalhau"], ["f-nata", "Pastel de nata"], ["f-francesinha", "Francesinha"], ["f-sardinhas", "Sardinhas assadas"], ["f-caldo", "Caldo verde"], ["f-leitao", "Leitão da Bairrada"], ["f-polvo", "Polvo à lagareiro"], ["f-cataplana", "Cataplana"], ["f-bifana", "Bifana"], ["f-queijo", "Queijo da Serra"], ["f-alheira", "Alheira"], ["f-ovos", "Ovos moles"]];
  d.forEach(([ph, n], i) => {
    const x = MX + (i % 6) * 2.04, y = 1.75 + Math.floor(i / 6) * 2.55;
    img(s, P(ph + ".jpg"), x, y, 1.9, 1.85);
    tb(s, n, { x, y: y + 1.92, w: 1.9, h: 0.4, fontSize: 14, bold: true, italic: true, fontFace: "Cambria", color: COL.green });
  });
  s.addNotes(d.map(([, n], i) => n + " : " + F["cult_d" + (i + 1) + "_desc"]).join("\n"));
}
{
  const s = add();
  head(s, F.cult_world_eyebrow, F.cult_world_title, { w: 7.5, size: 26 });
  [["Tempura", "Japon", F.cult_w1], ["Vindaloo", "Inde", F.cult_w2], ["Piri-piri", "Asie & Afrique", F.cult_w3], ["Kasutera", "Japon", F.cult_w4], ["Marmelada", "Europe", F.cult_w5]].forEach(([n, r, t], i) => {
    const y = 1.75 + i * 1.02;
    tb(s, n, { x: MX, y, w: 1.9, h: 0.45, fontSize: 20, bold: true, italic: true, fontFace: "Cambria", color: ACC[i % 4] });
    tb(s, r.toUpperCase(), { x: MX, y: y + 0.45, w: 1.9, h: 0.3, fontSize: 10, bold: true, color: COL.grey, charSpacing: 1 });
    tb(s, t, { x: MX + 2.0, y, w: 5.3, h: 0.95, fontSize: 13 });
  });
  card(s, 8.4, 0.6, 4.33, 6.2, "5E2230");
  tb(s, F.cult_wine_eyebrow, { x: 8.7, y: 0.85, w: 3.8, h: 0.3, fontSize: 12, bold: true, color: "F2C14E", charSpacing: 2 });
  [["Vinho do Porto", F.cult_v1_desc], ["Vinho verde", F.cult_v2_desc], ["Dão", F.cult_v3_desc]].forEach(([n, t], i) => {
    const y = 1.3 + i * 1.8;
    tb(s, n, { x: 8.7, y, w: 3.8, h: 0.55, fontSize: 24, bold: true, italic: true, fontFace: "Cambria", color: COL.white });
    tb(s, t, { x: 8.7, y: y + 0.55, w: 3.8, h: 1.1, fontSize: 13, color: "F1E4E7" });
  });
}
{
  const s = add();
  head(s, F.cult_fest_eyebrow, F.cult_fest_title);
  [["c-diaportugal.jpg", F.cult_f1_date, "Dia de Portugal", F.cult_f1_desc], ["c-santoantonio.jpg", F.cult_f2_date, "Santo António", F.cult_f2_desc], ["c-saojoao.jpg", F.cult_f3_date, "São João", F.cult_f3_desc]].forEach(([ph, dt, n, t], i) => {
    const x = MX + i * 4.1;
    img(s, P(ph), x, 1.75, 3.9, 2.7);
    tb(s, dt, { x, y: 4.6, w: 3.9, h: 0.6, fontSize: 28, bold: true, fontFace: "Cambria", color: COL.red });
    tb(s, n.toUpperCase(), { x, y: 5.2, w: 3.9, h: 0.3, fontSize: 12, bold: true, charSpacing: 2 });
    tb(s, t, { x, y: 5.55, w: 3.9, h: 1.2, fontSize: 14 });
  });
}
// =====================================================================
sec("06 Sport");
divider("06", "sport_hero_title", "sport_hero_subtitle", "sport_hero_text", P("hero-sport.jpg"));
{
  const s = add();
  img(s, P("s-ronaldo.jpg"), 0, 0, 4.6, H);
  tb(s, F.sport_foot_eyebrow, { x: 5.1, y: 0.45, w: 7, h: 0.3, fontSize: 12, bold: true, charSpacing: 3, color: COL.red });
  tb(s, F.sport_foot_title, { x: 5.1, y: 0.75, w: 7.6, h: 0.75, fontSize: 34, bold: true, fontFace: "Cambria", color: COL.green });
  card(s, 5.1, 1.7, 7.63, 2.35, COL.green);
  [["2016", F.sport_t1], ["2019", F.sport_t2], ["2025", F.sport_t3]].forEach(([y, t], i) => {
    tb(s, y, { x: 5.4, y: 1.9 + i * 0.68, w: 1.2, h: 0.55, fontSize: 26, bold: true, fontFace: "Cambria", color: "F2C14E" });
    tb(s, t, { x: 6.7, y: 1.95 + i * 0.68, w: 5.9, h: 0.55, fontSize: 15, color: COL.white });
  });
  tb(s, "Cristiano Ronaldo", { x: 5.1, y: 4.3, w: 7.6, h: 0.5, fontSize: 22, bold: true, fontFace: "Cambria", color: COL.ink });
  tb(s, F.sport_cr7_desc, { x: 5.1, y: 4.8, w: 7.6, h: 0.75, fontSize: 15 });
  tb(s, F.sport_leg_desc + " " + F.sport_clubs_desc, { x: 5.1, y: 5.6, w: 7.6, h: 1.2, fontSize: 14, color: COL.grey });
}
{
  const s = add();
  head(s, F.sport_more_eyebrow, F.sport_more_title);
  img(s, P("hero-sport-card.jpg"), MX, 1.75, 6.0, 3.6);
  tb(s, F.sport_m1_title, { x: MX, y: 5.5, w: 6, h: 0.45, fontSize: 20, bold: true, fontFace: "Cambria", color: COL.azul });
  tb(s, F.sport_video_text, { x: MX, y: 5.95, w: 4.0, h: 0.9, fontSize: 13 });
  link(s, "▶  Vidéo Nazaré", "https://youtu.be/ZfLSN4mxY0E", 4.7, 6.05, 1.9, COL.azul);
  [["s-hockey.jpg", "sport_m2"], [null, "sport_m3"], [null, "sport_m4"]].forEach(([ph, k], i) => {
    const y = 1.75 + i * 1.72, x = 6.95;
    card(s, x, y, 5.78, 1.55);
    if (ph) img(s, P(ph), x, y, 1.8, 1.55); else dot(s, x + 0.65, y + 0.52, ACC[i + 1]);
    tb(s, F[k + "_title"], { x: x + 2.0, y: y + 0.15, w: 3.6, h: 0.4, fontSize: 18, bold: true, fontFace: "Cambria", color: COL.green });
    tb(s, F[k + "_desc"], { x: x + 2.0, y: y + 0.6, w: 3.6, h: 0.9, fontSize: 13 });
  });
}
{
  const s = add("BLEED");
  s.background = { color: "0F2A4F" };
  img(s, P("s-rbar.jpg"), 0, 0, 7.2, H);
  tb(s, F.rbar_eyebrow, { x: 7.7, y: 1.1, w: 5.2, h: 0.4, fontSize: 12, bold: true, color: "F2C14E", charSpacing: 2 });
  tb(s, "RED BULL AIR RACE", { x: 7.7, y: 1.5, w: 5.3, h: 0.8, fontSize: 36, bold: true, italic: true, fontFace: "Calibri", color: COL.white });
  tb(s, F.rbar_text, { x: 7.7, y: 2.45, w: 5.1, h: 2.6, fontSize: 15, color: COL.white });
  stat(s, 7.7, 5.2, 2.3, "2007", F.rbar_f1, "F2C14E", true);
  stat(s, 10.1, 5.2, 2.8, "1 000 000", F.rbar_f2, "F2C14E", true);
  tb(s, F.rbar_cap, { x: 0.3, y: 7.05, w: 6.6, h: 0.3, fontSize: 10, color: COL.white });
}
// =====================================================================
sec("07 Régions");
divider("07", "reg_hero_title", "reg_hero_subtitle", "reg_hero_text", P("hero-reg.jpg"));
{
  const s = add();
  head(s, F.reg_eyebrow, F.reg_title);
  const r = [["r-porto.jpg", F.reg_n_name, "Porto · Braga · Guimarães"], ["r-coimbra.jpg", F.reg_c_name, "Coimbra · Aveiro · Viseu ★"], ["r-lisboa.jpg", F.reg_l_name, "Lisboa · Sintra · Cascais"], ["r-evora.jpg", F.reg_al_name, "Évora · Beja"], ["r-algarve.jpg", F.reg_ag_name, "Faro · Lagos"], ["r-acores.jpg", F.reg_az_name, "Ponta Delgada"], ["r-madeira.jpg", F.reg_m_name, "Funchal"]];
  r.forEach(([ph, n, c], i) => {
    const row = i < 4 ? 0 : 1, col = row ? i - 4 : i, w = 2.87, x = MX + col * 3.07 + (row ? 1.53 : 0), y = 1.75 + row * 2.6;
    img(s, P(ph), x, y, w, 1.7);
    tb(s, n, { x, y: y + 1.78, w, h: 0.4, fontSize: 18, bold: true, fontFace: "Cambria", color: i === 1 ? COL.red : COL.green });
    tb(s, c, { x, y: y + 2.15, w, h: 0.3, fontSize: 12, color: COL.grey });
  });
  s.addNotes(["n", "c", "l", "al", "ag", "az", "m"].map((k) => F["reg_" + k + "_name"] + " : " + F["reg_" + k + "_desc"]).join("\n"));
}
{
  const s = add();
  img(s, L("caramulo-vue.jpg"), 7.3, 0.6, 5.43, 3.9);
  img(s, P("r-caramulo2.jpg"), 7.3, 4.65, 2.62, 2.15);
  card(s, 10.1, 4.65, 2.63, 2.15, COL.tintBlue);
  tb(s, "1 076 m", { x: 10.25, y: 4.85, w: 2.4, h: 0.6, fontSize: 28, bold: true, fontFace: "Cambria", color: COL.azul });
  tb(s, F.reg_car_f1, { x: 10.25, y: 5.5, w: 2.35, h: 1.1, fontSize: 12 });
  head(s, F.reg_car_eyebrow, "Caramulo, la montagne de l'air pur", { w: 6.4, size: 26 });
  tb(s, F.reg_car_text, { x: MX, y: 1.75, w: 6.3, h: 3.0, fontSize: 16 });
  stat(s, MX, 5.0, 3, "1920s", F.reg_car_f2, COL.green);
  stat(s, MX + 3.2, 5.0, 3, "1953", F.reg_car_f3, COL.red);
}
{
  const s = add("BLEED");
  img(s, L("motorfestival.jpg"), 0, 0, W, H);
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 7.8, h: H, fill: { color: "1E0808", transparency: 20 }, line: { color: "1E0808", transparency: 100 } });
  tb(s, F.cmf_eyebrow, { x: 0.8, y: 0.9, w: 6.5, h: 0.4, fontSize: 12, bold: true, color: "F2C14E", charSpacing: 2 });
  tb(s, "CARAMULO MOTORFESTIVAL", { x: 0.8, y: 1.3, w: 6.8, h: 1.3, fontSize: 40, bold: true, italic: true, color: COL.white });
  tb(s, F.cmf_text, { x: 0.8, y: 2.7, w: 6.5, h: 2.4, fontSize: 15, color: COL.white });
  [["60 000+", F.cmf_f3], ["3", F.cmf_f1], ["180+", F.cmf_f2]].forEach(([b, l], i) => stat(s, 0.8 + i * 2.2, 5.15, 2.1, b, l, "F2C14E", true));
  link(s, "▶  Regarder la vidéo", "https://youtu.be/jJedre8t3Go", 0.8, 6.55, 2.8);
  s.addNotes(F.cmf_text);
}
// =====================================================================
sec("08 Conclusion");
divider("08", "concl_hero_title", "concl_hero_subtitle", "concl_hero_text", P("hero-concl.jpg"));
{
  const s = add();
  head(s, F.concl_life_eyebrow, F.concl_life_title);
  const st = [["concl_t1_d", "concl_t1"], ["concl_t1b_d", "concl_t1b"], ["concl_t2_d", "concl_t2"], ["concl_t3_d", "concl_t3"], ["concl_t4_d", "concl_t4"], ["concl_t5_d", "concl_t5"]];
  s.addShape(pres.shapes.LINE, { x: MX + 0.25, y: 2.0, w: 11.6, h: 0, line: { color: "C9CFCB", width: 2 } });
  st.forEach(([d, t], i) => {
    const x = MX + i * 2.04;
    dot(s, x, 1.75, ACC[i % 4], "0" + (i + 1));
    tb(s, F[d], { x, y: 2.4, w: 1.9, h: 0.75, fontSize: 17, bold: true, fontFace: "Cambria", color: i % 2 ? COL.azul : COL.red });
    tb(s, F[t], { x, y: 3.15, w: 1.9, h: 1.8, fontSize: 12 });
  });
  [[L("caramulo-vue.jpg"), F.concl_ph_caramulo], [P("smf-castle2.jpg"), F.concl_ph_feira], [L("lac.jpg"), "Le Léman, ma vie en Suisse"]].forEach(([ph, c], i) => {
    const x = MX + i * 4.1;
    img(s, ph, x, 5.05, 3.9, 1.75);
    caption(s, c, x, 6.8, 3.9);
  });
}
{
  const s = add();
  head(s, F.concl_pas_eyebrow, F.concl_pas_title);
  const p = [["moto-alpes.jpg", "concl_p_moto"], ["moto-garage.jpg", "concl_p_meca"], ["parapente.jpg", "concl_p_para"], ["jura.jpg", "concl_p_sort"], ["lac.jpg", "concl_p_lac"], ["tanay.jpg", "concl_p_walk"]];
  p.forEach(([ph, k], i) => {
    const x = MX + (i % 3) * 4.1, y = 1.7 + Math.floor(i / 3) * 2.6;
    img(s, L(ph), x, y, 1.9, 2.4);
    tb(s, F[k + "_t"], { x: x + 2.05, y, w: 1.9, h: 0.75, fontSize: 16, bold: true, fontFace: "Cambria", color: COL.green });
    tb(s, F[k], { x: x + 2.05, y: y + 0.75, w: 1.9, h: 1.65, fontSize: 11, fit: "shrink" });
  });
  s.addNotes(p.map(([, k]) => F[k + "_t"] + " : " + F[k]).join("\n"));
}
{
  const s = add();
  head(s, F.concl_fam_eyebrow, F.concl_fam_title, { w: 5 });
  tb(s, F.concl_fam_text, { x: MX, y: 1.7, w: 4.3, h: 1.6, fontSize: 16 });
  img(s, L("famille-portugal.jpg"), 5.2, 0.6, 7.53, 4.1);
  [L("famille-diner.jpg"), L("famille-diner2.jpg"), L("famille.jpg")].forEach((ph, i) => img(s, ph, 5.2 + i * 2.56, 4.85, 2.41, 1.95));
  img(s, IMG + "luis.jpg", MX, 3.5, 2.2, 3.3);
}
{
  const s = add();
  head(s, F.concl_eyebrow, "Ce que le Portugal représente pour moi");
  [["concl_p1", COL.green], ["concl_p2", COL.red], ["concl_p3", COL.azul]].forEach(([k, c], i) => {
    const x = MX + i * 4.1;
    card(s, x, 2.0, 3.9, 4.0);
    dot(s, x + 1.7, 2.35, c);
    tb(s, F[k + "_title"], { x: x + 0.3, y: 3.1, w: 3.3, h: 0.6, fontSize: 26, bold: true, fontFace: "Cambria", color: c, align: "center" });
    tb(s, F[k + "_desc"], { x: x + 0.3, y: 3.8, w: 3.3, h: 2.0, fontSize: 16 });
  });
}
{
  const s = add("DARK");
  tb(s, "Obrigado!", { x: 0, y: 2.0, w: W, h: 1.8, fontSize: 96, bold: true, italic: true, fontFace: "Cambria", color: "F2C14E", align: "center" });
  tb(s, F.concl_thanks, { x: 0, y: 3.9, w: W, h: 0.6, fontSize: 24, color: COL.white, align: "center" });
  tb(s, F.concl_questions, { x: 0, y: 4.6, w: W, h: 0.7, fontSize: 30, italic: true, fontFace: "Cambria", color: COL.white, align: "center" });
  img(s, IMG + "flag-pt.jpg", 5.86, 5.7, 0.7, 0.7, { rounding: true });
  img(s, IMG + "flag-ch.jpg", 6.77, 5.7, 0.7, 0.7, { rounding: true });
}
// credits
sec("Crédits");
{
  const items = Object.entries(CRED).sort().map(([f, c]) => c.title.replace(/^File:/, "").replace(/\.[a-z]+$/i, "").slice(0, 48) + " — " + (c.artist || "").slice(0, 26) + ", " + c.lic);
  const per = 34;
  for (let p = 0; p * per < items.length; p++) {
    const s = add();
    head(s, "SOURCES", F.credits_title + (items.length > per ? " (" + (p + 1) + ")" : ""));
    tb(s, F.credits_intro, { x: MX, y: 1.5, w: 12, h: 0.35, fontSize: 12, color: COL.grey });
    const chunk = items.slice(p * per, p * per + per);
    [0, 1].forEach((c) => tb(s, chunk.slice(c * 17, c * 17 + 17).join("\n"), { x: MX + c * 6.15, y: 1.95, w: 6.0, h: 4.9, fontSize: 10, color: COL.grey, paraSpaceAfter: 2 }));
  }
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
