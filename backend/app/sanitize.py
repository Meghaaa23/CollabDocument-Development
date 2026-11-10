"""HTML sanitization.

Document content is rich-text HTML produced by TipTap in the browser. Because
the client is never trusted, every piece of HTML that enters the system -- from
the editor *and* from uploaded files -- is run through an allow-list sanitizer
before it is stored. This prevents stored-XSS (e.g. a <script> smuggled inside
an uploaded .docx) while preserving the formatting the editor actually uses.
"""
import bleach

# Tags TipTap emits for the formatting features we support.
ALLOWED_TAGS = [
    "p", "br", "strong", "b", "em", "i", "u", "s",
    "h1", "h2", "h3",
    "ul", "ol", "li",
    "blockquote", "code", "pre", "hr",
    "a",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
}

# Only safe URL schemes may appear in links.
ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


def sanitize_html(html: str) -> str:
    """Return a safe subset of the given HTML."""
    if not html:
        return ""
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
