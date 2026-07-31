PLATFORMS = [
    ("youtube shorts", "YouTube Shorts"),
    ("instagram", "Instagram"),
    ("tik tok", "TikTok"),
    ("tiktok", "TikTok"),
    ("facebook", "Facebook"),
    ("linkedin", "LinkedIn"),
    ("snapchat", "Snapchat"),
    ("twitter", "X"),
    ("x.com", "X"),
    ("youtube", "YouTube"),
]


def extract_platforms(text: str) -> list[str]:
    """
    Extrai automaticamente as plataformas mencionadas
    num Campaign Brief.

    Evita duplicados e garante que 'YouTube Shorts'
    não gera também 'YouTube'.
    """

    lower = text.lower()

    found = []

    for keyword, platform in PLATFORMS:

        if keyword not in lower:
            continue

        # evita adicionar YouTube quando já existe YouTube Shorts
        if (
            platform == "YouTube"
            and "YouTube Shorts" in found
        ):
            continue

        if platform not in found:
            found.append(platform)

    return found