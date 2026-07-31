from .models import ValidationResult


def validate_content(campaign, clip):

    result = ValidationResult()

    transcript = getattr(
        clip,
        "transcript",
        ""
    ).lower()

    for word in campaign.forbidden:

        if word.lower() in transcript:

            result.passed = False

            result.score -= 20

            result.errors.append(
                f"Forbidden content detected: {word}"
            )

    return result