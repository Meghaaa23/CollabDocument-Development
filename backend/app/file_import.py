"""Turn an uploaded file into editable rich-text HTML.

Supported types (stated clearly in the UI + README):
    .txt  -> paragraphs, newline-preserving
    .md   -> rendered Markdown (headings, bold, lists, etc.)
    .docx -> converted with mammoth, preserving headings/bold/italic/lists

Everything returned here is still passed through the sanitizer by the caller,
so even a malicious .docx cannot inject active content.
"""
import io
from html import escape

import mammoth
import markdown as md

SUPPORTED_EXTENSIONS = {".txt", ".md", ".markdown", ".docx"}


class UnsupportedFileType(ValueError):
    pass


def _ext(filename: str) -> str:
    dot = filename.rfind(".")
    return filename[dot:].lower() if dot != -1 else ""


def _txt_to_html(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    paragraphs = text.split("\n\n")
    html_parts = []
    for para in paragraphs:
        para = para.strip("\n")
        if not para.strip():
            continue
        # Preserve single newlines inside a paragraph as <br>.
        html_parts.append("<p>" + escape(para).replace("\n", "<br>") + "</p>")
    return "".join(html_parts) or "<p></p>"


def _md_to_html(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    return md.markdown(text, extensions=["extra", "sane_lists"])


def _docx_to_html(raw: bytes) -> str:
    result = mammoth.convert_to_html(io.BytesIO(raw))
    return result.value or "<p></p>"


def import_file(filename: str, raw: bytes) -> tuple[str, str]:
    """Return (suggested_title, html_body) for a supported upload.

    Raises UnsupportedFileType for anything outside SUPPORTED_EXTENSIONS.
    """
    ext = _ext(filename)
    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileType(
            f"Unsupported file type '{ext or 'unknown'}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if ext == ".txt":
        body = _txt_to_html(raw)
    elif ext in (".md", ".markdown"):
        body = _md_to_html(raw)
    else:  # .docx
        body = _docx_to_html(raw)

    # Suggested title = filename without extension.
    base = filename[: filename.rfind(".")] if "." in filename else filename
    title = base.strip() or "Imported document"
    return title[:255], body
