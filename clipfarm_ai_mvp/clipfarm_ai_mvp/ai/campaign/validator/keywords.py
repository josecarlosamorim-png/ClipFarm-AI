from .models import ValidationResult


def validate_keywords(campaign, clip):

    result = ValidationResult()

    transcript = getattr(
        clip,
        "transcript",
        ""
    ).lower()

    for word in campaign.required_keywords:

        if word.lower() not in transcript:

            result.score -= 5

            result.warnings.append(
                f"Missing keyword: {word}"
            )

    return result