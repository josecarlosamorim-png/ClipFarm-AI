import re


KNOWN_BRANDS = [
    "MoonPay",
    "Red Bull",
    "Nike",
    "Adidas",
    "Puma",
    "Monster",
    "Monster Energy",
    "X Games",
]


def extract_brand(text: str) -> str:
    """
    Procura automaticamente a marca principal
    da campanha.
    """

    lower = text.lower()

    for brand in KNOWN_BRANDS:

        if brand.lower() in lower:
            return brand

    return ""


def requires_logo(text: str) -> bool:

    return "logo" in text.lower()


def extract_logo_seconds(text: str):

    match = re.search(
        r"first\s+(\d+)\s+seconds",
        text.lower()
    )

    if match:
        return int(match.group(1))

    return None