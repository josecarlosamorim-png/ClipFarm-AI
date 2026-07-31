from dataclasses import dataclass, field


@dataclass
class DecisionResult:

    # -----------------------------
    # Resultado Final
    # -----------------------------

    passed: bool = True

    final_score: float = 0.0

    confidence: float = 0.0

    priority: int = 0

    # -----------------------------
    # Scores individuais
    # -----------------------------

    campaign_score: float = 0.0

    viral_score: float = 0.0

    retention_score: float = 0.0

    branding_score: float = 0.0

    engagement_score: float = 0.0

    hook_score: float = 0.0

    # -----------------------------
    # Informação
    # -----------------------------

    strategy: str = ""

    reasons: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)