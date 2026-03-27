#!/usr/bin/env python3
"""Audit images on a page for SEO and GEO compliance.

Extracts all <img> tags, checks alt text quality, file format, lazy loading,
width/height attributes, and estimates file sizes via HEAD requests.

Usage:
    python check-images.py --url https://example.com/page
    python check-images.py --url https://example.com/page --tools tools.json

Output: JSON with per-image analysis and aggregate issues.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from typing import Optional


# ---------------------------------------------------------------------------
# HTML Parser
# ---------------------------------------------------------------------------

class ImageExtractor(HTMLParser):
    """Extract <img> and <picture>/<source> elements."""

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.images: list[dict] = []
        self.has_picture_elements = False
        self._img_index = 0

    def handle_starttag(self, tag: str, attrs):
        attr_dict = {k: v for k, v in attrs}

        if tag == "picture":
            self.has_picture_elements = True

        if tag == "img":
            src = attr_dict.get("src", "")
            if src:
                src = urljoin(self.base_url, src)

            self.images.append({
                "index": self._img_index,
                "src": src,
                "alt": attr_dict.get("alt"),  # None if missing, "" if empty
                "width": attr_dict.get("width"),
                "height": attr_dict.get("height"),
                "loading": attr_dict.get("loading"),
                "srcset": attr_dict.get("srcset"),
            })
            self._img_index += 1


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

KEYWORD_STUFFING_RE = re.compile(r"(\b\w+\b).*\b\1\b.*\b\1\b", re.IGNORECASE)
MODERN_FORMATS = {"webp", "avif", "svg"}
LEGACY_FORMATS = {"jpg", "jpeg", "png", "gif", "bmp", "tiff"}


def get_format_from_url(url: str) -> str:
    """Guess image format from URL extension."""
    path = urlparse(url).path.lower()
    for ext in ["avif", "webp", "svg", "png", "jpg", "jpeg", "gif", "bmp", "tiff"]:
        if path.endswith(f".{ext}"):
            return ext
    return "unknown"


def assess_alt_quality(alt: Optional[str]) -> str:
    """Classify alt text quality."""
    if alt is None:
        return "missing"
    if alt == "":
        return "decorative"  # Intentionally empty
    if len(alt) > 125:
        return "too_long"
    lower = alt.lower()
    if lower in ("image", "photo", "picture", "img", "icon", "logo", "banner"):
        return "generic"
    if KEYWORD_STUFFING_RE.search(alt):
        return "keyword_stuffed"
    return "good"


def estimate_file_size(url: str) -> Optional[int]:
    """HEAD request to get Content-Length in bytes. Returns None on failure."""
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
    try:
        req = Request(url, method="HEAD",
                      headers={"User-Agent": "Mozilla/5.0 (compatible; on-page-sgeo-audit/1.0)"})
        with urlopen(req, timeout=8) as resp:
            cl = resp.headers.get("Content-Length")
            return int(cl) if cl else None
    except (HTTPError, URLError, ValueError, Exception):
        return None


def analyze_images(images: list[dict], check_sizes: bool = True) -> dict:
    issues: list[dict] = []
    analyzed = []

    for i, img in enumerate(images):
        src = img["src"]
        alt = img["alt"]
        fmt = get_format_from_url(src)
        alt_quality = assess_alt_quality(alt)
        has_dimensions = bool(img["width"] and img["height"])
        is_lazy = (img["loading"] or "").lower() == "lazy"
        has_srcset = bool(img["srcset"])

        # Estimate file size for first 10 images
        size_kb: Optional[float] = None
        if check_sizes and i < 10 and src:
            size_bytes = estimate_file_size(src)
            if size_bytes is not None:
                size_kb = round(size_bytes / 1024, 1)

        entry = {
            "src": src,
            "alt": alt if alt is not None else "(missing)",
            "alt_quality": alt_quality,
            "format": fmt,
            "dimensions_set": has_dimensions,
            "lazy_loading": is_lazy,
            "has_srcset": has_srcset,
            "estimated_size_kb": size_kb,
        }
        analyzed.append(entry)

        # Flag issues
        if alt_quality == "missing":
            issues.append({"type": "missing_alt", "src": src})
        elif alt_quality == "keyword_stuffed":
            issues.append({"type": "keyword_stuffed_alt", "src": src, "alt": alt})
        elif alt_quality == "generic":
            issues.append({"type": "generic_alt", "src": src, "alt": alt})
        elif alt_quality == "too_long":
            issues.append({"type": "alt_too_long", "src": src, "length": len(alt or "")})

        if not has_dimensions:
            issues.append({"type": "missing_dimensions", "src": src})

        if fmt in LEGACY_FORMATS and fmt != "svg":
            issues.append({"type": "legacy_format", "src": src, "format": fmt})

        if size_kb is not None and size_kb > 200:
            issues.append({"type": "large_file", "src": src, "size_kb": size_kb})

        # First 2 images should NOT be lazy (likely above fold)
        if i < 2 and is_lazy:
            issues.append({"type": "lazy_above_fold", "src": src,
                           "detail": "First 2 images are likely above the fold — do not lazy load"})

    return {
        "total_images": len(images),
        "images": analyzed,
        "has_picture_elements": False,  # Updated by caller
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_html(url: str) -> str:
    from urllib.request import Request, urlopen
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; on-page-sgeo-audit/1.0)"})
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Audit images on a page for SEO and GEO compliance")
    ap.add_argument("--url", required=True, help="Page URL to analyze")
    ap.add_argument("--tools", default=None, help="Path to tools.json inventory file")
    ap.add_argument("--skip-size-check", action="store_true", help="Skip file size estimation via HEAD")
    args = ap.parse_args()

    try:
        html = fetch_html(args.url)
    except Exception as e:
        print(json.dumps({"error": f"Failed to fetch URL: {e}", "url": args.url}), file=sys.stderr)
        sys.exit(1)

    parser = ImageExtractor(args.url)
    parser.feed(html)

    result = analyze_images(parser.images, check_sizes=not args.skip_size_check)
    result["url"] = args.url
    result["has_picture_elements"] = parser.has_picture_elements
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
