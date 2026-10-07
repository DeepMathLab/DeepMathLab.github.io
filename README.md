# DeepMathLab

English-first website for computational mathematics and scientific computing at KENTECH, led by Hyunju Kim.

## Update the website

Edit `site.json` for research, people, publications, and bilingual content. Edit `styles.css` and `app.js` for presentation and interactions.

```sh
python3 build.py
python3 -m http.server 4173 --bind 127.0.0.1
```

The build writes `index.html` (English), `ko.html` (Korean), and `home.html` (English sharing URL). All files are served directly from the repository root. GitHub Pages publishes the `main` branch root. `.nojekyll` disables Jekyll processing.

## Content status and sources

This first public version is marked as a website concept. The complete member roster, final lab name spelling, and contact address remain under review. Publications are selected published papers, not a complete or latest bibliography.

- [KENTECH faculty website](https://kentech.ac.kr/hjkim/template/main.do)
- [KENTECH faculty directory](https://admission.kentech.ac.kr/ourFaculty.do)
- Publication records are linked by DOI.
- Faculty portrait: KENTECH faculty directory.
- The spline surface is a conceptual vector illustration, not a simulation result.

Source details and verification date are recorded in `site.json`.

## Link previews

`share-card.svg` is the editable brand artwork and `share-card.png` is its 1200 × 630 export. Both English and Korean pages explicitly select the PNG with Open Graph and Twitter Card metadata. Link previews use this brand artwork.

After changing the shared image, update its version in `SHARE_IMAGE` in `build.py` and rebuild the pages. Kakao may cache previous URL metadata; its URL metadata tool can reset the cached preview.

Use https://deepmathlab.github.io/home.html when sharing while the original homepage preview remains cached. This page contains the same English website, with its own matching canonical and `og:url`, and does not redirect to the cached root URL. Keep it generated from the same content to avoid stale copies. Kakao's [official support explains](https://devtalk.kakao.com/t/og-url/136380) that a different `og:url` can cause the crawler to scrape that destination instead.
