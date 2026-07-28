#!/usr/bin/env python3
"""Fail-closed AAAI-27 source and PDF submission-format gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

OFFICIAL_STYLE_SHA256 = "391bce82815bf698b8e382dd3ae7e30c75d7ab46df140cb295b1266016bc8623"
PDF_VERSION_MIN = (1, 5)
LETTER_WIDTH = 612.0
LETTER_HEIGHT = 792.0
POINT_TOLERANCE = 1.0
ALLOWED_GRAPHIC_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}
FORBIDDEN_GRAPHIC_EXTENSIONS = {".gif", ".eps", ".ps"}

FORBIDDEN_PACKAGES = {
    "authblk", "babel", "balance", "bbm", "cjk", "epsf", "epsfig",
    "euler", "float", "flushend", "fullpage", "geometry", "graphics",
    "hyperref", "indentfirst", "layout", "lmodern", "multicol", "nameref",
    "navigator", "pdfcomment", "pgfplots", "psfig", "pstricks", "savetrees",
    "setspace", "stfloats", "t1enc", "tabu", "times", "titlesec",
    "tocbibind", "ulem", "wrapfig",
}

FORBIDDEN_COMMANDS = {
    "abovecaption", "abovedisplay", "addevensidemargin", "addsidemargin",
    "addtolength", "balance", "baselinestretch", "belowcaption", "belowdisplay",
    "break", "clearpage", "clip", "float", "linespread", "newpage",
    "nocopyright", "pagebreak", "pagestyle", "setlength", "tiny", "trim",
}

LAYOUT_LENGTHS = {
    "columnsep", "evensidemargin", "oddsidemargin", "textheight", "textwidth",
    "topmargin", "topskip",
}

REQUIRED_ATTESTATIONS = {
    "layout", "anonymity", "title-case", "figures", "tables", "checklist-complete",
    "source-pdf-match",
}

OPTIONAL_ATTESTATIONS = {
    "graphics-source-files", "official-style", "references-only", "source-review",
}

INCLUDEGRAPHICS_RE = re.compile(
    r"\\includegraphics(?P<star>\*)?\s*(?:\[(?P<options>[^]]*)\])?\s*\{(?P<target>[^}]*)\}",
    re.IGNORECASE | re.DOTALL,
)
FLOAT_ENV_RE = re.compile(
    r"\\begin\{(?P<kind>figure\*?|table\*?)\}(?P<body>.*?)\\end\{(?P=kind)\}",
    re.IGNORECASE | re.DOTALL,
)
CAPTION_RE = re.compile(r"\\caption(?:\s*\[[^]]*\])?\s*\{", re.IGNORECASE | re.DOTALL)
TABLE_CONTENT_END_RE = re.compile(
    r"\\end\{(?:tabular\*?|tabularx|array)\}", re.IGNORECASE,
)


@dataclass
class Finding:
    status: str
    code: str
    message: str
    location: str | None = None


class Gate:
    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def add(self, status: str, code: str, message: str, location: str | None = None) -> None:
        self.findings.append(Finding(status, code, message, location))

    def fail(self, code: str, message: str, location: str | None = None) -> None:
        self.add("FAIL", code, message, location)

    def passed(self, code: str, message: str, location: str | None = None) -> None:
        self.add("PASS", code, message, location)

    def manual(self, code: str, message: str, location: str | None = None) -> None:
        self.add("MANUAL", code, message, location)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strip_tex_comments(text: str) -> str:
    output: list[str] = []
    for line in text.splitlines(keepends=True):
        cut = len(line)
        for index, char in enumerate(line):
            if char != "%":
                continue
            slashes = 0
            pos = index - 1
            while pos >= 0 and line[pos] == "\\":
                slashes += 1
                pos -= 1
            if slashes % 2 == 0:
                cut = index
                break
        kept = line[:cut]
        if line.endswith("\n") and not kept.endswith("\n"):
            kept += "\n"
        output.append(kept)
    return "".join(output)


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def find_tex_sources(main: Path, gate: Gate) -> list[tuple[Path, str]]:
    collected: list[tuple[Path, str]] = []
    seen: set[Path] = set()

    def visit(path: Path) -> None:
        resolved = path.resolve()
        if resolved in seen:
            return
        seen.add(resolved)
        if not resolved.is_file():
            gate.fail("tex.include-missing", "Included TeX source does not exist.", str(resolved))
            return
        try:
            raw = resolved.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raw = resolved.read_text(encoding="utf-8", errors="replace")
            gate.fail("tex.encoding", "TeX source is not valid UTF-8.", str(resolved))
        clean = strip_tex_comments(raw)
        collected.append((resolved, clean))
        for match in re.finditer(r"\\(?:input|include)\s*\{([^}]+)\}", clean):
            name = match.group(1).strip()
            child = resolved.parent / name
            if child.suffix == "":
                child = child.with_suffix(".tex")
            visit(child)

    visit(main)
    return collected


def package_declarations(text: str) -> Iterable[tuple[str, set[str], int]]:
    pattern = re.compile(r"\\usepackage(?:\s*\[([^]]*)\])?\s*\{([^}]*)\}", re.DOTALL)
    for match in pattern.finditer(text):
        options = {item.strip().lower() for item in (match.group(1) or "").split(",") if item.strip()}
        for package in match.group(2).split(","):
            name = package.strip().lower()
            if name:
                yield name, options, match.start()


def graphic_extension(source_path: Path, target: str) -> tuple[str | None, list[Path]]:
    """Return an explicit/resolved graphic extension and existing candidates."""
    normalized = target.strip()
    explicit = Path(normalized).suffix.lower()
    if explicit:
        return explicit, [source_path.parent / normalized]
    if "\\" in normalized:
        return None, []
    candidates = [
        source_path.parent / f"{normalized}{extension}"
        for extension in sorted(ALLOWED_GRAPHIC_EXTENSIONS | FORBIDDEN_GRAPHIC_EXTENSIONS)
        if (source_path.parent / f"{normalized}{extension}").is_file()
    ]
    extensions = {candidate.suffix.lower() for candidate in candidates}
    if len(extensions) == 1:
        return extensions.pop(), candidates
    return None, candidates


def check_graphics_source(sources: list[tuple[Path, str]], gate: Gate) -> None:
    graphic_count = 0
    format_failures = 0
    crop_failures = 0
    caption_failures = 0
    table_resize_failures = 0
    figure_minipage_failures = 0
    unresolved_graphics: list[str] = []

    for source_path, text in sources:
        for match in INCLUDEGRAPHICS_RE.finditer(text):
            graphic_count += 1
            location = f"{source_path}:{line_number(text, match.start())}"
            target = match.group("target").strip()
            options = (match.group("options") or "").lower()
            forbidden_crop = bool(match.group("star")) or bool(
                re.search(r"(?:^|,)\s*(?:clip|trim|viewport)\b", options)
            )
            if forbidden_crop:
                crop_failures += 1
                gate.fail(
                    "tex.figure-cropping",
                    "Crop graphics outside LaTeX; starred includegraphics and clip/trim/viewport options are forbidden.",
                    location,
                )

            extension, candidates = graphic_extension(source_path, target)
            if extension in ALLOWED_GRAPHIC_EXTENSIONS:
                continue
            if extension in FORBIDDEN_GRAPHIC_EXTENSIONS or extension:
                format_failures += 1
                gate.fail(
                    "tex.figure-format",
                    f"Graphic '{target}' uses {extension or 'an unsupported format'}; only JPG, JPEG, PNG, and PDF are permitted.",
                    location,
                )
            else:
                candidate_list = ", ".join(str(path) for path in candidates) or "no directly resolvable file"
                unresolved_graphics.append(f"{location}: {target} ({candidate_list})")

        for env_match in FLOAT_ENV_RE.finditer(text):
            kind = env_match.group("kind").lower()
            body = env_match.group("body")
            location = f"{source_path}:{line_number(text, env_match.start())}"
            captions = list(CAPTION_RE.finditer(body))
            if kind.startswith("figure"):
                images = list(INCLUDEGRAPHICS_RE.finditer(body))
                if re.search(r"\\begin\{minipage\}", body, re.IGNORECASE):
                    figure_minipage_failures += 1
                    gate.fail(
                        "tex.figure-minipage",
                        "Do not use minipage to group figures under the AAAI-27 Author Kit.",
                        location,
                    )
                if images and not captions:
                    caption_failures += 1
                    gate.fail("tex.figure-caption", "Each figure requires a caption below the illustration.", location)
                elif images and captions[0].start() < images[-1].end():
                    caption_failures += 1
                    gate.fail("tex.figure-caption", "The figure caption must appear below the illustration.", location)
            elif kind.startswith("table"):
                if re.search(
                    r"\\(?:resizebox|scalebox|adjustbox)\b|\\begin\{adjustbox\}",
                    body,
                    re.IGNORECASE,
                ):
                    table_resize_failures += 1
                    gate.fail(
                        "tex.table-resize",
                        "Do not resize or scale an entire table; table text must remain 9 pt or larger.",
                        location,
                    )
                content_ends = [match.end() for match in TABLE_CONTENT_END_RE.finditer(body)]
                if not captions:
                    caption_failures += 1
                    gate.fail("tex.table-caption", "Each table requires a 10 pt Roman caption below the table.", location)
                elif content_ends and captions[0].start() < max(content_ends):
                    caption_failures += 1
                    gate.fail("tex.table-caption", "The table caption must appear below the table.", location)

    if graphic_count and not format_failures and not unresolved_graphics:
        gate.passed("tex.figure-format", f"All {graphic_count} graphic reference(s) resolve to JPG, JPEG, PNG, or PDF.")
    if graphic_count and not crop_failures:
        gate.passed("tex.figure-cropping", "No starred includegraphics or clip/trim/viewport option was found.")
    if not caption_failures:
        gate.passed("tex.float-captions", "No source-detectable figure/table caption-position violation was found.")
    if not table_resize_failures:
        gate.passed("tex.table-resize", "No whole-table resize/scaling command was found in table floats.")
    if not figure_minipage_failures:
        gate.passed("tex.figure-minipage", "No minipage grouping was found in figure floats.")
    if unresolved_graphics:
        preview = "; ".join(unresolved_graphics[:3])
        if len(unresolved_graphics) > 3:
            preview += f"; and {len(unresolved_graphics) - 3} more"
        gate.manual(
            "graphics-source-files",
            "Verify every unresolved extensionless or macro-based graphic resolves only to JPG, JPEG, PNG, or PDF: " + preview,
        )


def check_tex(main: Path, style: Path | None, gate: Gate) -> None:
    sources = find_tex_sources(main, gate)
    if not sources:
        return
    main_path, main_text = sources[0]
    preamble = main_text.split(r"\begin{document}", 1)[0]

    docclass = re.search(r"\\documentclass\s*\[([^]]*)\]\s*\{article\}", preamble, re.DOTALL)
    if not docclass or "letterpaper" not in {x.strip().lower() for x in docclass.group(1).split(",")}:
        gate.fail("tex.documentclass", "Require \\documentclass[letterpaper]{article}.", str(main_path))
    else:
        gate.passed("tex.documentclass", "US-Letter article document class is declared.")

    packages = list(package_declarations(preamble))
    aaai = [item for item in packages if item[0] == "aaai2027"]
    if len(aaai) != 1 or "submission" not in aaai[0][1]:
        gate.fail("tex.submission-mode", "Require exactly one \\usepackage[submission]{aaai2027} declaration.", str(main_path))
    else:
        gate.passed("tex.submission-mode", "AAAI-27 anonymous submission mode is enabled.")

    required_packages = {
        "url": {"hyphens"},
        "graphicx": set(),
        "natbib": set(),
        "caption": set(),
    }
    by_name: dict[str, list[set[str]]] = {}
    for name, options, _ in packages:
        by_name.setdefault(name, []).append(options)
    for name, expected_options in required_packages.items():
        declarations = by_name.get(name, [])
        if not declarations:
            gate.fail(f"tex.required-package.{name}", f"Required package '{name}' is missing.", str(main_path))
        elif name in {"natbib", "caption"} and any(options for options in declarations):
            gate.fail(f"tex.package-options.{name}", f"Package '{name}' must not have options.", str(main_path))
        elif expected_options and not any(expected_options <= options for options in declarations):
            gate.fail(f"tex.package-options.{name}", f"Package '{name}' requires options: {', '.join(sorted(expected_options))}.", str(main_path))
        else:
            gate.passed(f"tex.required-package.{name}", f"Required package '{name}' is present.")

    required_patterns = {
        "tex.urlstyle": (r"\\urlstyle\s*\{rm\}", r"Require \\urlstyle{rm}."),
        "tex.urlfont": (r"\\def\s*\\UrlFont\s*\{\s*\\rm\s*\}", r"Require \\def\UrlFont{\rm}."),
        "tex.frenchspacing": (r"\\frenchspacing\b", r"Require \\frenchspacing."),
        "tex.template-version": (r"/TemplateVersion\s*\(2027\.1\)", "Require /TemplateVersion (2027.1) in \\pdfinfo."),
    }
    for code, (pattern, message) in required_patterns.items():
        if re.search(pattern, preamble, re.DOTALL):
            gate.passed(code, message.replace("Require", "Found"))
        else:
            gate.fail(code, message, str(main_path))

    combined = "\n".join(text for _, text in sources)
    for source_path, text in sources:
        for package, _, position in package_declarations(text):
            if package in FORBIDDEN_PACKAGES:
                gate.fail(
                    "tex.forbidden-package",
                    f"Forbidden package: {package}.",
                    f"{source_path}:{line_number(text, position)}",
                )
        command_re = re.compile(r"\\(" + "|".join(sorted(map(re.escape, FORBIDDEN_COMMANDS), key=len, reverse=True)) + r")\b")
        for match in command_re.finditer(text):
            gate.fail(
                "tex.forbidden-command",
                f"Forbidden command: \\{match.group(1)}.",
                f"{source_path}:{line_number(text, match.start())}",
            )
        layout_assignment_re = re.compile(
            r"\\(" + "|".join(sorted(LAYOUT_LENGTHS)) + r")\s*(?:=|\\(?:advance|multiply|divide)\b)"
        )
        for match in layout_assignment_re.finditer(text):
            gate.fail(
                "tex.layout-modification",
                f"Modification of layout length is forbidden: \\{match.group(1)}.",
                f"{source_path}:{line_number(text, match.start())}",
            )
        for match in re.finditer(r"\\(?:vspace|vskip)\s*\{?\s*-", text):
            gate.fail(
                "tex.negative-spacing",
                "Negative vspace/vskip requires removal under the hard gate.",
                f"{source_path}:{line_number(text, match.start())}",
            )
        for match in re.finditer(r"\\(?:href|hypersetup|pdfbookmark|bookmark)\b", text):
            gate.fail(
                "tex.embedded-link-command",
                f"Embedded-link/bookmark command is forbidden: {match.group(0)}.",
                f"{source_path}:{line_number(text, match.start())}",
            )

    if re.search(r"\\(?:section\*?|subsection\*?)\s*\{\s*Acknowledge?ments?\s*\}", combined, re.IGNORECASE):
        gate.fail("tex.acknowledgments", "Acknowledgments must be omitted from the review submission.")
    else:
        gate.passed("tex.acknowledgments", "No acknowledgments heading was found in TeX source.")

    check_graphics_source(sources, gate)

    style_path = style or (main.parent / "aaai2027.sty")
    if style_path.is_file():
        actual = sha256(style_path)
        if actual == OFFICIAL_STYLE_SHA256:
            gate.passed("tex.official-style", "Local aaai2027.sty matches the verified official Author Kit hash.", str(style_path))
        else:
            gate.fail("tex.official-style", f"aaai2027.sty hash mismatch: {actual}.", str(style_path))
    else:
        gate.manual("official-style", "Confirm the build resolved the unmodified official aaai2027.sty (2027.1); no local style was available to hash.")


def dereference(value: Any) -> Any:
    try:
        return value.get_object()
    except AttributeError:
        return value


def object_key(value: Any) -> tuple[Any, ...]:
    if hasattr(value, "idnum"):
        return ("indirect", value.idnum, getattr(value, "generation", 0))
    ref = getattr(value, "indirect_reference", None)
    if ref is not None and hasattr(ref, "idnum"):
        return ("indirect", ref.idnum, getattr(ref, "generation", 0))
    return ("direct", id(value))


def embedded_font(font: Any) -> tuple[bool, list[str]]:
    font = dereference(font)
    subtype = str(font.get("/Subtype", "unknown"))
    if subtype == "/Type3":
        return False, [subtype]
    concrete_fonts: list[Any]
    if subtype == "/Type0":
        concrete_fonts = [dereference(item) for item in dereference(font.get("/DescendantFonts", []))]
    else:
        concrete_fonts = [font]
    details: list[str] = [subtype]
    embedded = True
    for concrete in concrete_fonts:
        details.append(str(concrete.get("/Subtype", "unknown")))
        descriptor = dereference(concrete.get("/FontDescriptor")) if concrete.get("/FontDescriptor") else None
        has_program = bool(descriptor) and any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3"))
        embedded = embedded and has_program
    return embedded, details


def check_resources(resources: Any, page_number: int, gate: Gate, seen_fonts: set[tuple[Any, ...]], seen_resources: set[tuple[Any, ...]]) -> None:
    if resources is None:
        return
    resource_key = object_key(resources)
    if resource_key in seen_resources:
        return
    seen_resources.add(resource_key)
    resources = dereference(resources)
    fonts = dereference(resources.get("/Font", {}))
    for label, font_ref in fonts.items():
        key = object_key(font_ref)
        if key in seen_fonts:
            continue
        seen_fonts.add(key)
        font = dereference(font_ref)
        name = str(font.get("/BaseFont", label))
        subtype = str(font.get("/Subtype", "unknown"))
        encoding = str(font.get("/Encoding", ""))
        embedded, details = embedded_font(font)
        location = f"PDF page {page_number}: {name}"
        if subtype == "/Type3" or "/Type3" in details:
            gate.fail("pdf.type3-font", f"Type 3 font is forbidden: {name}.", location)
        elif not embedded:
            gate.fail("pdf.unembedded-font", f"Font program is not embedded: {name} ({'/'.join(details)}).", location)
        else:
            gate.passed("pdf.embedded-font", f"Embedded font: {name} ({'/'.join(details)}).", location)
        if "Identity-H" in encoding or "Identity-V" in encoding:
            gate.fail("pdf.identity-font", f"Identity-encoded font requires removal or conversion under the Author Kit: {name} ({encoding}).", location)
    xobjects = dereference(resources.get("/XObject", {}))
    for _, xobject_ref in xobjects.items():
        xobject = dereference(xobject_ref)
        if str(xobject.get("/Subtype", "")) == "/Form":
            check_resources(xobject.get("/Resources"), page_number, gate, seen_fonts, seen_resources)


def parse_pdf_version(header: str) -> tuple[int, int] | None:
    match = re.search(r"%PDF-(\d+)\.(\d+)", header)
    return (int(match.group(1)), int(match.group(2))) if match else None


def check_pdf(pdf: Path, gate: Gate) -> int | None:
    try:
        from pypdf import PdfReader
    except Exception as exc:
        raise RuntimeError(f"pypdf is required for the hard gate: {exc}") from exc

    try:
        reader = PdfReader(str(pdf), strict=True)
    except Exception as exc:
        gate.fail("pdf.parse", f"PDF cannot be parsed strictly: {exc}", str(pdf))
        return None

    if reader.is_encrypted:
        gate.fail("pdf.encryption", "Encrypted or password-protected PDFs are forbidden.", str(pdf))
        return None
    gate.passed("pdf.encryption", "PDF is not encrypted.")

    version = parse_pdf_version(getattr(reader, "pdf_header", ""))
    if version is None:
        gate.fail("pdf.version", "Could not determine the PDF version.")
    elif version < PDF_VERSION_MIN:
        gate.fail("pdf.version", f"PDF version {version[0]}.{version[1]} is below 1.5.")
    else:
        gate.passed("pdf.version", f"PDF version is {version[0]}.{version[1]}.")

    pages = len(reader.pages)
    if pages > 9:
        gate.fail("pdf.page-count", f"PDF has {pages} pages; AAAI-27 permits at most 9.")
    elif pages < 1:
        gate.fail("pdf.page-count", "PDF has no pages.")
    else:
        gate.passed("pdf.page-count", f"PDF has {pages} page(s).")

    seen_fonts: set[tuple[Any, ...]] = set()
    seen_resources: set[tuple[Any, ...]] = set()
    extracted_pages: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        box = page.mediabox
        width = float(box.width)
        height = float(box.height)
        rotation = int(page.get("/Rotate", 0) or 0) % 360
        if abs(width - LETTER_WIDTH) > POINT_TOLERANCE or abs(height - LETTER_HEIGHT) > POINT_TOLERANCE:
            gate.fail("pdf.page-size", f"Page is {width:.2f} x {height:.2f} pt, not US Letter 612 x 792 pt.", f"PDF page {index}")
        elif rotation:
            gate.fail("pdf.rotation", f"Page rotation is {rotation} degrees.", f"PDF page {index}")
        else:
            gate.passed("pdf.page-size", "Page is unrotated US Letter.", f"PDF page {index}")

        check_resources(page.get("/Resources"), index, gate, seen_fonts, seen_resources)
        annots = dereference(page.get("/Annots", []))
        for annot_ref in annots:
            annot = dereference(annot_ref)
            subtype = str(annot.get("/Subtype", ""))
            if subtype == "/Link" or "/A" in annot or "/Dest" in annot:
                gate.fail("pdf.link-annotation", f"Embedded link/action annotation is forbidden ({subtype or 'action'}).", f"PDF page {index}")
            if subtype == "/FileAttachment":
                gate.fail("pdf.attachment", "Embedded file attachment is forbidden.", f"PDF page {index}")
        try:
            extracted_pages.append(page.extract_text() or "")
        except Exception as exc:
            gate.fail("pdf.text-extraction", f"Could not extract text for anonymity/content checks: {exc}", f"PDF page {index}")
            extracted_pages.append("")

    root = dereference(reader.trailer.get("/Root", {}))
    if "/Outlines" in root:
        gate.fail("pdf.bookmarks", "PDF catalog contains outlines/bookmarks.")
    else:
        gate.passed("pdf.bookmarks", "No PDF outline/bookmark tree was found.")
    if "/OpenAction" in root or "/AA" in root:
        gate.fail("pdf.catalog-action", "PDF catalog contains an automatic action.")
    names = dereference(root.get("/Names", {}))
    if any(key in names for key in ("/Dests", "/EmbeddedFiles", "/JavaScript")):
        gate.fail("pdf.named-content", "PDF contains named destinations, embedded files, or JavaScript.")

    metadata = reader.metadata or {}
    sensitive_keys = ("/Title", "/Author", "/Subject", "/Keywords")
    leaked = [(key, str(metadata.get(key, "")).strip()) for key in sensitive_keys if str(metadata.get(key, "")).strip()]
    if leaked:
        for key, value in leaked:
            gate.fail("pdf.metadata", f"Metadata field {key} is not empty: {value!r}.")
    else:
        gate.passed("pdf.metadata", "Title, author, subject, and keyword metadata fields are empty.")

    first_page = extracted_pages[0] if extracted_pages else ""
    if re.search(r"anonymous\s+submission", first_page, re.IGNORECASE):
        gate.passed("pdf.anonymous-marker", "Anonymous-submission marker appears on page 1.")
    else:
        gate.fail("pdf.anonymous-marker", "Page 1 lacks the AAAI anonymous-submission marker; verify submission mode.")

    full_text = "\n".join(extracted_pages)
    if re.search(r"(?im)^\s*acknowledge?ments?\s*$", full_text):
        gate.fail("pdf.acknowledgments", "An acknowledgments heading appears in the review PDF.")
    else:
        gate.passed("pdf.acknowledgments", "No acknowledgments heading was detected in extracted PDF text.")

    if pages > 7:
        gate.manual("references-only", "Inspect pages 8–9 and attest that they contain references exclusively.")
    return pages


def resolve_attestations(gate: Gate, attestations: set[str]) -> None:
    manual_codes = {finding.code for finding in gate.findings if finding.status == "MANUAL"}
    manual_codes |= REQUIRED_ATTESTATIONS
    unknown = attestations - manual_codes
    for code in sorted(unknown):
        gate.fail("attestation.unknown", f"Unknown or inapplicable attestation: {code}.")

    existing_manual = {finding.code: finding for finding in gate.findings if finding.status == "MANUAL"}
    gate.findings = [finding for finding in gate.findings if finding.status != "MANUAL"]
    messages = {
        "layout": "Visually verify margins, gutter, two-column layout, headers/footers/page numbers, and absence of squeezing.",
        "anonymity": "Inspect the PDF and context for author, affiliation, acknowledgment, self-citation, and URL identity leaks.",
        "title-case": "Verify the paper title follows Chicago Title Case.",
        "figures": (
            "Inspect figures at final size: all labels/text are at least 9 pt; captions are below in 10 pt Roman; "
            "raster art is 300 dpi; callouts use Times Roman or Helvetica; fonts are embedded with no Type 3 or "
            "Identity encoding; strokes are at least 0.5 pt; WCAG contrast exceeds 4.5:1; meaning survives "
            "grayscale and does not rely on color; graphics are legible, high resolution, externally cropped, "
            "within margins/gutter, and compliant for non-Roman scripts."
        ),
        "tables": (
            "Inspect tables at final size: text is 10 pt Roman (9 pt minimum only when necessary); captions are "
            "below in 10 pt Roman; no whole-table scaling was used; content is legible and stays within margins/gutter."
        ),
        "checklist-complete": "Verify the separate reproducibility checklist is complete and consistent with the paper.",
        "source-pdf-match": "Verify the supplied TeX source is the source that produced the checked PDF by spot-checking title, structure, figures, and final content.",
    }
    for code in sorted(manual_codes):
        message = existing_manual.get(code, Finding("MANUAL", code, messages.get(code, "Complete this manual gate."))).message
        if code in attestations:
            gate.passed(f"attestation.{code}", f"Attested: {message}")
        else:
            gate.manual(code, message)


def print_report(gate: Gate, as_json: bool) -> int:
    has_fail = any(item.status == "FAIL" for item in gate.findings)
    has_manual = any(item.status == "MANUAL" for item in gate.findings)
    if has_fail:
        overall, exit_code = "FAIL", 1
    elif has_manual:
        overall, exit_code = "MANUAL REVIEW REQUIRED", 3
    else:
        overall, exit_code = "PASS", 0

    if as_json:
        print(json.dumps({"overall": overall, "exit_code": exit_code, "findings": [asdict(item) for item in gate.findings]}, indent=2))
    else:
        print(f"AAAI-27 HARD GATE: {overall}")
        order = {"FAIL": 0, "MANUAL": 1, "PASS": 2}
        for item in sorted(gate.findings, key=lambda value: (order[value.status], value.code, value.location or "")):
            where = f" [{item.location}]" if item.location else ""
            print(f"[{item.status}] {item.code}{where}: {item.message}")
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, type=Path, help="Compiled anonymous review PDF")
    parser.add_argument("--tex", type=Path, help="Main LaTeX source")
    parser.add_argument("--style", type=Path, help="Local aaai2027.sty to hash-check")
    parser.add_argument("--checklist", type=Path, help="Separate completed reproducibility checklist")
    parser.add_argument("--attest", action="append", default=[], choices=sorted(REQUIRED_ATTESTATIONS | OPTIONAL_ATTESTATIONS), help="A manually verified gate; repeat as needed")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    gate = Gate()
    try:
        if not args.pdf.is_file():
            raise FileNotFoundError(f"PDF not found: {args.pdf}")
        if args.tex:
            if not args.tex.is_file():
                raise FileNotFoundError(f"TeX source not found: {args.tex}")
            check_tex(args.tex, args.style, gate)
        else:
            gate.manual("source-review", "No TeX source was supplied; manually verify the source-level Author Kit requirements.")

        if args.checklist is None or not args.checklist.is_file() or args.checklist.stat().st_size == 0:
            gate.fail("checklist.missing", "Supply the separate, non-empty reproducibility checklist with --checklist.")
        else:
            gate.passed("checklist.present", "A separate non-empty reproducibility checklist file is present.", str(args.checklist))

        check_pdf(args.pdf, gate)
        resolve_attestations(gate, set(args.attest))
        return print_report(gate, args.json)
    except (OSError, RuntimeError) as exc:
        if args.json:
            print(json.dumps({"overall": "INPUT OR TOOL ERROR", "exit_code": 2, "error": str(exc)}, indent=2))
        else:
            print(f"AAAI-27 HARD GATE: INPUT OR TOOL ERROR\n{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
