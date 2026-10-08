#!/usr/bin/env python3
"""Build an English-only research website with Python's standard library."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'site.json').read_text(encoding='utf-8'))
PUBLIC_ORIGIN = 'https://deepmathlab.github.io/'
ASSET_VERSION = DATA['site_version']
SHARE_IMAGE = PUBLIC_ORIGIN + 'share-card.png?v=' + ASSET_VERSION
FONT_STYLESHEET = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400&family=Inter:wght@400;500;600&family=Manrope:wght@500;600;700&display=swap'
PAGES = ['home', 'research', 'people', 'publications', 'join', 'contact', 'not-found']
if DATA.get('resources'):
    PAGES.append('resources')
if DATA.get('news'):
    PAGES.append('news')
SYMBOLS = {
    'geometry': '<path d="M8 39 24 9l28 10-14 28Z M8 39l44-20M24 9l14 38M14 28l29-4M18 19l28 11M18 42l13-31M28 45l12-30"/><circle cx="24" cy="9" r="2"/><circle cx="38" cy="47" r="2"/>',
    'fractional': '<path d="M8 46h46M12 48V10M12 42C16 21 19 15 23 29s7 13 11 2 7-6 10-3 5 2 9-1"/><path d="M12 42c8-5 13-9 20-12s13-5 21-6" stroke-dasharray="3 4"/>',
    'mechanics': '<path d="m10 40 30 9 14-23-30-9Z M10 40l14-23M20 43l14-23M30 46l14-23M15 32l30 9M20 25l30 9"/><path d="M28 8v11m-4-4 4 4 4-4M41 10v13m-4-4 4 4 4-4"/>'
}


def esc(value):
    return html.escape(str(value), quote=True)


def route(page, lang='en'):
    if page == 'not-found':
        return '404.html'
    return 'index.html' if page == 'home' else page + '.html'


def bibtex(item):
    key = 'deepmathlab-' + re.sub(r'[^A-Za-z0-9]+', '-', item['doi'])
    fields = {'title': item['title'], 'author': item['authors'].replace(', ', ' and '),
              'journal': item['journal'], 'year': str(item['year']), 'doi': item['doi']}
    return '@article{' + key + ',\n' + ',\n'.join('  ' + k + ' = {' + v + '}' for k, v in fields.items()) + '\n}'


def render(page='home', page_path=None):
    lang = 'en'
    def t(value):
        raw = value.get(lang, value.get('en', '')) if isinstance(value, dict) else value
        return esc(raw).replace('\n', '<br>\n').replace('&lt;br&gt;', '<br>\n').replace('&lt;span&gt;', '<span>').replace('&lt;/span&gt;', '</span>')

    def c(key):
        return t(DATA['copy'][key])

    def r(key):
        return './' + route(key, lang)

    def link(label, url, cls='text-link', download=False, new_tab=False):
        external = ' target="_blank" rel="noopener noreferrer"' if url.startswith('https:') or new_tab else ''
        download_attr = ' download' if download else ''
        glyph = '↓' if download else '↑' if url == '#top' else '↗' if external else '→'
        kind = 'external' if external else 'internal'
        return f'<a class="{cls}" data-link-kind="{kind}" href="{esc(url)}"{external}{download_attr}>{label}<span aria-hidden="true">{glyph}</span></a>'

    def group_summary():
        return f'<div class="group-summary"><p class="eyebrow">KENTECH / ENERGY ENGINEERING</p><h3>{c("group_panel_title")}</h3><dl class="group-facts"><div><dt>{c("location_label")}</dt><dd>{c("group_panel_location")}</dd></div><div><dt>{t(DATA["nav"]["research"])}</dt><dd>{c("group_panel_research")}</dd></div></dl>{link(c("all_people"), r("people"))}</div>'

    def media(key, label):
        item = DATA.get('media', {}).get(key)
        if item and item.get('src'):
            return f'<figure class="media-slot media-slot--filled"><img src="{esc(item["src"])}" alt="{t(item.get("alt", label))}" loading="lazy"><figcaption>{t(item.get("caption", label))}</figcaption></figure>'
        return ''

    def source_figure(item, compact=False):
        figure = item.get('figure')
        if not figure:
            return ''
        cls = 'research-preview' if compact else 'research-figure'
        caption = t(figure['title'] if compact else figure['caption'])
        return f'''<figure class="{cls}"><div class="research-image"><img src="{esc(figure['src'])}" width="{int(figure['width'])}" height="{int(figure['height'])}" alt="{t(figure['alt'])}" loading="lazy" decoding="async"></div><figcaption><p>{caption}</p><span class="figure-source">{t(figure['source'])}</span>{link(c('view_figure'), figure['original'], 'figure-view', new_tab=True)}</figcaption></figure>'''

    def foundation_diagram():
        methods = ['Mathematical analysis', 'Learning methods', 'Simulation & modeling']
        method_list = ''.join(f'<li>{esc(method)}</li>' for method in methods)
        areas = ''.join(f'<li>{t(area)}</li>' for area in DATA['application_areas'])
        return f'''<figure class="foundation-map"><figcaption class="eyebrow">{c('foundation_label')}</figcaption><div class="foundation-core"><h3>{c('foundation_title')}</h3><ul class="foundation-methods" aria-label="Common methods">{method_list}</ul></div><div class="foundation-branches" aria-hidden="true"></div><ul class="foundation-areas" aria-label="Research connections">{areas}</ul></figure>'''

    def papers(items, citations=False, heading_level=3):
        result = []
        heading = 'h' + str(heading_level)
        for item in items:
            cite = f'<details class="bibtex-entry"><summary>BibTeX</summary><div class="citation-tools"><button class="copy-citation" type="button" data-label-copy="{c("copy_citation")}" data-label-copied="{c("copied_citation")}" data-label-failed="{c("copy_failed")}" hidden>{c("copy_citation")}</button><span class="copy-status" role="status" aria-live="polite"></span></div><pre tabindex="0"><code>{esc(bibtex(item))}</code></pre></details>' if citations else ''
            search = esc(' '.join([item['title'], item['authors'], item['journal'], item['doi']]).lower())
            result.append(f'''<article class="publication" data-year="{item['year']}" data-topic="{esc(item.get('category', 'other'))}" data-search="{search}">
              <span class="pub-year">{item['year']}</span><div class="pub-body"><span class="pub-type">{t(item['topic'])}</span>
              <{heading}><a href="https://doi.org/{esc(item['doi'])}" target="_blank" rel="noopener noreferrer">{esc(item['title'])}<span class="pub-arrow" aria-hidden="true">↗</span></a></{heading}>
              <p class="pub-authors">{esc(item['authors'])}</p><p class="pub-journal"><span>{esc(item['journal'])}</span> · {esc(item['detail'])}</p>
              <a class="pub-doi" href="https://doi.org/{esc(item['doi'])}" target="_blank" rel="noopener noreferrer">DOI: {esc(item['doi'])}<span aria-hidden="true">↗</span></a>{cite}</div></article>''')
        return ''.join(result)

    def profiles(items):
        rows = []
        for person in items:
            photo = person.get('photo')
            dimensions = f' width="{int(person["photo_width"])}" height="{int(person["photo_height"])}"' if photo and person.get('photo_width') and person.get('photo_height') else ''
            visual = f'<img src="{esc(photo)}"{dimensions} alt="{t(person["name"])}" loading="lazy" decoding="async">' if photo else esc(person['initials'])
            portrait_class = 'portrait-slot portrait-slot--photo' if photo else 'portrait-slot'
            if photo and person.get('photo_fit') == 'contain':
                portrait_class += ' portrait-slot--contain'
            profile_link = link(t(person.get('url_label', DATA['copy']['member_website_label'])), person['url']) if person.get('url') else ''
            interests = person.get('research_interests', [])
            research = f'<div class="profile-interests"><h4>{c("member_research_label")}</h4><ul>{"".join(f"<li>{t(interest)}</li>" for interest in interests)}</ul></div>' if interests else ''
            email = f'<a class="profile-email" href="mailto:{esc(person["email"])}">{esc(person["email"])}</a>' if person.get('email') else ''
            rows.append(f'''<article class="profile-card"><div class="{portrait_class}">{visual}</div><div class="profile-copy"><h3>{t(person['name'])}</h3><p class="profile-role">{t(person['role'])}</p><p class="profile-affiliation">{t(person['detail'])}</p>{research}<div class="profile-links">{email}{profile_link}</div></div></article>''')
        return ''.join(rows)

    def page_hero(title, intro):
        label = DATA['nav'].get(page, {'en': page, 'ko': page})
        return f'<section class="page-hero container"><p class="eyebrow">DEEP-MATH / {t(label)}</p><h1>{title}</h1><p class="page-intro">{intro}</p></section>'

    research_cards = ''.join(f'''<article class="research-item" id="research-{esc(item['id'])}">
      <div class="research-card-top"><span class="item-number">{esc(item['number'])} / RESEARCH</span></div>
      <div class="research-titles"><h3 class="research-title"><a href="{r('research')}#{esc(item['id'])}">{t(item['title'])}</a></h3></div>
      <div class="research-detail"><p>{t(item['description'])}</p><div class="tags">{''.join(f'<span>{esc(tag)}</span>' for tag in item['tags'])}</div></div>{source_figure(item, compact=True)}</article>''' for item in DATA['research_axes'])
    pi = f'''<article class="pi-profile" id="hyunju-kim"><figure class="pi-portrait"><img src="./hyunju-kim-portrait.webp" width="640" height="800" alt="{c('pi_name')}" loading="lazy" decoding="async"><figcaption>KENTECH · HYUNJU KIM</figcaption></figure>
      <div class="pi-text"><p class="eyebrow">{c('pi_label')}</p><h3>{c('pi_name')}</h3><p class="pi-role">{c('pi_role')}</p><p class="pi-department">{c('pi_department')}</p><p class="pi-description">{c('pi_description')}</p><p class="pi-education"><span>{c('education_label')}</span>{c('pi_education')}</p>{link(c('profile_link'), DATA['academic_url'])}</div></article>'''
    join_cards = ''.join(f'<article class="join-card"><p class="eyebrow">0{i+1}</p><h2>{t(item["title"])}</h2><p>{t(item["description"])}</p></article>' for i, item in enumerate(DATA['join_paths']))
    title = 'DEEP-MATH Lab | Mathematics for AI and Energy | KENTECH'
    if page != 'home':
        title = f'{t(DATA["nav"].get(page, page))} | DEEP-MATH Lab | KENTECH'
    description = DATA['site_description'] if page == 'home' else DATA['copy'].get('page_' + page + '_intro', DATA['copy'].get(page + '_intro', DATA['site_description']))
    canonical = PUBLIC_ORIGIN + ('' if page == 'home' else route(page, lang))
    share_url = PUBLIC_ORIGIN + (page_path if page_path is not None else ('' if page == 'home' else route(page, lang)))
    if page == 'home':
        featured = [DATA['publications'][0]] + [item for item in DATA['publications'] if item['year'] in (2018, 2013)]
        news = ''
        if DATA.get('news'):
            news = f'<section class="section container"><div class="section-head"><h2>{c("news_title")}</h2>{link(c("news_title"), r("news"))}</div>' + ''.join(f'<article class="content-callout"><p class="eyebrow">{esc(item["date"])}</p><h3>{t(item["title"])}</h3><p>{t(item["summary"])}</p></article>' for item in DATA['news'][:3]) + '</section>'
        content = f'''<section class="hero container" aria-labelledby="hero-title"><div class="hero-copy"><div class="hero-eyebrow"><span class="eyebrow">DEEP-MATH / KENTECH</span></div>
          <h1 id="hero-title">{c('hero_title')}</h1><p class="hero-subtitle">{c('hero_subtitle')}</p><p class="hero-intro">{c('hero_intro')}</p>
          <p class="hero-affiliation">{c('hero_affiliation')} <a href="{r('people')}#hyunju-kim">{c('pi_name')}</a> · {c('hero_department')}</p><div class="hero-buttons">{link(c('hero_cta'), r('research'), 'button-primary')}{link(c('hero_secondary'), r('publications'), 'button-primary button-secondary')}</div></div>
          <div class="hero-strip"><span class="strip-label">RESEARCH CONNECTIONS</span><span>{c('hero_strip')}</span><span class="strip-arrow" aria-hidden="true">↘</span></div></section>
          <section class="section research-section" id="research"><div class="container"><div class="section-head"><div><p class="eyebrow section-number">01 / {t(DATA['nav']['research'])}</p><h2>{c('research_heading')}</h2></div><div class="research-overview"><p class="section-intro">{c('research_intro')}</p>{link(c('all_research'), r('research'), 'text-link section-link')}</div></div><div class="research-list">{research_cards}</div></div></section>
          <section class="section overview-section container" id="people"><div class="lab-overview"><div class="overview-copy"><p class="eyebrow section-number">02 / {t(DATA['nav']['people'])}</p><h2>{c('about_heading')}</h2><p>{c('about_intro')}</p><p class="lab-name-note">{c('about_detail')}</p>{link(c('all_people'), r('people'))}</div>{foundation_diagram()}</div></section>
          <section class="section publications-section" id="publications"><div class="container"><div class="section-head"><div><p class="eyebrow section-number">03 / {t(DATA['nav']['publications'])}</p><h2>{c('publications_heading')}</h2></div>{link(c('all_publications'), r('publications'))}</div><p class="publications-intro">{c('publications_intro')}</p><div id="publication-list">{papers(featured)}</div></div></section>
          {news}<section class="contact-section" id="contact"><div class="container contact-layout"><div class="contact-copy"><p class="eyebrow section-number">04 / {t(DATA['nav']['join'])}</p><h2>{c('join_heading')}</h2><p>{c('join_home_intro')}</p>{link(c('join_link'), r('join'), 'button-primary')}</div><div class="contact-location"><p class="eyebrow">{c('location_label')}</p><p>{c('location')}</p>{link(c('page_contact_title'), r('contact'))}</div></div></section>'''
    elif page == 'research':
        foundations = []
        for item in DATA['research']:
            related = [pub for pub in DATA['publications'] if pub['doi'] in item['related_dois']]
            foundations.append(f'''<details class="research-foundation" id="{esc(item['id'])}"><summary><h3>{t(item['title'])}<span class="foundation-toggle" aria-hidden="true"></span></h3></summary><div class="foundation-content"><p>{t(item['description'])}</p><dl class="research-meta"><div><dt>{c('methods_label')}</dt><dd>{' / '.join(esc(x) for x in item['tags'])}</dd></div><div><dt>{c('problems_label')}</dt><dd>{t(item['scope'])}</dd></div></dl>{media(item['id'], t(item['title']) + ' / ' + c('research_visual'))}<h4>{c('related_papers')}</h4>{papers(related, heading_level=5)}</div></details>''')
        blocks = []
        for item in DATA['research_axes']:
            numerical = f'<div class="numerical-foundations"><p class="eyebrow">{c("numerical_foundations_heading")}</p>{"".join(foundations)}</div>' if item['id'] == 'simulation-modeling' else ''
            focus = ''.join(f'<li>{esc(part.strip().rstrip("."))}</li>' for part in item['scope'].split(';'))
            methods = ''.join(f'<li>{esc(tag)}</li>' for tag in item['tags'])
            blocks.append(f'''<article class="research-detail-block" id="{esc(item['id'])}"><p class="eyebrow">{esc(item['number'])} / RESEARCH</p><h2>{t(item['title'])}</h2><p class="research-description">{t(item['description'])}</p><dl class="axis-summary"><div><dt>{c('research_focus_label')}</dt><dd><ul>{focus}</ul></dd></div><div><dt>{c('research_method_label')}</dt><dd><ul>{methods}</ul></dd></div></dl>{source_figure(item)}{numerical}</article>''')
        index = ''.join(f'<a href="#{esc(item["id"])}">{esc(item["number"])} / {t(item["title"])}</a>' for item in DATA['research_axes'])
        connections = f'<section class="research-connections" id="research-connections"><h2>{c("research_connections_title")}</h2>{foundation_diagram()}<p>{c("foundation_intro")}</p></section>'
        content = page_hero(c('page_research_title'), c('page_research_intro')) + f'<section class="page-content container">{connections}<div class="content-layout"><div class="content-main">{"".join(blocks)}</div><aside class="content-aside"><nav class="section-nav" aria-label="Research themes">{index}</nav><div class="content-callout"><p>{c("research_context")}</p>{link(c("research_source"), DATA["research_url"])}</div></aside></div></section>'
    elif page == 'people':
        alumni = f'<h2>{c("alumni_heading")}</h2><div class="people-grid">{profiles(DATA["alumni"])}</div>' if DATA.get('alumni') else ''
        group_image = media('group', c('group_photo'))
        group_image = f'<div class="group-image">{group_image}</div>' if group_image else ''
        members_note = f'<p class="members-note">{c("members_note")}</p>' if DATA['copy'].get('members_note') else ''
        content = page_hero(c('page_people_title'), c('page_people_intro')) + f'<section class="page-content container"><h2 class="eyebrow section-number">{c("faculty_label")}</h2>{pi}<div class="members-heading" id="researchers"><h2>{c("current_members")}</h2></div><div class="people-grid">{profiles(DATA["members"])}</div>{members_note}{alumni}{group_image}</section>'
    elif page == 'publications':
        options = ''.join(f'<option value="{year}">{year}</option>' for year in sorted({x['year'] for x in DATA['publications']}, reverse=True))
        topic_buttons = ''.join(f'<button type="button" class="filter-chip" data-topic-filter="{topic}" aria-pressed="{str(topic == "all").lower()}">{c(key)}</button>' for topic, key in [('all', 'all_topics'), ('fractional', 'topic_fractional'), ('geometry', 'topic_geometry'), ('singular', 'topic_singular')])
        content = page_hero(c('page_publications_title'), c('page_publications_intro')) + f'''<section class="page-content container"><div class="bibliography-links">{link(c('publications_source'), DATA['publications_url'])}{link(c('bibtex_download'), './publications.bib', download=True)}</div><div class="publication-filters" role="group" aria-label="{'Publication topics' if lang == 'en' else '논문 주제'}" hidden>{topic_buttons}</div><div class="publication-tools" hidden><label class="search-box"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="6.5"/><path d="m15 15 5 5"/></svg><span class="sr-only">{c('search_label')}</span><input id="publication-search" type="search" placeholder="{c('search_placeholder')}" autocomplete="off"></label><label class="year-filter"><span class="sr-only">{c('filter_year_label')}</span><select id="publication-year"><option value="all">{c('filter_all_years')}</option>{options}</select></label></div><div class="publication-summary"><span id="result-status" role="status" aria-live="polite"></span><button type="button" class="search-clear" hidden>{c('reset_filters')}</button></div><noscript><p>{'All selected papers are shown below.' if lang == 'en' else '주요 논문을 아래에서 확인할 수 있습니다.'}</p></noscript><div id="publication-list">{papers(DATA['publications'], True, heading_level=2)}</div><p class="no-results" hidden>{c('no_results')}</p></section>'''
    elif page == 'join':
        fields = ''.join(f'<li>{t(x)}</li>' for x in DATA['enquiry_fields'])
        content = page_hero(c('page_join_title'), c('page_join_intro')) + f'<section class="page-content container"><div class="join-grid">{join_cards}</div><div class="content-layout join-details"><div class="content-main"><h2>{c("join_prepare")}</h2><ul class="enquiry-list">{fields}</ul>{link(c("join_email_cta"), "mailto:" + DATA["email"], "button-primary")}</div><aside class="content-aside join-note"><p>{c("join_status")}</p>{link(c("university_info"), DATA["institution_url"])}</aside></div></section>'
    elif page == 'contact':
        content = page_hero(c('page_contact_title'), c('page_contact_intro')) + f'<section class="page-content container"><div class="content-layout"><div class="content-main"><dl class="contact-details"><div><dt>{c("email_label")}</dt><dd><a href="mailto:{esc(DATA["email"])}">{esc(DATA["email"])}</a></dd></div><div><dt>{c("campus_label")}</dt><dd>{c("campus_address")}</dd></div><div><dt>{c("pi_label")}</dt><dd>{link(c("pi_name"), DATA["profile_url"])}</dd></div></dl></div><aside class="content-aside"><div class="content-callout"><h2>{c("location_label")}</h2><p>{c("visit_note")}</p>{link(c("institution_link"), DATA["institution_url"])}</div></aside></div></section>'
    elif page == 'not-found':
        title = 'Page not found | DEEP-MATH Lab'
        description = 'Find research, people, publications and contact information at DEEP-MATH Lab.'
        content = f'<section class="page-hero container"><p class="eyebrow">DEEP-MATH / 404</p><h1>Page not found.</h1><p class="page-intro">This address is unavailable. Explore the lab using the navigation above, or return to the homepage.</p><div class="hero-buttons">{link("Back to the lab", r("home"), "button-primary")}{link("Browse research", r("research"), "text-link")}</div></section>'
    else:
        entries = DATA[page]
        cards = ''.join(f'<article class="content-callout"><p class="eyebrow">{esc(item.get("date", item.get("type", "")))}</p><h2>{t(item["title"])}</h2><p>{t(item.get("summary", item.get("description", "")))}</p>{link(t(item["title"]), item["url"]) if item.get("url") else ""}</article>' for item in entries)
        content = page_hero(c(page + '_title'), c(page + '_intro')) + f'<section class="page-content container">{cards}</section>'

    nav_items = dict(DATA['nav'])
    for key in ['resources', 'news']:
        if key in PAGES:
            nav_items[key] = {'en': key.title(), 'ko': '자료' if key == 'resources' else '소식'}
    navigation = ''.join('<a href="{}"{}>{}</a>'.format(r(key), ' aria-current="page"' if key == page else '', t(label)) for key, label in nav_items.items())
    creator_credit = f'<p class="creator-credit">{c("creator_credit")}</p>'
    footer_links = ''.join(f'<a href="{r(key)}">{t(label)}</a>' for key, label in nav_items.items())
    return f'''<!doctype html>
<html lang="{lang}"><head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  {'<base href="/">' if page == 'not-found' else ''}
  <meta name="color-scheme" content="light"><meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{title}</title><meta name="description" content="{esc(description)}">
  <meta name="theme-color" content="#ffffff"><meta name="robots" content="{'noindex,follow' if page == 'not-found' else 'noindex,nofollow' if DATA['preview'] else 'index,follow'}">
  <link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:site_name" content="{t(DATA['brand'])}">
  <meta property="og:title" content="{title}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{share_url}">
  <meta property="og:locale" content="{'ko_KR' if lang == 'ko' else 'en_US'}"><meta property="og:image" content="{SHARE_IMAGE}"><meta property="og:image:secure_url" content="{SHARE_IMAGE}">
  <meta property="og:image:type" content="image/png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="DEEP-MATH Lab — Mathematical foundations for AI and energy at KENTECH">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{SHARE_IMAGE}"><link rel="image_src" href="{SHARE_IMAGE}">
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="{esc(FONT_STYLESHEET)}">
  <link rel="icon" href="./favicon.svg?v={ASSET_VERSION}" type="image/svg+xml"><link rel="stylesheet" href="./styles.css?v={ASSET_VERSION}">
  <script src="./app.js?v={ASSET_VERSION}" defer></script>
</head><body class="lang-{lang} page-{page}" id="top">
  <a class="skip-link" href="#main">{c('skip')}</a><header class="site-header"><div class="container header-inner"><a class="wordmark" href="{r('home')}" aria-label="DEEP-MATH Lab home">
    <svg class="logo" viewBox="0 0 40 40" aria-hidden="true"><rect x="1" y="1" width="38" height="38" rx="6" fill="#365BFF"/><path d="M11 29V11h7a8 8 0 0 1 0 18h-7m12-18v18m-7-18v18" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round"/></svg><span><strong>{t(DATA['brand'])}</strong><small>{t(DATA['brand_sub'])}</small></span></a>
    <div class="header-actions"><nav id="navigation" aria-label="{'Primary navigation' if lang == 'en' else '주 메뉴'}">{navigation}</nav><button class="menu-toggle" aria-label="{c('menu')}" aria-expanded="false" aria-controls="navigation"><span></span><span></span></button></div></div></header>
  <main id="main" tabindex="-1">{content}</main><footer class="site-footer"><div class="container"><div class="footer-top"><div><strong>{t(DATA['brand'])}</strong><span>{c('footer_tagline')}</span></div>{link(c('back_top'), '#top')}</div><nav class="footer-navigation" aria-label="{c('footer_navigation')}">{footer_links}<a href="mailto:{esc(DATA['email'])}">{esc(DATA['email'])}</a></nav><div class="footer-bottom"><span>© 2026 · {t(DATA['brand'])} · KENTECH</span>{creator_credit}</div></div></footer>
</body></html>'''


built = []
for key in PAGES:
    name = route(key)
    (ROOT / name).write_text(render(key), encoding='utf-8')
    built.append(name)
(ROOT / 'home.html').write_text(render('home', 'home.html'), encoding='utf-8')
(ROOT / 'publications.bib').write_text('\n\n'.join(bibtex(x) for x in DATA['publications']) + '\n', encoding='utf-8')
indexable = [key for key in PAGES if key != 'not-found']
sitemap_urls = [PUBLIC_ORIGIN + ('' if key == 'home' else route(key)) for key in indexable]
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{esc(url)}</loc><lastmod>{esc(DATA["updated_on"])}</lastmod></url>\n' for url in sitemap_urls) + '</urlset>\n', encoding='utf-8')
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + PUBLIC_ORIGIN + 'sitemap.xml\n', encoding='utf-8')
print('Built', ', '.join(built), ', home.html, publications.bib, sitemap.xml and robots.txt')
