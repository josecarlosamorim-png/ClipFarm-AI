from .models import ValidationResult


def validate_duration(campaign, clip):

    result = ValidationResult()

    duration = getattr(
        clip,
        "duration",
        0,
    )

    min_duration = getattr(
        campaign,
        "min_duration",
        None,
    )

    max_duration = getattr(
        campaign,
        "max_duration",
        None,
    )

    if min_duration is not None:

        if duration < min_duration:

            result.passed = False

            result.score -= 25

            result.errors.append(
                f"Clip demasiado curto ({duration:.1f}s)"
            )

        else:

            result.passed_checks.append(
                "Minimum duration"
            )

    if max_duration is not None:

        if duration > max_duration:

            result.passed = False

            result.score -= 25

            result.errors.append(
                f"Clip demasiado longo ({duration:.1f}s)"
            )

        else:

            result.passed_checks.append(
                "Maximum duration"
            )

    result.score = max(result.score, 0)

    return result