from core.entities.clip import Clip


class RankingEngine:

    def rank(
        self,
        clips: list[Clip],
        top_n: int = 10,
    ) -> list[Clip]:

        ranked = sorted(

            clips,

            key=lambda clip: (

                clip.decision.final_score,

                clip.decision.campaign_score,

                clip.retention_score,

                clip.confidence,

            ),

            reverse=True,

        )

        return ranked[:top_n]