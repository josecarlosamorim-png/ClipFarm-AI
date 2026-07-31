from .models import ValidationResult


def merge_results(results):

    final = ValidationResult()

    final.score = 100

    for result in results:

        final.score = min(
            final.score,
            result.score
        )

        final.errors.extend(result.errors)

        final.warnings.extend(result.warnings)

        final.passed_checks.extend(
            result.passed_checks
        )

        if not result.passed:
            final.passed = False

    return final