from ai.decision.features.extractor import FeatureExtractor

from ai.decision.strategies.default import DefaultStrategy
from ai.decision.strategies.moonpay import MoonPayStrategy
from ai.decision.strategies.redbull import RedBullStrategy
from ai.decision.strategies.spotify import SpotifyStrategy


class DecisionEngine:

    def __init__(self):

        self.extractor = FeatureExtractor()

        self.strategies = {

            "default": DefaultStrategy(),

            "moonpay": MoonPayStrategy(),

            "redbull": RedBullStrategy(),

            "spotify": SpotifyStrategy(),

        }

    def evaluate(
        self,
        clip,
        campaign=None,
    ):

        strategy = self._get_strategy(campaign)

        features = self.extractor.extract(
            clip,
        )

        decision = strategy.evaluate(
            features,
            clip,
            campaign,
        )

        clip.decision = decision

        return decision

    def _get_strategy(
        self,
        campaign,
    ):

        if campaign is None:

            return self.strategies["default"]

        name = campaign.name.lower()

        return self.strategies.get(
            name,
            self.strategies["default"],
        )