from ai.decision.models import DecisionResult
from ai.decision.weights import (
    VIRAL_WEIGHT,
    CAMPAIGN_WEIGHT,
    RETENTION_WEIGHT,
    VISION_WEIGHT,
    AUDIO_WEIGHT,
)


class DecisionEngine:

    def evaluate(
        self,
        clip,
        campaign_result=None,
    ) -> DecisionResult:

        result = DecisionResult()

        # ------------------------
        # Viralidade
        # ------------------------

        result.viral_score = clip.score

        # ------------------------
        # Retenção
        # ------------------------

        result.retention_score = clip.retention_score

        # ------------------------
        # Vision
        # ------------------------

        if clip.analysis:

            result.vision_score = clip.analysis.campaign_score

            result.audio_score = clip.analysis.audio_score

        # ------------------------
        # Campanha
        # ------------------------

        if campaign_result:

            result.campaign_score = campaign_result.score

            result.passed_campaign = campaign_result.passed

            result.reasons.extend(
                campaign_result.reasons
            )

        else:

            result.campaign_score = 50

        # ------------------------
        # Score Final
        # ------------------------

        result.final_score = (

            result.viral_score * VIRAL_WEIGHT +

            result.campaign_score * CAMPAIGN_WEIGHT +

            result.retention_score * RETENTION_WEIGHT +

            result.vision_score * VISION_WEIGHT +

            result.audio_score * AUDIO_WEIGHT

        )

        # ------------------------
        # Confiança
        # ------------------------

        result.confidence = clip.confidence

        return result