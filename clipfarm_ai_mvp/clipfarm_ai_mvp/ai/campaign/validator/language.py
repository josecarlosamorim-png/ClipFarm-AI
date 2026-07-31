from .models import ValidationResult


def validate_language(campaign, clip):

    result = ValidationResult()

    expected = getattr(
        campaign,
        "language",
        None,
    )

    detected = getattr(
        clip.analysis,
        "language",
        None,
    )

    if expected is None:

        return result

    if detected is None:

        result.warnings.append(
            "Idioma não detetado"
        )

        result.score -= 5

        return result

    if detected.lower() != expected.lower():

        result.passed = False

        result.score -= 20

        result.errors.append(
            f"Idioma '{detected}' diferente de '{expected}'"
        )

    else:

        result.passed_checks.append(
            "Language"
        )

    result.score = max(result.score, 0)

    return result