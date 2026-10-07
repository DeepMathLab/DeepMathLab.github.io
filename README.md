# DeepMathLab

English-first website for computational mathematics and scientific computing at KENTECH, led by Hyunju Kim.

## Update the website

Edit `site.json` for research, people, publications, and bilingual content. Edit `styles.css` and `app.js` for presentation and interactions.

```sh
python3 build.py
python3 -m http.server 4173 --bind 127.0.0.1
```

The build writes `index.html` (English) and `ko.html` (Korean). All files are served directly from the repository root. GitHub Pages publishes the `main` branch root. `.nojekyll` disables Jekyll processing.

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

After changing the shared image, update its version in `SHARE_IMAGE` in `build.py` and rebuild both pages. Kakao may cache previous URL metadata; its URL metadata tool can reset the cached preview.
