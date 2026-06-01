import re
from urllib.parse import urlparse

def extract_features(url):
    try:
        if not url or not isinstance(url, str):
            return [0]*16

        parsed = urlparse(url)

        # 1. URL STRUCTURE
        length = len(url)
        num_dots = url.count(".")
        has_https = 1 if url.startswith("https") else 0
        num_subdomains = max(len(parsed.netloc.split(".")) - 2, 0) if parsed.netloc else 0
        num_slashes = url.count("/")
        num_hyphens = url.count("-")

        # 2. KEYWORDS
        has_login = 1 if "login" in url.lower() else 0
        has_verify = 1 if "verify" in url.lower() else 0
        has_bank = 1 if "bank" in url.lower() else 0
        has_secure = 1 if "secure" in url.lower() else 0
        has_update = 1 if "update" in url.lower() else 0

        # 3. SECURITY
        has_ip_address = 1 if re.match(r"^\d+\.\d+\.\d+\.\d+$", parsed.netloc) else 0
        has_at_symbol = 1 if "@" in url else 0
        has_special_chars = 1 if any(c in url for c in ["%", "?", "="]) else 0

        # 4. BEHAVIOR
        has_redirect = 1 if url.count("//") > 1 else 0
        is_http_not_https = 1 if url.startswith("http://") else 0

        features = [
            length, #0
            num_dots,#1
            has_https,#2
            num_subdomains,#3
            num_slashes,#4
            num_hyphens,#5
            has_login,#6
            has_verify,#7
            has_bank,#8
            has_secure,#9
            has_update,#10
            has_ip_address,#11
            has_at_symbol,#12
            has_special_chars,#13
            has_redirect,#14
            is_http_not_https#15
        ]
        
        # safety check
        if len(features) != 16:
            return [0]*16

        return features

    except Exception as e:
        print("Error processing URL:", url)
        return [0]*16
    
    



def is_suspicious(features):
    score = (
        features[6] + features[7] + features[8] +
        features[9] + features[11] + features[12] + features[15]
    )

    return ("suspicious", score) if score >= 2 else ("safe", score)