# Asset license record

Reviewed on 8 October 2026. This record covers the three font families and three conceptual SVGs listed below. It records upstream terms and asset provenance; it does not grant a reuse license for other website media.

## Fonts

Inter, Manrope, and IBM Plex Mono are distributed under the **SIL Open Font License, Version 1.1 (26 February 2007)**. The full upstream license texts are preserved unchanged in `licenses/`.

The audited distribution is the official [Google Fonts repository](https://github.com/google/fonts/tree/e9a263957eae262c5701d40b86eb1b2cbb9152e9), pinned to commit `e9a263957eae262c5701d40b86eb1b2cbb9152e9`.

| Font | Upstream file | Font version in metadata | Included license |
| --- | --- | --- | --- |
| Inter | [`ofl/inter/Inter[opsz,wght].ttf`](https://github.com/google/fonts/blob/e9a263957eae262c5701d40b86eb1b2cbb9152e9/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf) | 4.001; git-66647c0bb | [Inter-OFL.txt](licenses/Inter-OFL.txt) |
| Manrope | [`ofl/manrope/Manrope[wght].ttf`](https://github.com/google/fonts/blob/e9a263957eae262c5701d40b86eb1b2cbb9152e9/ofl/manrope/Manrope%5Bwght%5D.ttf) | 4.505 | [Manrope-OFL.txt](licenses/Manrope-OFL.txt) |
| IBM Plex Mono | [`ofl/ibmplexmono/IBMPlexMono-Regular.ttf`](https://github.com/google/fonts/blob/e9a263957eae262c5701d40b86eb1b2cbb9152e9/ofl/ibmplexmono/IBMPlexMono-Regular.ttf) | 2.3 | [IBMPlexMono-OFL.txt](licenses/IBMPlexMono-OFL.txt) |

### Copyright and names

The distribution license files and the font binaries contain the following notices. Differences in upstream copyright years are recorded here; neither the license files nor the binary metadata are rewritten.

- **Inter:** distribution OFL notice: `Copyright 2020 The Inter Project Authors (https://github.com/rsms/inter)`. Binary notice: `Copyright 2016 The Inter Project Authors (https://github.com/rsms/inter)`. Binary trademark field: `Inter UI and Inter is a trademark of rsms.` The accompanying OFL file declares no Reserved Font Name.
- **Manrope:** distribution OFL notice: `Copyright 2018 The Manrope Project Authors (https://github.com/googlefonts/manrope)`. Binary notice: `Copyright 2019 The Manrope Project Authors (https://github.com/googlefonts/manrope)`. The accompanying OFL file declares no Reserved Font Name.
- **IBM Plex Mono:** distribution OFL notice: `Copyright © 2017 IBM Corp. with Reserved Font Name "Plex"`. Binary notice: `Copyright 2017 IBM Corp. All rights reserved.` Binary trademark field: `IBM Plex(r) is a trademark of IBM Corp, registered in many jurisdictions worldwide.` **Plex is a Reserved Font Name.**

All three audited binaries identify OFL 1.1 in their license metadata. Their OpenType OS/2 `fsType` values are `0`; the OFL license text, rather than that flag alone, establishes the distribution conditions.

### Website use and distribution conditions

- The OFL permits use, copying, embedding, modification, and redistribution, subject to its conditions. The [official FAQ, section 2.1](https://openfontlicense.org/ofl-faq/) explicitly permits CSS `@font-face` web use and hosting on the same server as other website assets.
- Keep the relevant copyright notice and full OFL license with redistributed fonts, including public repository and website distributions. The fonts remain under OFL; the license does not require the website, its text, or graphics created with the fonts to be licensed under OFL.
- Do not sell a font by itself, relicense the font under a different license, or imply endorsement by its authors.
- Modified fonts must follow the Reserved Font Name restriction. In particular, do not subset or otherwise modify IBM Plex Mono while retaining the reserved name unless the applicable upstream permission allows it.
- The [official FAQ, sections 2.2–2.2.2](https://openfontlicense.org/ofl-faq/) describes a narrow WOFF/WOFF2 compression exception: unchanged original font data and equivalent, unaltered metadata may be compressed without a name change. Subsetting, other optimization, or incomplete metadata preservation is not automatically covered by that exception.

These points summarize the primary sources for this distribution. The complete included license text controls.

### Source integrity

SHA-256 values for the audited official TrueType binaries:

```text
Inter[opsz,wght].ttf    29160a80ff49ddcab2c97711247e08b1fab27a484a329ce8b813d820dc559031
Manrope[wght].ttf      3ae11c49db0455a3cc33e37d380f20fdb8c7f8b41dc07625c177e3d87a9d6ae6
IBMPlexMono-Regular.ttf 6a3412f058c7d8dfd9170c41e85ade48e5156ecb89356110ca57a0a27734af46
```

Official accompanying license sources:

- [Inter OFL](https://github.com/google/fonts/blob/e9a263957eae262c5701d40b86eb1b2cbb9152e9/ofl/inter/OFL.txt); [Inter project](https://github.com/rsms/inter).
- [Manrope OFL](https://github.com/google/fonts/blob/e9a263957eae262c5701d40b86eb1b2cbb9152e9/ofl/manrope/OFL.txt); [Manrope project](https://github.com/googlefonts/manrope).
- [IBM Plex Mono OFL](https://github.com/google/fonts/blob/e9a263957eae262c5701d40b86eb1b2cbb9152e9/ofl/ibmplexmono/OFL.txt); [IBM Plex project](https://github.com/IBM/plex).

### Repository webfont files

The website font configuration uses the local files below through CSS `@font-face`, rather than the Google Fonts stylesheet. [`build_fonts.py`](build_fonts.py) downloads the pinned official TrueType files, verifies their source SHA-256 values, and packages them as **WOFF 1.0** using lossless zlib compression. It does not subset glyphs, rename fonts, rewrite copyright or licensing metadata, or transform outline or variation data.

| Website file | Bytes | Preserved font tables | SHA-256 |
| --- | ---: | ---: | --- |
| [`fonts/inter.woff`](fonts/inter.woff) | 456,604 | 21 of 21 | `1e9f1183e37fde48807797b9ad4f503e01d1de253e4d60b9e6f9d2b329acac06` |
| [`fonts/manrope.woff`](fonts/manrope.woff) | 67,668 | 19 of 19 | `d544bc69d5e306079beefa3a5d3834b8f06b7654f1a266f3cac1b283f72b8b7b` |
| [`fonts/ibm-plex-mono.woff`](fonts/ibm-plex-mono.woff) | 56,372 | 19 of 19 | `2ce499d827ef11554ccf31896b9d0840c11d016b1bc6ca6d0c019c55ceea0f33` |

Total font payload: **580,644 bytes**. WOFF-specific extended metadata and private-data blocks are omitted. The original font tables, including `name` and `OS/2`, remain intact inside the WOFF package.

An independent inspection of these actual WOFF files decompressed every table and compared it with the SHA-verified source: **all font table bytes matched**, including copyright, licensing, naming, and variable-font tables. It also checked WOFF signatures and lengths, original table checksums, sorted directories, original physical table order, four-byte alignment and zero padding, absence of overlapping ranges or gaps, and successful reproduction by the packaging script. These checks follow the [W3C WOFF 1.0 format specification](https://www.w3.org/TR/WOFF/).

The unchanged font data and omission of WOFF-specific metadata are the basis for retaining the upstream family names under [OFL FAQ 2.2.1](https://openfontlicense.org/ofl-faq/). The included copyright notices and full OFL texts accompany this repository distribution.

## Conceptual research SVGs

`research-concept-ai.svg`, `research-concept-pinn.svg`, and `research-concept-modeling.svg` were created as original, code-native SVG source for this website. They do not incorporate stock imagery, third-party design assets, or traced figures from papers.

Their subject matter follows the documented lab research methods: neural-network initialization and signal propagation; physics-informed learning with equation and boundary constraints; and geometry-aware numerical approximation. They are **conceptual method diagrams**, not experimental or computed research results. In particular, the final contours in the modeling SVG are schematic and have no physical units or numerical values.

The typography references the font families listed above, with system fallback fonts. No font binary or glyph outline is embedded inside these SVGs. This provenance record does not declare a separate general reuse license for the SVG artwork.
