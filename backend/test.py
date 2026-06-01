from feature_extraction import extract_features, is_suspicious

urls = [
    "https://google.com",
    "http://192.168.1.1/login",
    "https://secure-bank-verify-login.com",
    "http://paypal-login-update.xyz"
]

for url in urls:
    features = extract_features(url)
    result = is_suspicious(features)

    print("\nURL:", url)
    print("Result:", result)
    print(features)