# DeepMathLab

English-only static website for Hyunju Kim's computational mathematics research group at KENTECH. The public origin is [deepmathlab.github.io](https://deepmathlab.github.io/). DeepMathLab is the working name supplied by the user; its official spelling and final content still need review.

## Build and pages

Edit `site.json` for English copy, people, research themes, publications and optional material. Run from the repository root:

```sh
python3 build.py
python3 -m http.server 4174 --bind 127.0.0.1
```

The current build produces eight HTML files:

| File | Purpose |
| --- | --- |
| `index.html` | Main overview; canonical is the public root URL |
| `research.html` | Research themes and related papers |
| `people.html` | Faculty and the currently supplied group directory |
| `publications.html` | Selected papers, filters and citations |
| `join.html` | Research and visitor enquiries |
| `contact.html` | Contact and campus information |
| `404.html` | Not-found page; root-relative base keeps links working from nested missing URLs |
| `home.html` | Non-redirecting sharing alias with its own matching canonical and `og:url` |

There are no Korean counterparts or language-switch controls. `publications.bib` contains the selected bibliography. Generated HTML, data, styles and assets are served from the repository root; the output is compatible with GitHub Pages and includes `.nojekyll`. Rebuild after content changes rather than editing generated HTML independently.

## Implemented behaviour

- **Theme:** the first visit follows the operating-system light/dark preference unless a choice is saved in `localStorage`. The toggle persists that choice when storage is available, updates its accessible state and swaps its icon. Storage failure does not prevent use.
- **Geometry:** the inline conceptual SVG has Surface, Mesh and Domain views. Controls update selected state, image description and status text. Fine-pointer hover adds a small tilt; touch and reduced-motion users do not receive it. Reduced motion disables nonessential transitions and smooth scrolling. Without JavaScript, the labelled SVG remains visible and controls stay hidden.
- **Navigation:** opening the mobile menu focuses its first link. Escape closes it and returns focus to the toggle; outside pointer actions and navigation close it. Collapse is enabled only after handlers bind, so navigation remains visible when JavaScript is unavailable.
- **Publication filters:** topic, year and text search combine. Search matches words in titles, authors, journals and DOIs. `q`, `year` and `topic` are read from and reflected in the URL without adding a history entry for each keystroke; invalid year/topic values fall back to All. Result counts, zero results and Reset filters are provided. Without JavaScript, all selected papers remain readable.
- **Citations:** expand/copy individual BibTeX entries or download the complete bibliography. Success is shown only after the clipboard promise succeeds. Failed or unavailable clipboard access selects the citation for manual copying and shows a failure message. Buttons are disabled while a request is pending.
- **Content and assets:** missing research/group media are omitted rather than rendered as large empty frames. The home overview uses known group information when its photograph is absent. Profiles without portraits use initials. The faculty page uses the verified KENTECH portrait.
- **Delivery:** shared static CSS/JS, inline SVG, lazy-loaded secondary images, font preconnects and `display=swap` support a small static implementation. Transfer sizes, font behaviour and loading performance require browser measurement.

## Figma guide crosswalk and verification

These official guides inform the design for researchers, prospective students and collaborators. Their trend suggestions do not prescribe one colour or require every fashionable interaction. The following are verification criteria, not a claim that browser/device testing has passed.

| Official guide | Verification criterion |
| --- | --- |
| [2026 Web Design Trends](https://www.figma.com/resource-library/web-design-trends/) | The first view communicates the group's subject and gives clear research/publication paths. Large type, contrast and geometric depth support that purpose; motion preserves reading and loading performance. |
| [Typography in Design](https://www.figma.com/resource-library/typography-in-design/) | Use consistent heading/body/metadata roles. Inspect long titles and paragraph widths; Figma suggests roughly 40–60 characters for English body text and more leading for longer lines. Do not apply heading line-height mechanically to paragraphs. |
| [Web Design Grid Layout Examples](https://www.figma.com/resource-library/web-design-grid-layout-examples/) | Check common content edges, spacing and gutters across overview/detail pages. Repeated components follow shared spacing; layouts adapt rather than forcing a rigid print grid. |
| [Responsive Website Design](https://www.figma.com/resource-library/responsive-website-design/) | Test 320, 390, 768 and 1280px widths and 200% zoom: no clipped content, unusable navigation or page-wide overflow. Check long DOI/email strings, SVG and scrollable BibTeX. These viewport choices are project checks. |
| [Website Structure](https://www.figma.com/resource-library/website-structure/) | Verify concise navigation, current-page markers, research-to-paper links and paths to people/contact. Check internal links and not-found recovery. |
| [Color Contrast Checker](https://www.figma.com/color-contrast-checker/) | Measure actual colours in both themes, including metadata, controls, selected/hover/focus states and hero captions. The guide gives AA thresholds of 4.5:1 for normal text and 3:1 for large text; contrast alone does not establish full accessibility. |
| [Button States](https://www.figma.com/resource-library/button-states/) | Check default/hover/active/focus/disabled states with keyboard and touch. Preserve focus visibility and truthful copy feedback; verify counts, zero results and reset. The guide's 44×44px mobile target and 100–200ms transition advice are design recommendations. |
| [Mobile-first Design](https://www.figma.com/resource-library/mobile-first-design/) | Test actual small-screen devices and constrained connectivity. Measure initial requests, font/image transfer and common-asset caching before/after added effects. Minimize unnecessary assets and third-party scripts. |

Also verify reduced motion, JavaScript-disabled navigation/content, blocked clipboard access and unavailable preference storage. The drawing is a conceptual illustration, not experimental or computational validation. Record actual browser/device results separately from source checks.

## Content to provide

| Priority | Material | Fields to include |
| --- | --- | --- |
| 1 | Group identity | Approved English name/short name, introduction and final research themes |
| 1 | Current people | English name, actual role/institution, research interests and public profile; portrait optional |
| 1 | Research projects | Title, question, methods, dates, active/completed status, participants, related papers, public code/data and confirmed collaborators |
| 1 | Publications | Exact title, author order, venue, year and DOI; public PDF/code/project links when available |
| 1 | Join and visits | Current enquiry/open-position policy, study/visitor categories, contact and actual application procedure |
| 1 | Location | Building/room and directions; the campus address is not a verified lab office |
| 2 | Research outputs | Public software, datasets, documentation and licenses; add to `resources` |
| 2 | News and alumni | Dated news; alumni names, tenure, later affiliation and public profiles |
| 3 | Images | Group photograph, better-resolution faculty/people portraits, research figures with captions and source/date |

Suggested image sizes are 1600px wide for a group photograph, 600px on the short side for portraits and 1200px wide for a research figure. These are practical asset suggestions, not mandatory guide thresholds. Missing images need not block verified text.

`media.group`, `media.geometry`, `media.fractional` and `media.mechanics` are currently null and omitted. Supply English strings to fill a slot, for example:

```json
{"src":"./group-photo.jpg","alt":"Group photograph at KENTECH","caption":"Group photograph, October 2026"}
```

Members may have `photo` and `url`; alumni use the same profile fields. Empty `alumni`, `resources` and `news` collections are not shown. Resources use `type`, `title`, `description`, `url`; news uses `date`, `title`, `summary`, `url`. Adding real entries enables their English pages and navigation, so the eight-file count increases. Do not add fictional projects, announcements, openings, staff or counts to fill space.

## Source and reference boundaries

Research wording and faculty background follow [KENTECH Introduction](https://kentech.ac.kr/submenu.do?menuurl=JPQbgLY0JlNRZPvKXFeixQ%3D%3D&siteName=hjkim), [Academics](https://kentech.ac.kr/submenu.do?menuurl=yar34NkQy16gucKYFAFqrw%3D%3D&siteName=hjkim) and the [official publication list](https://kentech.ac.kr/submenu.do?menuurl=EmPii7OvsAgMn8WvyAXCLg%3D%3D&siteName=hjkim). Selected-paper metadata was checked against publisher/Crossref records. The portrait is from the [official KENTECH faculty directory](https://admission.kentech.ac.kr/ourFaculty.do), whose image labels identify Hyunju Kim. These records do not establish the current status of unlisted projects or latest lab achievements.

The contact email and working DeepMathLab name come from the user. The known roster is incomplete. `preview: true` keeps generated pages `noindex,nofollow`; set it to false when content is ready for public indexing.

International benchmarks informed information architecture, not research claims or group scale:

- [Berkeley BAIR](https://bair.berkeley.edu/about.html): multi-faculty research community; people/alumni, software, admissions and blog paths.
- [MIT Langer Lab](https://langerlab.mit.edu/): faculty-led lab; research overview, yearly bibliography, news and differentiated contacts.
- [ETH Autonomous Systems Lab](https://asl.ethz.ch/): running/completed projects, people/alumni, software/datasets and visit directions.
- [Cambridge Machine Learning Group](https://mlg.eng.cam.ac.uk/): research themes linked to papers, role-based people/former members and degree enquiries.
- [MPI Perceiving Systems](https://is.mpg.de/ps): research department; projects, publications, code/data and visitors/alumni.

Reference-site wording, logos, template code and staff records are not copied. The white/charcoal/blue system, conceptual geometry and monogram are site assets; the faculty photograph is separately sourced as above.

## Sharing

`share-card.svg` is the editable artwork; `share-card.png` is its 1200×630 export. Pages use it for Open Graph and Twitter previews. Update `ASSET_VERSION` in `build.py` after presentation/share-art changes. Kakao may retain previous previews; `home.html` provides a separate sharing URL. Its `og:url` matches its address because [Kakao may scrape the `og:url` destination](https://devtalk.kakao.com/t/og-url/136380). Deployment alone does not verify a changed Kakao preview.
