from dataclasses import dataclass


@dataclass
class DecisionFeatures:

    # =====================================================
    # Scores Base
    # =====================================================

    heuristic: float = 0.0

    hook: float = 0.0

    llm: float = 0.0

    retention: float = 0.0

    virality: float = 0.0

    confidence: float = 0.0

    campaign_score: float = 0.0

    # =====================================================
    # Hook
    # =====================================================

    hook_strength: float = 0.0

    hook_question: bool = False

    hook_numbers: bool = False

    hook_curiosity: bool = False

    hook_shock: bool = False

    # =====================================================
    # Emotion
    # =====================================================

    emotion: bool = False

    emotion_label: str = ""

    emotion_positive: bool = False

    emotion_negative: bool = False

    emotion_high: bool = False

    emotion_intensity: float = 0.0

    # =====================================================
    # Engagement
    # =====================================================

    engagement: float = 0.0

    action: float = 0.0

    humor: float = 0.0

    energy: float = 0.0

    # =====================================================
    # Branding
    # =====================================================

    branding: float = 0.0

    logo_detected: bool = False

    sponsor_detected: bool = False

    cta_detected: bool = False

    # =====================================================
    # Narrative
    # =====================================================

    narrative: float = 0.0

    has_beginning: bool = False

    has_conflict: bool = False

    has_climax: bool = False

    has_resolution: bool = False

    # =====================================================
    # Quality
    # =====================================================

    quality: float = 0.0

    audio_quality: float = 0.0

    video_quality: float = 0.0

    subtitle_quality: float = 0.0

    # =====================================================
    # Keywords
    # =====================================================

    keywords: int = 0