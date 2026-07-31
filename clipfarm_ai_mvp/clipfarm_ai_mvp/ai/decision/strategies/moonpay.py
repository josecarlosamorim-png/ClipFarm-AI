from .default import DefaultStrategy


class MoonPayStrategy(DefaultStrategy):

    def evaluate(
        self,
        clip,
        campaign,
    ):

        result = super().evaluate(
            clip,
            campaign,
        )

        result.strategy = "moonpay"

        if clip.campaign:

            result.campaign_score = clip.campaign.score

            result.passed = clip.campaign.passed

            result.final_score = (

                result.final_score * 0.70 +

                clip.campaign.score * 0.30

            )

            if not clip.campaign.passed:

                result.final_score *= 0.50

                result.reasons.append(

                    "Campaign validation failed."

                )

        return result