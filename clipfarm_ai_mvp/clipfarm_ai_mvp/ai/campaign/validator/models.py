from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    passed: bool = True

    score: float = 100.0

    errors: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    passed_checks: list[str] = field(default_factory=list)