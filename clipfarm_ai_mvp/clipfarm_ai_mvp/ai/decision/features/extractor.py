from .models import DecisionFeatures

from .hook import HookFeature
from .emotion import EmotionFeature


class FeatureExtractor:

    def __init__(self):

        self.hook = HookFeature()

        self.emotion = EmotionFeature()

    def extract(
        self,
        clip,
    ):

        features = DecisionFeatures()

        # ==================================================
        # Scores Base
        # ==================================================

        features.heuristic = clip.heuristic_score

        features.llm = clip.llm_score

        features.retention = clip.retention_score

        features.virality = clip.virality_score

        features.confidence = clip.confidence

        features.keywords = len(
            clip.keywords
        )

        # ==================================================
        # Campaign
        # ==================================================

        if clip.campaign:

            features.campaign_score = (
                clip.campaign.score
            )

        # ==================================================
        # Hook Feature
        # ==================================================

        hook = self.hook.extract(
            clip
        )

        features.hook = hook["hook"]

        features.hook_strength = hook[
            "hook_strength"
        ]

        features.hook_question = hook[
            "hook_question"
        ]

        features.hook_numbers = hook[
            "hook_numbers"
        ]

        features.hook_curiosity = hook[
            "hook_curiosity"
        ]

        features.hook_shock = hook[
            "hook_shock"
        ]

        # ==================================================
        # Emotion Feature
        # ==================================================

        emotion = self.emotion.extract(
            clip
        )

        features.emotion = emotion[
            "emotion"
        ]

        features.emotion_label = emotion[
            "emotion_label"
        ]

        features.emotion_positive = emotion[
            "emotion_positive"
        ]

        features.emotion_negative = emotion[
            "emotion_negative"
        ]

        features.emotion_high = emotion[
            "emotion_high"
        ]

        features.emotion_intensity = emotion[
            "emotion_intensity"
        ]

        return features