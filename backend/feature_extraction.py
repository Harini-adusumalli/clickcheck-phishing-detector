import re
from urllib.parse import urlparse


def extract_features(url):
    parsed = urlparse(url)

    # ================================
    # 1. URL STRUCTURE FEATURES
    # ================================
    length = len(url)
    num_dots = url.count(".")
    has_https = 1 if url.startswith("https") else 0
    num_subdomains = len(parsed.netloc.split(".")) - 2 if parsed.netloc else 0
    num_slashes = url.count("/")
    num_hyphens = url.count("-")

    # ================================
    # 2. SUSPICIOUS KEYWORDS
    # ================================
    has_login = 1 if "login" in url.lower() else 0
    has_verify = 1 if "verify" in url.lower() else 0
    has_bank = 1 if "bank" in url.lower() else 0
    has_secure = 1 if "secure" in url.lower() else 0
    has_update = 1 if "update" in url.lower() else 0

    # ================================
    # 3. SECURITY FEATURES
    # ================================
    has_ip_address = 1 if re.match(r"\d+\.\d+\.\d+\.\d+", parsed.netloc) else 0
    has_at_symbol = 1 if "@" in url else 0
    has_special_chars = 1 if any(c in url for c in ["%", "?", "="]) else 0

    # ================================
    # 4. BEHAVIOR FEATURES
    # ================================
    has_redirect = 1 if url.count("//") > 1 else 0
    is_http_not_https = 1 if url.startswith("http://") else 0

    # ================================
    # FINAL FEATURE VECTOR (ORDER IMPORTANT)
    # ================================
    return [
        length,
        num_dots,
        has_https,
        num_subdomains,
        num_slashes,
        num_hyphens,
        has_login,
        has_verify,
        has_bank,
        has_secure,
        has_update,
        has_ip_address,
        has_at_symbol,
        has_special_chars,
        has_redirect,
        is_http_not_https
    ]

