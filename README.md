# DEEP-MATH Lab

English-only static website for DEEP-MATH Lab, led by Hyunju Kim at KENTECH. The public origin is [deepmathlab.github.io](https://deepmathlab.github.io/). DEEP-MATH expands to Deep-learning Engineering and Explanatory Principles in Mathematics, following the professor's 2025 lab introduction.

## Build and pages

Edit `site.json` for English copy, people, research axes, numerical foundations, publications and optional material. Run from the repository root:

```sh
python3 build.py
python3 -m http.server 4174 --bind 127.0.0.1
```

The current build produces eight HTML files:

| File | Purpose |
| --- | --- |
| `index.html` | Main overview; canonical is the public root URL |
| `research.html` | Research axes, numerical foundations and related papers |
| `people.html` | Faculty and the currently supplied group directory |
| `publications.html` | Selected papers, filters and citations |
| `join.html` | Research and visitor enquiries |
| `contact.html` | Contact and campus information |
| `404.html` | Not-found page; root-relative base keeps links working from nested missing URLs |
| `home.html` | Non-redirecting sharing alias; canonical points to the public root, while `og:url` preserves the sharing address |

There are no Korean counterparts or language-switch controls. `publications.bib` contains the selected bibliography. Generated HTML, data, styles and assets are served from the repository root; the output is compatible with GitHub Pages and includes `.nojekyll`. Rebuild after content changes rather than editing generated HTML independently.

## Implemented behaviour

- **Appearance:** a fixed light palette is used. There is no theme toggle, stored-theme lookup or system dark-mode override.
- **Landing layout:** the introductory copy occupies the left column on desktop, with open whitespace on the right. No image, frame or placeholder copy is shown. Small screens use a single column without an empty image row.
- **Navigation:** opening the mobile menu focuses its first link. Escape closes it and returns focus to the toggle; outside pointer actions and navigation close it. Collapse is enabled only after handlers bind, so navigation remains visible when JavaScript is unavailable.
- **Publication filters:** topic, year and text search combine. Search matches words in titles, authors, journals and DOIs. `q`, `year` and `topic` are read from and reflected in the URL without adding a history entry for each keystroke; invalid year/topic values fall back to All. Result counts, zero results and Reset filters are provided. Without JavaScript, all selected papers remain readable.
- **Citations:** expand/copy individual BibTeX entries or download the complete bibliography. Success is shown only after the clipboard promise succeeds. Failed or unavailable clipboard access selects the citation for manual copying and shows a failure message. Buttons are disabled while a request is pending.
- **Content and assets:** missing research/group media are omitted rather than rendered as large empty frames. The home overview uses known group information when its photograph is absent. Profiles without portraits use initials. The faculty page uses the user-supplied photograph with its background removed, exported as a transparent 640×800 WebP over a neutral panel.
- **Delivery:** shared static CSS/JS, inline SVG, lazy-loaded secondary images, font preconnects and `display=swap` support a small static implementation. Transfer sizes, font behaviour and loading performance require browser measurement.

## Figma guide crosswalk and verification

These official guides inform the design for researchers, prospective students and collaborators. Their trend suggestions do not prescribe one colour or require every fashionable interaction. The following are verification criteria, not a claim that browser/device testing has passed.

| Official guide | Verification criterion |
| --- | --- |
| [2026 Web Design Trends](https://www.figma.com/resource-library/web-design-trends/) | The first view communicates the group's subject and gives clear research/publication paths. Large type, contrast and geometric structure support that purpose; motion preserves reading and loading performance. |
| [Typography in Design](https://www.figma.com/resource-library/typography-in-design/) | Use consistent heading/body/metadata roles. Inspect long titles and paragraph widths; Figma suggests roughly 40–60 characters for English body text and more leading for longer lines. Do not apply heading line-height mechanically to paragraphs. |
| [Web Design Grid Layout Examples](https://www.figma.com/resource-library/web-design-grid-layout-examples/) | Check common content edges, spacing and gutters across overview/detail pages. Repeated components follow shared spacing; layouts adapt rather than forcing a rigid print grid. |
| [Responsive Website Design](https://www.figma.com/resource-library/responsive-website-design/) | Test 320, 390, 768 and 1280px widths and 200% zoom: no clipped content, unusable navigation or page-wide overflow. Check long DOI/email strings, SVG and scrollable BibTeX. These viewport choices are project checks. |
| [Website Structure](https://www.figma.com/resource-library/website-structure/) | Verify concise navigation, current-page markers, research-to-paper links and paths to people/contact. Check internal links and not-found recovery. |
| [Color Contrast Checker](https://www.figma.com/color-contrast-checker/) | Measure actual colours in the light palette, including metadata, controls, selected/hover/focus states and hero captions. The guide gives AA thresholds of 4.5:1 for normal text and 3:1 for large text; contrast alone does not establish full accessibility. |
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

Members may have `photo`, intrinsic `photo_width`/`photo_height`, `research_interests`, public `email`, `url` and `url_label`; alumni use the same profile fields. Empty `alumni`, `resources` and `news` collections are not shown. Resources use `type`, `title`, `description`, `url`; news uses `date`, `title`, `summary`, `url`. Adding real entries enables their English pages and navigation, so the eight-file count increases. Do not add fictional projects, announcements, openings, staff or counts to fill space.

## Source and reference boundaries

Research wording and faculty background follow [KENTECH Introduction](https://kentech.ac.kr/submenu.do?menuurl=JPQbgLY0JlNRZPvKXFeixQ%3D%3D&siteName=hjkim), [Academics](https://kentech.ac.kr/submenu.do?menuurl=yar34NkQy16gucKYFAFqrw%3D%3D&siteName=hjkim) and the [official publication list](https://kentech.ac.kr/submenu.do?menuurl=EmPii7OvsAgMn8WvyAXCLg%3D%3D&siteName=hjkim). Selected-paper metadata was checked against publisher/Crossref records. The current portrait was supplied by the user on 8 October 2026 and edited with the built-in image-generation tool to remove the distracting background and adjacent person. These records do not establish the current status of unlisted projects or latest lab achievements.

The lab contact email comes from the user. The DEEP-MATH name and three research axes follow the professor-supplied 2025 introduction. The professor's latest website direction defines the lab as a mathematical foundation and research hub for AI, hydrogen, batteries, power grids and nuclear research. These fields describe its research role rather than a list of claimed experimental projects. `preview: false` enables indexing of public content. The 404 page remains `noindex,follow`. The creator credit is a small English line in the shared footer.

International benchmarks informed information architecture, not research claims or group scale:

- [Berkeley BAIR](https://bair.berkeley.edu/about.html): multi-faculty research community; people/alumni, software, admissions and blog paths.
- [MIT Langer Lab](https://langerlab.mit.edu/): faculty-led lab; research overview, yearly bibliography, news and differentiated contacts.
- [ETH Autonomous Systems Lab](https://asl.ethz.ch/): running/completed projects, people/alumni, software/datasets and visit directions.
- [Cambridge Machine Learning Group](https://mlg.eng.cam.ac.uk/): research themes linked to papers, role-based people/former members and degree enquiries.
- [MPI Perceiving Systems](https://is.mpg.de/ps): research department; projects, publications, code/data and visitors/alumni.

Reference-site wording, logos, template code and staff records are not copied. The white/charcoal/blue system and monogram are site assets; the faculty photograph is separately sourced as above.

## Sharing

`share-card.svg` is the editable artwork; `share-card.png` is its 1200×630 export. Pages use it for Open Graph and Twitter previews. Update `site_version` in `site.json` after presentation/share-art changes. Kakao may retain previous previews; `home.html` provides a separate sharing URL. Its `og:url` matches its address because [Kakao may scrape the `og:url` destination](https://devtalk.kakao.com/t/og-url/136380). Deployment alone does not verify a changed Kakao preview.


## Version control and indexing

The current release is **1.3.0**. The `site_version` value also supplies the asset cache version. Keep editable sources and generated pages together in Git; [CHANGELOG.md](CHANGELOG.md) records user-visible releases. Run `python3 build.py` before publishing changes.

The build generates `sitemap.xml` with the six canonical content pages and `robots.txt` with its public location. `home.html` is a sharing alias and canonicalizes to the root; it and the 404 page are omitted from the sitemap. `updated_on` supplies the sitemap modification date and should change when content changes.

`google318d5d528899d7bd.html` is the public Google Search Console verification file for the laboratory account. Preserve it after verification. Submit `https://deepmathlab.github.io/sitemap.xml` and request the homepage's indexing in that account's URL-prefix property. Search-engine submission is not a guarantee of immediate visibility in search results.


## Current introduction and member profiles

The homepage uses the three axes in the professor's 2025 introduction: Mathematics for AI, AI for Mathematics, and Mathematical Simulation, Analysis, and Modeling. `research_axes` supplies these summaries. The existing `research` array retains the specific numerical foundations and DOI relationships, including stable links for geometry, fractional equations and mechanics. No unverified AI paper or application project is added to the bibliography.

Hansu Kim, Soobeen Jung and Hwanseo Lee supplied their names, roles, research interests, public email addresses and photographs in replies to the website-profile request on 8 October 2026. Hansu also supplied a GitHub link. Their photo files are web exports of the supplied originals, with metadata removed and no generated facial changes. Original correspondence and source photographs are kept outside the public repository.

The hero remains without an illustration. Social sharing uses a flat typographic lab card, with the lab's five research connections and no personal photograph.


## Research imagery and information structure

The 1.2.0 update revisits each of the eight official Figma guides in the crosswalk above. The main introduction keeps the representative-image area open. Three research axes use a title, one sentence, method keywords and an original research example. The lab's shared foundation and five research connections are drawn as a two-level HTML diagram with readable labels. This describes the professor's mission scope, not a matrix of active projects.

Three images come from the professor-supplied 2025 introduction:

| Source inside PPTX | Website example | Interpretation |
| --- | --- | --- |
| `ppt/media/image61.png` | `research-initialization` | PINN training loss for a Burgers-equation example under different initialization settings |
| `ppt/media/image14.png` | `research-helmholtz` | A Helmholtz approximation on a curved geometry using isogeometric collocation and a neural network |
| `ppt/media/image68.png` | `research-phase-field` | A phase-field pattern on a circular domain; no time or fractional order is inferred |

Each PNG is an unchanged copy of the embedded source image. WebP previews preserve image proportions, axes, legends and color scales. HTML captions name the example and its source. A full-size link opens the source PNG in a new tab. No performance comparison, model parameter or publication DOI is inferred from these images.

Research overviews show Focus, Methods and Example. Dense numerical foundations use native disclosure rows, retaining their descriptions and related papers. Existing fragment links open the relevant row. The disclosures remain usable without JavaScript. Sources, full-size links, intrinsic image sizes, alt text and link focus states are checked separately from image appearance. Browser viewport checks do not certify real-device performance or full accessibility compliance.

## First-screen refinement

Version 1.3.0 uses typography as the main visual: a full-width, two-line mission, a concise introduction, a primary Research action and a quiet Publications link. Five static field labels describe the lab’s scope without implying project counts or achievements. No representative image, gradient, animation or tracking dependency was added. Homepage research cards retain original examples and remove repetitive method tags; the Research page keeps the methods.

The refinement revisits Figma’s [visual hierarchy](https://www.figma.com/resource-library/what-is-visual-hierarchy/), [typography](https://www.figma.com/resource-library/typography-in-design/) and [grid layouts](https://www.figma.com/resource-library/web-design-grid-layout-examples/). [Apple](https://www.apple.com/), [Google DeepMind About](https://deepmind.google/about/) and [IBM Research](https://research.ibm.com/) inform the emphasis on one first-screen message and clear exploration paths. Their logos, media, wording, claims and site code are not reused.
