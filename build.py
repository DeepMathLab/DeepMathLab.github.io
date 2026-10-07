#!/usr/bin/env python3
"""Build a portable bilingual static site using only the Python standard library."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
OUT = ROOT
OUT.mkdir(exist_ok=True)
PUBLIC_ORIGIN = "https://deepmathlab.github.io/"
ASSET_VERSION = "20261007-atlas2"
SHARE_IMAGE = PUBLIC_ORIGIN + "share-card.png?v=" + ASSET_VERSION

RESEARCH_SYMBOLS = {
    "geometry": '<path d="M8 39 24 9l28 10-14 28Z M8 39l44-20M24 9l14 38M14 28l29-4M18 19l28 11M18 42l13-31M28 45l12-30"/><circle cx="24" cy="9" r="2"/><circle cx="38" cy="47" r="2"/>',
    "fractional": '<path d="M8 46h46M12 48V10M12 42C16 21 19 15 23 29s7 13 11 2 7-6 10-3 5 2 9-1"/><path d="M12 42c8-5 13-9 20-12s13-5 21-6" stroke-dasharray="3 4"/>',
    "mechanics": '<path d="m10 40 30 9 14-23-30-9Z M10 40l14-23M20 43l14-23M30 46l14-23M15 32l30 9M20 25l30 9"/><path d="M28 8v11m-4-4 4 4 4-4M41 10v13m-4-4 4 4 4-4"/>'
}


def esc(value):
    return html.escape(str(value), quote=True)


def render(lang, page_path=None):
    def t(value):
        raw = value.get(lang, value.get("en", "")) if isinstance(value, dict) else value
        return (esc(raw).replace("\n", "<br>\n").replace("&lt;br&gt;", "<br>\n")
                .replace("&lt;span&gt;", "<span>").replace("&lt;/span&gt;", "</span>")
                )

    def c(key):
        return t(DATA["copy"][key])

    research = "".join(f'''
        <article class="research-item" id="research-{esc(item['id'])}">
          <div class="research-card-top"><svg class="research-symbol" viewBox="0 0 64 56" aria-hidden="true">{RESEARCH_SYMBOLS[item['id']]}</svg><span class="item-number">{esc(item['number'])}</span></div>
          <div class="research-titles"><h3 class="research-title">{t(item['title'])}</h3><p class="research-subtitle">{t(item['subtitle'])}</p></div>
          <div class="research-detail"><p>{t(item['description'])}</p><div class="tags">{''.join(f'<span>{esc(tag)}</span>' for tag in item['tags'])}</div></div>
        </article>''' for item in DATA["research"])
    members = "".join(f'''
        <article class="member"><div class="member-avatar" aria-hidden="true">{esc(member['initials'])}</div>
          <div class="member-name"><h4>{t(member['name'])}</h4><span>{t(member['name_secondary'])}</span></div>
          <div class="member-role"><p>{t(member['role'])}</p><span>{t(member['detail'])}</span></div>
        </article>''' for member in DATA["members"])
    publications = "".join(f'''
        <article class="publication" data-year="{item['year']}" data-search="{esc(' '.join([item['title'], item['authors'], item['journal'], item['doi']]).lower())}">
          <span class="pub-year">{item['year']}</span><div class="pub-body"><span class="pub-type">{t(item['topic'])}</span>
            <h3><a href="https://doi.org/{esc(item['doi'])}" target="_blank" rel="noopener noreferrer">{esc(item['title'])}<span class="pub-arrow" aria-hidden="true">↗</span></a></h3>
            <p class="pub-authors">{esc(item['authors'])}</p><p class="pub-journal"><span>{esc(item['journal'])}</span> · {esc(item['detail'])}</p><a class="pub-doi" href="https://doi.org/{esc(item['doi'])}" target="_blank" rel="noopener noreferrer">DOI: {esc(item['doi'])}<span aria-hidden="true">↗</span></a>
          </div></article>''' for item in DATA["publications"])
    years = sorted({p["year"] for p in DATA["publications"]}, reverse=True)
    options = "".join(f'<option value="{year}">{year}</option>' for year in years)
    navigation = "".join(f'<a href="#{name}">{t(label)}</a>' for name, label in DATA["nav"].items())
    alternate = "ko.html" if lang == "en" else "index.html"
    alternate_label = "한국어" if lang == "en" else "EN"
    title = "DeepMathLab | Computational Mathematics | KENTECH" if lang == "en" else "DeepMathLab | 김현주 교수 연구실 | KENTECH"
    canonical = PUBLIC_ORIGIN + (page_path if page_path is not None else ("ko.html" if lang == "ko" else ""))
    description = esc(DATA["copy"]["hero_intro"][lang])
    share_title = "DeepMathLab | KENTECH"
    share_alt = "DeepMathLab — Computational Mathematics and Scientific Computing at KENTECH"
    preview_footer = f'<p class="footer-note">{c("footer_note")}</p>' if DATA["preview"] else ""
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(DATA['copy']['hero_intro'][lang])}">
  <meta name="theme-color" content="#f7f8f5">
  <meta name="robots" content="{'noindex,nofollow' if DATA['preview'] else 'index,follow'}">
  <title>{title}</title>
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="DeepMathLab">
  <meta property="og:title" content="{share_title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:locale" content="{'ko_KR' if lang == 'ko' else 'en_US'}">
  <meta property="og:image" content="{SHARE_IMAGE}">
  <meta property="og:image:secure_url" content="{SHARE_IMAGE}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{share_alt}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{share_title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{SHARE_IMAGE}">
  <meta name="twitter:image:alt" content="{share_alt}">
  <link rel="image_src" href="{SHARE_IMAGE}">
  <link rel="icon" href="./favicon.svg?v={ASSET_VERSION}" type="image/svg+xml">
  <link rel="stylesheet" href="./styles.css?v={ASSET_VERSION}">
  <link rel="alternate" hreflang="en" href="./index.html">
  <link rel="alternate" hreflang="ko" href="./ko.html">
  <script src="./app.js" defer></script>
</head>
<body class="lang-{lang}" id="top">
  <a class="skip-link" href="#main">{c('skip')}</a>
  <header class="site-header"><div class="container header-inner">
    <a class="wordmark" href="{'index.html' if lang == 'en' else 'ko.html'}" aria-label="{title}">
      <svg class="logo" viewBox="0 0 40 40" aria-hidden="true"><rect x="1" y="1" width="38" height="38" rx="6" fill="#1d6258"/><path d="M11 29V11h7a8 8 0 0 1 0 18h-7m12-18v18m-7-18v18" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round"/></svg>
      <span><strong>{t(DATA['brand'])}</strong><small>{t(DATA['brand_sub'])}</small></span>
    </a>
    <div class="header-actions"><nav id="navigation" aria-label="{'Primary navigation' if lang == 'en' else '주 메뉴'}">{navigation}</nav>
      <a class="language-switch" href="./{alternate}" lang="{'ko' if lang == 'en' else 'en'}" aria-label="{'한국어 페이지로 전환' if lang == 'en' else 'Switch to English'}">{alternate_label}</a>
      <button class="menu-toggle" aria-label="{c('menu')}" aria-expanded="false" aria-controls="navigation"><span></span><span></span></button>
    </div>
  </div></header>
  <main id="main">
    <section class="hero container" aria-labelledby="hero-title">
      <div class="hero-copy"><div class="hero-eyebrow"><span class="eyebrow">DEEPMATHLAB / KENTECH</span></div>
        <h1 id="hero-title">{c('hero_title')}</h1><p class="hero-subtitle">{c('hero_subtitle')}</p>
        <p class="hero-intro">{c('hero_intro')}</p><p class="hero-affiliation">{c('hero_affiliation')} <a href="#people">{c('pi_name')}</a> · {c('hero_department')}</p><div class="hero-buttons"><a class="button-primary" href="#research">{c('hero_cta')}<span aria-hidden="true">↗</span></a><a class="button-primary button-secondary" href="#publications">{c('hero_secondary')}<span aria-hidden="true">→</span></a></div>
      </div>
      <figure class="hero-figure"><div class="figure-heading"><span>GEOMETRY / APPROXIMATION</span><span aria-hidden="true">FIG. 01</span></div><img src="./geometry-study.svg?v={ASSET_VERSION}" width="700" height="600" alt="{'Conceptual surface with a parameter lattice, projection guides, and approximation points' if lang == 'en' else '매개격자, 투영선, 근사점을 갖는 곡면 개념도'}"><figcaption><span class="figure-line" aria-hidden="true"></span>{c('figure_caption')}</figcaption></figure>
      <div class="hero-strip"><span class="strip-label">RESEARCH FOCUS</span><span>{c('hero_strip')}</span><span class="strip-arrow" aria-hidden="true">↘</span></div>
    </section>
    <section class="section research-section" id="research" aria-labelledby="research-heading"><div class="container">
      <div class="section-head"><div><p class="eyebrow section-number">01 / {t(DATA['nav']['research'])}</p><h2 id="research-heading">{c('research_heading')}</h2></div><div class="research-overview"><p class="section-intro">{c('research_intro')}</p><a class="text-link" href="{esc(DATA['research_url'])}" target="_blank" rel="noopener noreferrer">{c('research_source')}<span aria-hidden="true">↗</span></a></div></div>
      <div class="research-list">{research}</div>
    </div></section>
    <section class="section people-section container" id="people" aria-labelledby="people-heading">
      <div class="section-head"><div><p class="eyebrow section-number">02 / {t(DATA['nav']['people'])}</p><h2 id="people-heading">{c('people_heading')}</h2></div><span class="section-aside">KENTECH<br>NAJU, SOUTH KOREA</span></div>
      <article class="pi-profile"><figure class="pi-portrait"><img src="./hyunju-kim.jpg" width="123" height="148" alt="{'Hyunju Kim, Associate Professor at KENTECH' if lang == 'en' else 'KENTECH 김현주 부교수'}" loading="lazy"><figcaption>KENTECH · HYUNJU KIM</figcaption></figure>
        <div class="pi-text"><p class="eyebrow">{c('pi_label')}</p><h3>{c('pi_name')} <span>{'김현주' if lang == 'en' else 'Hyunju Kim'}</span></h3><p class="pi-role">{c('pi_role')}</p><p class="pi-department">{c('pi_department')}</p><p class="pi-description">{c('pi_description')}</p><p class="pi-education"><span>{c('education_label')}</span>{c('pi_education')}</p><a class="text-link" href="{esc(DATA['academic_url'])}" target="_blank" rel="noopener noreferrer">{c('profile_link')}<span aria-hidden="true">↗</span></a></div>
      </article>
      <div class="members-heading"><h3>{c('members_label')}</h3></div><div class="member-list">{members}</div><p class="members-note">{c('members_note')}</p>
    </section>
    <section class="section publications-section" id="publications" aria-labelledby="publications-heading"><div class="container">
      <div class="section-head"><div><p class="eyebrow section-number">03 / {t(DATA['nav']['publications'])}</p><h2 id="publications-heading">{c('publications_heading')}</h2></div><a class="text-link" href="{esc(DATA['publications_url'])}" target="_blank" rel="noopener noreferrer">{c('publications_source')}<span aria-hidden="true">↗</span></a></div>
      <p class="publications-intro">{c('publications_intro')}</p><div class="publication-tools">
        <label class="search-box"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="6.5"/><path d="m15 15 5 5"/></svg><span class="sr-only">{c('search_label')}</span><input id="publication-search" type="search" placeholder="{c('search_placeholder')}" autocomplete="off"></label>
        <label class="year-filter"><span class="sr-only">{c('filter_year_label')}</span><select id="publication-year"><option value="all">{c('filter_all_years')}</option>{options}</select></label>
      </div><div id="publication-list">{publications}</div><p class="no-results" hidden>{c('no_results')}</p><span id="result-status" class="sr-only" role="status" aria-live="polite"></span>
    </div></section>
    <section class="contact-section" id="contact" aria-labelledby="contact-heading"><div class="container contact-layout">
      <div class="contact-copy"><p class="eyebrow section-number">04 / {t(DATA['nav']['contact'])}</p><h2 id="contact-heading">{c('contact_heading')}</h2><p>{c('contact_intro')}</p><a class="contact-email" href="mailto:{esc(DATA['email'])}">{esc(DATA['email'])}<span aria-hidden="true">↗</span></a></div>
      <div class="contact-location"><p class="eyebrow">{c('location_label')}</p><p>{c('location')}</p><a class="text-link" href="{esc(DATA['institution_url'])}" target="_blank" rel="noopener noreferrer">{c('institution_link')}<span aria-hidden="true">↗</span></a><svg viewBox="0 0 220 130" aria-hidden="true"><path d="M0 15h220M0 45h220M0 75h220M0 105h220M25 0v130M65 0v130M105 0v130M145 0v130M185 0v130"/><path d="m25 105 80-60 80 30" class="location-path"/><circle cx="105" cy="45" r="5" class="location-point"/></svg></div>
    </div></section>
  </main>
  <footer class="site-footer"><div class="container"><div class="footer-top"><div><strong>{t(DATA['brand'])}</strong><span>Computational Mathematics & Scientific Computing</span></div><a class="text-link" href="#top">{c('back_top')}<span aria-hidden="true">↑</span></a></div><div class="footer-bottom"><span>© 2026 · DeepMathLab · KENTECH</span>{preview_footer}</div></div></footer>
</body>
</html>'''


for language, filename in [("en", "index.html"), ("ko", "ko.html"), ("en", "home.html")]:
    # A distinct, non-redirecting URL gives link crawlers a fresh preview entry.
    page_path = "home.html" if filename == "home.html" else None
    (OUT / filename).write_text(render(language, page_path), encoding="utf-8")
print("Built index.html, ko.html and home.html")
