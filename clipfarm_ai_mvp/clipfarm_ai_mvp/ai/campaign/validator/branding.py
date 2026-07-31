from .models import ValidationResult


def validate_branding(campaign, clip) -> ValidationResult:

    result = ValidationResult()

    if campaign.requires_logo:

        has_logo = getattr(clip, "has_logo", False)

        if not has_logo:

            result.passed = False

            result.score -= 40

            result.errors.append(
                "Required logo not detected."
            )

        else:

            result.passed_checks.append(
                "Logo detected."
            )

    return result