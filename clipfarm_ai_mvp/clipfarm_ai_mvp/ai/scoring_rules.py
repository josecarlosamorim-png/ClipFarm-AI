import re
from typing import Tuple


class ScoringRules:
    """
    Sistema heurístico de pontuação.

    Score máximo: 100

    O objetivo é encontrar segmentos com elevado potencial
    para TikTok, Reels e Shorts.
    """

    HOOK_WORDS = {

        "imagina",
        "sabias",
        "segredo",
        "erro",
        "nunca",
        "atenção",
        "porque",
        "como",
        "verdade",
        "descobre",
        "wait",
        "listen",
        "warning",
        "top",
        "best",
        "crazy",
        "insane"

    }

    EMOTION_WORDS = {

        "incrível",
        "inacreditável",
        "impossível",
        "fantástico",
        "chocante",
        "amedrontador",
        "ridículo",
        "perfeito",
        "melhor",
        "pior"

    }

    CTA_WORDS = {

        "segue",
        "follow",
        "subscribe",
        "partilha",
        "share",
        "comenta",
        "like"

    }

    def score(self, segment: dict) -> Tuple[int, list]:

        score = 0

        reasons = []

        text = segment["text"]

        text_lower = text.lower()

        duration = segment["end"] - segment["start"]

        # --------------------------
        # Duração
        # --------------------------

        if 20 <= duration <= 40:

            score += 20
            reasons.append("Boa duração")

        elif 15 <= duration <= 50:

            score += 12
            reasons.append("Duração aceitável")

        # --------------------------
        # Número de palavras
        # --------------------------

        words = text.split()

        word_count = len(words)

        if word_count >= 80:

            score += 20
            reasons.append("Muito conteúdo")

        elif word_count >= 50:

            score += 15
            reasons.append("Boa quantidade de fala")

        elif word_count >= 30:

            score += 8

        # --------------------------
        # Hook
        # --------------------------

        if any(word in text_lower for word in self.HOOK_WORDS):

            score += 20

            reasons.append("Hook")

        # --------------------------
        # Emoção
        # --------------------------

        emotion_hits = sum(

            word in text_lower

            for word in self.EMOTION_WORDS

        )

        score += emotion_hits * 5

        if emotion_hits:

            reasons.append("Palavras emocionais")

        # --------------------------
        # Call To Action
        # --------------------------

        if any(word in text_lower for word in self.CTA_WORDS):

            score += 8

            reasons.append("Call To Action")

        # --------------------------
        # Perguntas
        # --------------------------

        questions = text.count("?")

        score += min(

            questions * 5,

            10

        )

        if questions:

            reasons.append("Pergunta")

        # --------------------------
        # Exclamações
        # --------------------------

        exclamations = text.count("!")

        score += min(

            exclamations * 3,

            9

        )

        if exclamations:

            reasons.append("Ênfase")

        # --------------------------
        # Números
        # --------------------------

        numbers = re.findall(

            r"\d+",

            text

        )

        if numbers:

            score += 5

            reasons.append("Números")

        # --------------------------
        # Frases longas
        # --------------------------

        average_length = (

            word_count /

            max(

                text.count("."),

                1

            )

        )

        if average_length > 12:

            score += 5

            reasons.append("Boa densidade")

        # --------------------------
        # Limites
        # --------------------------

        score = max(

            0,

            min(

                score,

                100

            )

        )

        return score, reasons
