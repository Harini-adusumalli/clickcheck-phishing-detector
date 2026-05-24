from urllib.parse import urlparse

def extract_features(url):
    # URL length
    length = len(url)

    # number of dots
    dots = url.count(".")

    # https check
    https = 1 if url.startswith("https") else 0

    return [length, dots, https]


# test
if __name__ == "__main__":
    test_url = "https://google.com"
    print(extract_features(test_url))