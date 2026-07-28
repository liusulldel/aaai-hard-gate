# AAAI-27 official gate reference

Verified against the official AAAI-27 materials on 2026-07-27.

## Authoritative sources

- Author Kit redirect: <https://aaai.org/authorkit27/>
- Author Kit ZIP: <https://aaai.org/wp-content/uploads/2026/05/AuthorKit27.zip>
- Main-track submission instructions: <https://aaai.org/conference/aaai/aaai-27/submission-instructions/>
- Main technical track call: <https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/>

Observed kit fingerprints:

- `AuthorKit27.zip`: `e28c6ac9bc6eb3b4e2d849547d2cefb5162610ee39d0a12e0dc62d1126b44a7d`
- `aaai2027.sty`: `391bce82815bf698b8e382dd3ae7e30c75d7ab46df140cb295b1266016bc8623`
- `aaai2027.bst`: `5db7765ba99de5c1e4686f9b3940a0add9c5e702f2164514462bec130ccb6e3c`
- Required PDF metadata marker in the source: `/TemplateVersion (2027.1)`

If AAAI replaces the kit, update the skill rather than accepting the old hash.

## Review-submission blockers

- Submit a trouble-free, high-resolution PDF through OpenReview.
- Use the AAAI two-column camera-ready style on US Letter paper.
- Limit non-reference main content (body text, figures, tables, algorithms) strictly to pages 1–7. Spilling any main body text onto Page 8 results in immediate desk rejection. Total PDF is limited to nine pages, with Pages 8–9 reserved exclusively for references.
- Use anonymous submission mode; remove author and affiliation information and omit acknowledgments.
- Clear identifying PDF metadata and anonymize references or links that reveal the authors.
- Upload the completed reproducibility checklist separately.

## Author Kit invariants

- Compile LaTeX with PDFLaTeX using the unmodified `aaai2027.sty` and `aaai2027.bst`.
- Embed every font, including fonts in figures. Reject Type 3 fonts.
- Use PDF version 1.5 or higher, no encryption, no embedded links or bookmarks, and no page headers, footers, or numbers.
- Do not alter margins, columns, spacing, line spacing, captions, fonts, font sizes, or the style file.
- Do not use `.ps` or `.eps` figures.
- Do not use packages or commands that alter the prescribed layout. The official kit explicitly lists common forbidden packages and commands; the checker encodes that list.

## Graphics and tables hard requirements

Apply these to the final placed size, not the figure's editing-canvas size.

- Use only JPG/JPEG, PNG, or PDF graphics. Do not use GIF, PS, or EPS.
- Put every figure caption below its illustration in 10 pt Roman. Do not make the caption smaller, bold, or italic except where individual words require italics.
- Make every label and other text inside a figure at least 9 pt. Use Times Roman or Helvetica for figure callouts.
- Embed every font in every graphic. Reject Type 3 fonts. Convert or remove CID/Identity-H/Identity-V fonts; restrict non-Roman scripts to bitmapped figures or outlines as the kit directs.
- Incorporate raster graphics at 300 dpi. Reject low-resolution screen dumps, including 72 dpi images.
- Make every line stroke at least 0.5 pt; reject hairlines. Uniform line widths between 0.5 and 2 pt are recommended.
- Keep color contrast greater than 4.5:1 under WCAG 2.0. The figure must remain decipherable in grayscale and without color as the sole distinguishing channel.
- Crop and resize graphics outside LaTeX. Reject starred `\includegraphics` and `clip`, `trim`, or `viewport` cropping. Do not group figures with `minipage`.
- Keep figures inside the page margins and column gutter. Place them near their first discussion and number them sequentially.
- Use `graphicx` to insert figures. Pre-generate plots outside the paper source; `pgfplots` is forbidden in the submitted source.
- Set tables in 10 pt Roman. If necessary, reduce table text only to 9 pt. Do not use `\resizebox`, `\scalebox`, `\adjustbox`, or another whole-table scaling mechanism.
- Put every table caption below the table in 10 pt Roman; do not make it smaller, bold, or italic except where individual words require italics.

The checker automatically rejects source-detectable format, cropping, caption-position, figure-`minipage`, and whole-table-scaling violations. PDF resource inspection rejects unembedded, Type 3, and Identity-encoded fonts. The `figures`, `tables`, and `layout` attestations remain mandatory for final-size typography, effective raster resolution, strokes, contrast, grayscale/color independence, caption styling, placement, and visual margin/gutter safety.

## Limits of automation

PDF parsing cannot prove semantic anonymity, Title Case, reference-only content, final-size figure/table typography, effective raster resolution, stroke width, color contrast, color-independent interpretation, caption styling, or the absence of all visual margin violations. Those items remain mandatory manual gates. OpenReview upload acceptance is not a certificate of formatting compliance.

The hard gate also requires a manual source–PDF match check. This prevents a compliant PDF from masking violations in a different or stale TeX source.
