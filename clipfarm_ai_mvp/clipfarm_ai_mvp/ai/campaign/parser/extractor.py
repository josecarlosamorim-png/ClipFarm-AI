import re

from .models import Campaign

from .rules.platforms import extract_platforms
from .rules.branding import (
    extract_brand,
    requires_logo,
    extract_logo_seconds,
)


class RuleExtractor:

    def extract(self, text: str):

        campaign = Campaign()

        lower = text.lower()

        # -----------------------
        # Branding
        # -----------------------

        campaign.name = extract_brand(text)

        campaign.requires_logo = requires_logo(text)

        campaign.logo_first_seconds = extract_logo_seconds(
            text
        )

        # -----------------------
        # Platforms
        # -----------------------

        campaign.platforms = extract_platforms(text)

        # -----------------------
        # Preferred content
        # -----------------------

        preferred = []

        keywords = [
            "wins",
            "big tricks",
            "happy moments",
            "high scores",
        ]

        for word in keywords:

            if word in lower:
                preferred.append(word)

        campaign.preferred = preferred

        # -----------------------
        # Forbidden content
        # -----------------------

        forbidden = []

        words = [
            "falls",
            "injuries",
            "betting",
            "trading",
            "odds",
            "crashes",
        ]

        for word in words:

            if word in lower:
                forbidden.append(word)

        campaign.forbidden = forbidden

        return campaign