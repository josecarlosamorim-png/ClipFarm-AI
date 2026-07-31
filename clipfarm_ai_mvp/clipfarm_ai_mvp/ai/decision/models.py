from dataclasses import dataclass, field


@dataclass
class DecisionResult:
    """
    Resultado final da decisão para um clip.
    """

    final_score: float = 0

    viral_score: float = 0
    campaign_score: float = 0

    retention_score: float = 0
    vision_score: float = 0
    audio_score: float = 0

    confidence: float = 0

    passed_campaign: bool = True

    reasons: list[str] = field(default_factory=list)