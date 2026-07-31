from ai.decision.models import DecisionResult
from .base import BaseStrategy


class DefaultStrategy(BaseStrategy):

    # ==================================================
    # API Pública
    # ==================================================

    def evaluate(
        self,
        features,
        clip,
        campaign,
    ):

        result = DecisionResult()

        result.strategy = "default"

        result.viral_score = features.virality

        result.retention_score = features.retention

        result.hook_score = features.hook

        result.confidence = features.confidence

        result.campaign_score = features.campaign_score

        result.final_score = self._calculate_score(
            features,
        )

        result.passed = True

        result.reasons.append(
            "Default decision strategy."
        )

        return result

    # ==================================================
    # Score Principal
    # ==================================================

    def _calculate_score(
        self,
        features,
    ):

        emotion_bonus = 5 if features.emotion else 0

        keyword_bonus = min(
            features.keywords,
            5,
        )

        score = (

            features.heuristic * 0.35 +

            features.hook * 0.20 +

            features.llm * 0.20 +

            features.retention * 0.15 +

            features.virality * 0.10 +

            emotion_bonus +

            keyword_bonus

        )

        # ===============================================
        # Hook Intelligence
        # ===============================================

        if features.hook_question:

            score += 2

        if features.hook_curiosity:

            score += 3

        if features.hook_numbers:

            score += 2

        if features.hook_shock:

            score += 2

        # ===============================================
        # Emotion Intelligence
        # ===============================================

        if features.emotion_high:

            score += 4

        elif features.emotion_positive:

            score += 2

        elif features.emotion_negative:

            score += 1

        # ===============================================
        # Confidence
        # ===============================================

        score *= (

            0.75 +

            features.confidence * 0.25

        )

        score = max(
            0,
            min(
                score,
                100,
            ),
        )

        return round(score, 2)