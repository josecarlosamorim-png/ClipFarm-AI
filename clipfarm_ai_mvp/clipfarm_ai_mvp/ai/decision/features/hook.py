class HookFeature:

    QUESTION_WORDS = {

        "what",
        "why",
        "how",
        "when",
        "who",
        "where",

        "como",
        "porque",
        "porquê",
        "quando",
        "quem",
        "qual",
        "quais",

    }

    SHOCK_WORDS = {

        "impossible",
        "insane",
        "crazy",
        "unbelievable",
        "secret",
        "never",
        "worst",
        "best",

        "impossível",
        "insano",
        "louco",
        "segredo",
        "nunca",
        "melhor",
        "pior",

    }

    def extract(
        self,
        clip,
    ):

        transcript = (
            clip.transcript or ""
        ).lower()

        words = transcript.split()

        return {

            "hook": clip.hook_score,

            "hook_strength": clip.hook_score,

            "hook_question": self._has_question(
                transcript,
                words,
            ),

            "hook_numbers": self._has_numbers(
                transcript,
            ),

            "hook_curiosity": self._has_curiosity(
                transcript,
            ),

            "hook_shock": self._has_shock(
                words,
            ),

        }

    def _has_question(
        self,
        transcript,
        words,
    ):

        if "?" in transcript:

            return True

        if not words:

            return False

        return words[0] in self.QUESTION_WORDS

    def _has_numbers(
        self,
        transcript,
    ):

        return any(
            c.isdigit()
            for c in transcript
        )

    def _has_curiosity(
        self,
        transcript,
    ):

        triggers = [

            "wait",

            "watch",

            "until",

            "don't",

            "before",

            "espera",

            "vê",

            "antes",

            "não",

        ]

        transcript = transcript.lower()

        return any(

            t in transcript

            for t in triggers

        )

    def _has_shock(
        self,
        words,
    ):

        return any(

            w in self.SHOCK_WORDS

            for w in words

        )