import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def extract_features(url):
    try:
        if not url or not isinstance(url, str):
            return [0] * 23

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

        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")

            web_is_live = 1 if response.status_code == 200 else 0

            web_forms_count = len(soup.find_all("form"))

            web_password_fields = len(
                soup.find_all("input", {"type": "password"})
            )

            web_has_login = (
                1 if (
                    web_password_fields > 0
                    or "login" in response.text.lower()
                ) else 0
            )

            web_ssl_valid = 1 if url.startswith("https://") else 0

        except Exception:
            web_is_live = 0
            web_forms_count = 0
            web_password_fields = 0
            web_has_login = 0
            web_ssl_valid = 0
        web_security_score = 0

        if web_is_live:
            web_security_score += 1

        if web_ssl_valid:
            web_security_score += 1

        if web_password_fields == 0:
            web_security_score += 1

        if not has_ip_address:
            web_security_score += 1

        features = [
    web_is_live,
    web_security_score,
    web_forms_count,
    web_password_fields,
    web_has_login,
    web_ssl_valid,

    length,
    url.count("@"),
    url.count("?"),
    url.count("-"),
    url.count("="),
    url.count("."),
    url.count("#"),
    url.count("%"),
    url.count("+"),
    url.count("$"),

    num_subdomains,
    has_verify,
    has_bank,
    has_secure,
    has_update,
    has_ip_address,
    has_redirect
]
        
        # safety check
        if len(features) != 23:
            return [0] * 23

        return features

    except Exception as e:
        print("Error processing URL:", url)
        return [0] * 23
    
    



def is_suspicious(features):
    score = (
        features[6] + features[7] + features[8] +
        features[9] + features[11] + features[12] + features[15]
    )

    return ("suspicious", score) if score >= 2 else ("safe", score)

if __name__ == "__main__":
    url = input("Enter URL: ")

    features = extract_features(url)

    print("Length:", len(features))
    print(features)