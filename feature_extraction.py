import re
from urllib.parse import urlparse


# Suspicious words commonly associated with phishing URLs
SUSPICIOUS_WORDS = [
    "login",
    "signin",
    "verify",
    "verification",
    "secure",
    "security",
    "account",
    "update",
    "password",
    "confirm",
    "bank",
    "wallet",
    "paypal",
    "payment",
    "invoice",
    "free",
    "bonus",
    "winner",
    "prize",
    "recover",
    "unlock",
    "suspend",
    "alert"
]


# Common URL shortening services
SHORTENING_SERVICES = [
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "t.co",
    "ow.ly",
    "is.gd",
    "buff.ly"
]


def extract_features(url):

    features = {}

    # Parse URL
    parsed_url = urlparse(url)

    hostname = parsed_url.hostname or ""
    path = parsed_url.path or ""
    query = parsed_url.query or ""

    url_lower = url.lower()
    hostname_lower = hostname.lower()

    # -------------------------------------------------
    # 1. URL Length
    # -------------------------------------------------

    features["url_length"] = len(url)

    # -------------------------------------------------
    # 2. Domain Length
    # -------------------------------------------------

    features["domain_length"] = len(hostname)

    # -------------------------------------------------
    # 3. Path Length
    # -------------------------------------------------

    features["path_length"] = len(path)

    # -------------------------------------------------
    # 4. Query Length
    # -------------------------------------------------

    features["query_length"] = len(query)

    # -------------------------------------------------
    # 5. Number of dots
    # -------------------------------------------------

    features["dot_count"] = url.count(".")

    # -------------------------------------------------
    # 6. Number of hyphens
    # -------------------------------------------------

    features["hyphen_count"] = url.count("-")

    # -------------------------------------------------
    # 7. Number of underscores
    # -------------------------------------------------

    features["underscore_count"] = url.count("_")

    # -------------------------------------------------
    # 8. Number of @ symbols
    # -------------------------------------------------

    features["at_count"] = url.count("@")

    # -------------------------------------------------
    # 9. Number of question marks
    # -------------------------------------------------

    features["question_count"] = url.count("?")

    # -------------------------------------------------
    # 10. Number of equal signs
    # -------------------------------------------------

    features["equal_count"] = url.count("=")

    # -------------------------------------------------
    # 11. Number of slash characters
    # -------------------------------------------------

    features["slash_count"] = url.count("/")

    # -------------------------------------------------
    # 12. Number of colon characters
    # -------------------------------------------------

    features["colon_count"] = url.count(":")

    # -------------------------------------------------
    # 13. Number of semicolons
    # -------------------------------------------------

    features["semicolon_count"] = url.count(";")

    # -------------------------------------------------
    # 14. Number of ampersands
    # -------------------------------------------------

    features["ampersand_count"] = url.count("&")

    # -------------------------------------------------
    # 15. Number of percent symbols
    # -------------------------------------------------

    features["percent_count"] = url.count("%")

    # -------------------------------------------------
    # 16. Number of digits
    # -------------------------------------------------

    features["digit_count"] = sum(
        character.isdigit()
        for character in url
    )

    # -------------------------------------------------
    # 17. Number of special characters
    # -------------------------------------------------

    features["special_char_count"] = len(
        re.findall(r"[^a-zA-Z0-9]", url)
    )

    # -------------------------------------------------
    # 18. HTTPS
    # -------------------------------------------------

    features["https"] = int(
        parsed_url.scheme.lower() == "https"
    )

    # -------------------------------------------------
    # 19. IP address detection
    # -------------------------------------------------

    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"

    features["has_ip"] = int(
        re.search(ip_pattern, hostname) is not None
    )

    # -------------------------------------------------
    # 20. Suspicious words
    # -------------------------------------------------

    features["suspicious_words"] = sum(
        word in url_lower
        for word in SUSPICIOUS_WORDS
    )

    # -------------------------------------------------
    # 21. URL shortening service
    # -------------------------------------------------

    features["shortened_url"] = int(
        any(
            service in hostname_lower
            for service in SHORTENING_SERVICES
        )
    )

    # -------------------------------------------------
    # 22. Number of subdomains
    # -------------------------------------------------

    parts = hostname.split(".")

    if len(parts) > 2:
        features["subdomain_count"] = len(parts) - 2
    else:
        features["subdomain_count"] = 0

    # -------------------------------------------------
    # 23. Suspicious domain words
    # -------------------------------------------------

    suspicious_domain_words = [
        "login",
        "verify",
        "secure",
        "account",
        "bank",
        "paypal",
        "payment"
    ]

    features["suspicious_domain"] = sum(
        word in hostname_lower
        for word in suspicious_domain_words
    )

    # -------------------------------------------------
    # 24. Number of URL parameters
    # -------------------------------------------------

    if query:
        features["parameter_count"] = len(
            query.split("&")
        )
    else:
        features["parameter_count"] = 0

    return features