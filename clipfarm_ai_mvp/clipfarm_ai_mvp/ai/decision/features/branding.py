from dataclasses import dataclass


@dataclass
class DecisionFeatures:

    heuristic: float = 0

    hook: float = 0

    llm: float = 0

    retention: float = 0

    virality: float = 0

    confidence: float = 0

    branding: float = 0

    engagement: float = 0

    campaign_score: float = 0

    emotion: bool = False

    keywords: int = 0