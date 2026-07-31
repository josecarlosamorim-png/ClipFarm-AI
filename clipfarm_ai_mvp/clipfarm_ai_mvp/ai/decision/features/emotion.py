class EmotionFeature:

    POSITIVE = {

        "happy",
        "joy",
        "fun",
        "excited",
        "love",

        "feliz",
        "alegre",
        "divertido",
        "amor",

    }

    NEGATIVE = {

        "sad",
        "angry",
        "fear",
        "cry",

        "triste",
        "raiva",
        "medo",

    }

    HIGH_INTENSITY = {

        "shock",
        "surprise",
        "rage",
        "ecstatic",

        "choque",
        "surpresa",
        "euforia",

    }

    def extract(
        self,
        clip,
    ):

        emotion = (
            clip.emotion or ""
        ).lower()

        return {

            "emotion": bool(emotion),

            "emotion_label": emotion,

            "emotion_positive": emotion in self.POSITIVE,

            "emotion_negative": emotion in self.NEGATIVE,

            "emotion_high": emotion in self.HIGH_INTENSITY,

            "emotion_intensity": self._intensity(
                emotion
            ),

        }

    def _intensity(
        self,
        emotion,
    ):

        if emotion in self.HIGH_INTENSITY:

            return 1.0

        if emotion:

            return 0.7

        return 0.0