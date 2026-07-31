from dataclasses import dataclass, field


@dataclass
class ClipAnalysis:

    # -----------------------------
    # Informação base
    # -----------------------------

    start: float = 0.0
    end: float = 0.0
    duration: float = 0.0

    transcript: str = ""

    language: str = "unknown"

    # -----------------------------
    # Vision
    # -----------------------------

    has_logo: bool = False

    logos: list[str] = field(default_factory=list)

    faces: int = 0

    objects: list[str] = field(default_factory=list)

    ocr_text: str = ""

    # -----------------------------
    # Audio
    # -----------------------------

    has_music: bool = False

    speech_volume: float = 0.0

    silence_ratio: float = 0.0

    # -----------------------------
    # AI
    # -----------------------------

    emotion: str = ""

    keywords: list[str] = field(default_factory=list)

    category: str = ""

    hook: str = ""

    # -----------------------------
    # Campaign
    # -----------------------------

    campaign_score: float = 100

    campaign_errors: list[str] = field(default_factory=list)

    campaign_warnings: list[str] = field(default_factory=list)

    # -----------------------------
    # Viral
    # -----------------------------

    viral_score: float = 0

    heuristic_score: float = 0

    llm_score: float = 0

    retention_score: float = 0

    confidence: float = 0

    # -----------------------------
    # Final
    # -----------------------------

    final_score: float = 0