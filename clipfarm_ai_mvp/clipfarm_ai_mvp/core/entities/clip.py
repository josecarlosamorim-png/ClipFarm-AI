from dataclasses import dataclass, field

from ai.analysis.clip.models import ClipAnalysis
from ai.decision.models import DecisionResult
from ai.campaign.validator.models import ValidationResult


@dataclass
class Clip:

    # -----------------------------
    # Informação temporal
    # -----------------------------

    start: float

    end: float

    duration: float

    transcript: str

    # -----------------------------
    # Score principal
    # -----------------------------

    score: float = 0

    # -----------------------------
    # Scores internos
    # -----------------------------

    heuristic_score: float = 0

    hook_score: float = 0

    llm_score: float = 0

    retention_score: float = 0

    virality_score: float = 0

    confidence: float = 0

    # -----------------------------
    # Informação IA
    # -----------------------------

    title: str = ""

    hook: str = ""

    category: str = ""

    subcategory: str = ""

    emotion: str = ""

    target_audience: str = ""

    keywords: list[str] = field(default_factory=list)

    reason: str = ""

    heuristic_reasons: list[str] = field(default_factory=list)

    # -----------------------------
    # Análise completa
    # -----------------------------

    analysis: ClipAnalysis = field(
        default_factory=ClipAnalysis
    )
    

    # -----------------------------
    # Validação da campanha
    # -----------------------------

    campaign: ValidationResult = field(
        default_factory=ValidationResult
    )

    # -----------------------------
    # Decisão Final
    # -----------------------------

    decision: DecisionResult = field(
    default_factory=DecisionResult
    )