#!/usr/bin/env python3
"""
check-https-security.py — Verify HTTPS implementation, redirect chains, HSTS, and mixed content.

Checks that a site serves over HTTPS, HTTP properly redirects, HSTS header is
configured, and no mixed content patterns exist in the HTML.

Usage:
    python3 check-https-security.py --domain example.com
    python3 check-https-security.py --domain example.com --check-pages /about /pricing

AI Agent Usage:
    Agents should use WebFetch to:
    1. Fetch http://domain.com and follow redirects — verify it reaches https://
    2. Check response headers for Strict-Transport-Security
    3. Scan HTML for http:// resource URLs (mixed content)
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import ssl
import re


def follow_redirects(url, max_hops=10):
    """Follow redirects manually, recording each hop. Returns (chain, final_url, final_status, error)."""
    chain = []
    current_url = url

    for i in range(max_hops):
        try:
            # Use a custom opener that does NOT follow redirects
            class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return None

            opener = urllib.request.build_opener(NoRedirectHandler)
            req = urllib.request.Request(current_url)
            req.add_header("User-Agent", "check-https-security/1.0")

            try:
                response = opener.open(req, timeout=10)
                status = response.getcode()
                chain.append({"url": current_url, "status": status})
                return chain, current_url, status, None
            except urllib.error.HTTPError as e:
                if e.code in (301, 302, 303, 307, 308):
                    location = e.headers.get("Location", "")
                    if not location:
                        chain.append({"url": current_url, "status": e.code, "error": "Redirect with no Location header"})
                        return chain, current_url, e.code, "Redirect with no Location header"

                    # Handle relative redirects
                    if location.startswith("/"):
                        from urllib.parse import urlparse
                        parsed = urlparse(current_url)
                        location = f"{parsed.scheme}://{parsed.netloc}{location}"

                    chain.append({"url": current_url, "status": e.code, "location": location})
                    current_url = location
                else:
                    chain.append({"url": current_url, "status": e.code})
                    return chain, current_url, e.code, None
        except Exception as e:
            chain.append({"url": current_url, "error": str(e)})
            return chain, current_url, None, str(e)

    return chain, current_url, None, "Too many redirects (>10)"


def check_hsts(domain):
    """Check HSTS header on the HTTPS version of the domain."""
    url = f"https://{domain}/"
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "check-https-security/1.0")
        response = urllib.request.urlopen(req, timeout=10)
        hsts = response.headers.get("Strict-Transport-Security", "")

        if not hsts:
            return {"present": False, "recommendation": "Add Strict-Transport-Security header with max-age=31536000; includeSubDomains"}

        result = {"present": True, "value": hsts}

        # Parse max-age
        max_age_match = re.search(r"max-age=(\d+)", hsts)
        if max_age_match:
            max_age = int(max_age_match.group(1))
            result["max_age"] = max_age
            if max_age < 31536000:
                result["max_age_sufficient"] = False
                result["recommendation"] = f"max-age is {max_age} ({max_age // 86400} days). Increase to 31536000 (1 year)."
            else:
                result["max_age_sufficient"] = True

        result["include_subdomains"] = "includesubdomains" in hsts.lower()
        result["preload"] = "preload" in hsts.lower()

        return result
    except Exception as e:
        return {"present": False, "error": str(e)}


def check_ssl_certificate(domain):
    """Basic SSL certificate check."""
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(ssl.socket.socket(), server_hostname=domain) as sock:
            sock.settimeout(10)
            sock.connect((domain, 443))
            cert = sock.getpeercert()

            # Extract basic info
            subject = dict(x[0] for x in cert.get("subject", ()))
            issuer = dict(x[0] for x in cert.get("issuer", ()))
            not_after = cert.get("notAfter", "")

            return {
                "valid": True,
                "subject_cn": subject.get("commonName", ""),
                "issuer": issuer.get("organizationName", ""),
                "expires": not_after,
            }
    except ssl.SSLCertVerificationError as e:
        return {"valid": False, "error": f"Certificate verification failed: {str(e)}"}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def check_mixed_content(domain, pages=None):
    """Scan pages for mixed content patterns (http:// resources on https:// pages)."""
    if not pages:
        pages = ["/"]

    mixed_content = []

    for page in pages:
        url = f"https://{domain}{page}"
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "Mozilla/5.0 (compatible; check-https-security/1.0)")
            response = urllib.request.urlopen(req, timeout=15)
            html = response.read().decode("utf-8", errors="replace")

            # Find http:// URLs in resource tags (not in text content or comments)
            # Check script src, link href, img src, iframe src
            patterns = [
                (r'<script[^>]*\ssrc=["\']http://', "script"),
                (r'<link[^>]*\shref=["\']http://', "stylesheet/link"),
                (r'<img[^>]*\ssrc=["\']http://', "image"),
                (r'<iframe[^>]*\ssrc=["\']http://', "iframe"),
                (r'<video[^>]*\ssrc=["\']http://', "video"),
                (r'<audio[^>]*\ssrc=["\']http://', "audio"),
            ]

            for pattern, resource_type in patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    mixed_content.append({
                        "page": page,
                        "type": resource_type,
                        "count": len(matches),
                    })

        except Exception as e:
            mixed_content.append({"page": page, "error": str(e)})

    return mixed_content


def main():
    parser = argparse.ArgumentParser(
        description="Verify HTTPS implementation, redirect chains, HSTS header, and mixed content.",
        epilog="Output: JSON report with HTTPS status, redirect chain, HSTS config, and mixed content findings."
    )
    parser.add_argument("--domain", required=True, help="Domain to check (e.g., example.com)")
    parser.add_argument("--check-pages", nargs="*", default=["/"],
                        help="Pages to scan for mixed content (default: /)")
    parser.add_argument("--tools", help="Path to tools.json from inventory-tools.py")
    args = parser.parse_args()

    domain = args.domain.replace("https://", "").replace("http://", "").rstrip("/")

    # Check HTTP to HTTPS redirect
    http_url = f"http://{domain}/"
    redirect_chain, final_url, final_status, redirect_error = follow_redirects(http_url)

    https_redirect = final_url.startswith("https://") if final_url else False

    # Check HSTS
    hsts = check_hsts(domain)

    # Check SSL certificate
    certificate = check_ssl_certificate(domain)

    # Check mixed content
    mixed = check_mixed_content(domain, args.check_pages)

    # Build recommendations
    recommendations = []
    if not https_redirect:
        recommendations.append("HTTP does not redirect to HTTPS. Add a 301 redirect from http:// to https://.")
    if len(redirect_chain) > 3:
        recommendations.append(f"Redirect chain has {len(redirect_chain)} hops. Reduce to a single 301 redirect.")
    if not hsts.get("present"):
        recommendations.append("Add HSTS header: Strict-Transport-Security: max-age=31536000; includeSubDomains")
    elif not hsts.get("max_age_sufficient", True):
        recommendations.append(hsts.get("recommendation", ""))
    if not certificate.get("valid"):
        recommendations.append(f"SSL certificate issue: {certificate.get('error', 'unknown')}")
    if mixed:
        mixed_count = sum(m.get("count", 0) for m in mixed if "count" in m)
        if mixed_count > 0:
            recommendations.append(f"Found {mixed_count} mixed content resource(s). Update http:// URLs to https://.")

    result = {
        "domain": domain,
        "https": https_redirect,
        "redirect_chain": redirect_chain,
        "hsts": hsts,
        "certificate": certificate,
        "mixed_content": mixed,
        "mixed_content_found": any(m.get("count", 0) > 0 for m in mixed),
        "recommendations": recommendations,
        "overall_status": "pass" if (https_redirect and hsts.get("present") and certificate.get("valid") and not any(m.get("count", 0) > 0 for m in mixed)) else "needs_work",
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
