# DeepMathLab

English-first computational mathematics research group website at KENTECH, led by Hyunju Kim. Published at https://deepmathlab.github.io/ with a Korean counterpart.

## Build and pages

Edit `site.json` for bilingual content, people, research themes, and publications. Run:

```sh
python3 build.py
python3 -m http.server 4174 --bind 127.0.0.1
```

The root English overview is `index.html`; the Korean overview is `ko.html`. Detail pages are `research.html`, `people.html`, `publications.html`, `join.html`, and `contact.html`, each with a `-ko.html` counterpart. `home.html` is a non-redirecting sharing alias with a matching canonical and `og:url`. `publications.bib` contains the selected bibliography. All generated pages, data, styles, and assets are served from the repository root; GitHub Pages publishes `main` with `.nojekyll`.

The shared navigation links to real pages. Publication search/year filtering runs only where its controls exist. BibTeX records contain verified title, author order, journal, year, and DOI; optional issue/page fields are not guessed.

## Content to provide

| Priority | Material | Fields to include |
| --- | --- | --- |
| 1 | Group identity | Approved English name/short name, one-paragraph introduction, final research themes |
| 1 | Current people | English/Korean name, role, institution, research interests, public profile link; portrait optional |
| 1 | Research projects | Title, research question, methods, start/end dates, active/completed status, participants, related papers, public code/data, collaborator names |
| 1 | Publications | Updated list with exact title, author order, venue, year, DOI; public PDF/code/project links when available |
| 1 | Join and visits | Whether enquiries/open positions are welcome, available study/visitor categories, contact and actual application procedure |
| 1 | Location | Building/room and visitor directions; the current address is the KENTECH campus, not a verified lab office |
| 2 | Research outputs | Public software, datasets, documentation and licenses; add to `resources` |
| 2 | News and alumni | Dated news; alumni names, tenure, later affiliation and public profile links |
| 3 | Images | Group photograph, high-resolution faculty/people portraits, research figures and captions |

Suggested images: group photograph at least 1600px wide (3:2 or 16:9); portraits at least 600px on the short side; one research figure per theme at least 1200px wide. Include a meaningful caption and the image's source/date. Images can remain empty while content is collected.

`media.group`, `media.geometry`, `media.fractional`, and `media.mechanics` are currently null and render honest empty image slots. To fill one, supply an object such as:

```json
{"src":"./group-photo.jpg","alt":{"en":"Group photograph at KENTECH","ko":"KENTECH 연구실 단체 사진"},"caption":{"en":"Group photograph","ko":"연구실 단체 사진"}}
```

Members may have `photo` (local image path) and `url` (public profile). Alumni use the same profile fields. Empty `alumni`, `resources`, and `news` collections are not shown. Adding `resources` entries (`type`, bilingual `title`/`description`, `url`) or `news` entries (`date`, bilingual `title`/`summary`, `url`) generates their English/Korean pages and activates their navigation links. Do not add fictional projects, publications, announcements, openings, or membership counts to fill space.

## Source and reference boundaries

Research wording and faculty background follow [KENTECH Introduction](https://kentech.ac.kr/submenu.do?menuurl=JPQbgLY0JlNRZPvKXFeixQ%3D%3D&siteName=hjkim), [Academics](https://kentech.ac.kr/submenu.do?menuurl=yar34NkQy16gucKYFAFqrw%3D%3D&siteName=hjkim), and the [official publication list](https://kentech.ac.kr/submenu.do?menuurl=EmPii7OvsAgMn8WvyAXCLg%3D%3D&siteName=hjkim). Selected paper metadata was checked against publisher/Crossref records. The supplied contact email and working DeepMathLab name come from the user. The current known roster is incomplete. This draft remains `noindex` until approved for indexing.

International benchmarks informed structure, not research claims or group scale:

- [Berkeley BAIR](https://bair.berkeley.edu/about.html): multi-faculty research community; research, people/alumni, software, admissions and blog paths.
- [MIT Langer Lab](https://langerlab.mit.edu/): faculty-led lab; research overview, yearly bibliography, news and differentiated contacts.
- [ETH Autonomous Systems Lab](https://asl.ethz.ch/): research projects with running/completed states; people/alumni, software/datasets and visits.
- [Cambridge Machine Learning Group](https://mlg.eng.cam.ac.uk/): research themes linked to papers; role-based people, former members and degree enquiries.
- [MPI Perceiving Systems](https://is.mpg.de/ps): research department; projects, publications, code/data and visitors/alumni.

No reference-site text, images, logos, code, achievements, or staff records are copied. The illustration is a conceptual geometry drawing, not a simulation result. The teal/sage/graphite atlas design and monogram are DeepMathLab's own website assets.

## Sharing

`share-card.svg` is the editable artwork; `share-card.png` is its 1200×630 export. All pages explicitly choose it as the Open Graph/Twitter image. Update `ASSET_VERSION` in `build.py` after presentation or share-art changes. Kakao may keep previous URL previews; `home.html` gives a separate sharing URL. Its `og:url` must match its actual address because [Kakao may scrape the `og:url` destination](https://devtalk.kakao.com/t/og-url/136380).
