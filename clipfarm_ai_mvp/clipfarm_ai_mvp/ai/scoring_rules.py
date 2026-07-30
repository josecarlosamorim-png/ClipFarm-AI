import re
from typing import Tuple


class ScoringRules:

    HOOK_WORDS = {
        "imagina", "sabias", "segredo", "erro", "nunca",
        "atenção", "porque", "como", "verdade",
        "descobre", "wait", "listen", "warning",
        "top", "best", "crazy", "insane"
    }

    EMOTION_WORDS = {
        "incrível", "inacreditável", "fantástico",
        "impossível", "ridículo", "melhor",
        "pior", "chocante", "assustador",
        "insano", "surpreendente"
    }

    STORY_WORDS = {
        "um dia",
        "aconteceu",
        "de repente",
        "então",
        "mas",
        "até que",
        "no entanto"
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

    CURIOSITY_WORDS = {
        "ninguém",
        "segredo",
        "descobre",
        "porque",
        "como",
        "verdade",
        "erro",
        "nunca"
    }

    def score(self, segment: dict) -> Tuple[int, list]:

        reasons = []

        score = 0

        text = segment["text"]

        lower = text.lower()

        duration = segment["duration"]

        words = text.split()

        word_count = len(words)

        # ---------------------------------
        # Duração
        # ---------------------------------

        if 22 <= duration <= 38:

            score += 18

            reasons.append("Boa duração")

        elif 18 <= duration <= 45:

            score += 12

        # ---------------------------------
        # Densidade
        # ---------------------------------

        density = word_count / max(duration, 1)

        if 2 <= density <= 4:

            score += 15

            reasons.append("Boa densidade")

        elif density > 4:

            score += 8

        # ---------------------------------
        # Conteúdo
        # ---------------------------------

        if word_count >= 90:

            score += 18

            reasons.append("Muito conteúdo")

        elif word_count >= 60:

            score += 12

        elif word_count < 20:

            score -= 12

            reasons.append("Pouco conteúdo")

        # ---------------------------------
        # Hooks
        # ---------------------------------

        hooks = sum(

            word in lower

            for word in self.HOOK_WORDS

        )

        score += min(hooks * 5, 20)

        if hooks:

            reasons.append("Hook")

        # ---------------------------------
        # Curiosidade
        # ---------------------------------

        curiosity = sum(

            word in lower

            for word in self.CURIOSITY_WORDS

        )

        score += curiosity * 4

        if curiosity:

            reasons.append("Curiosity Gap")

        # ---------------------------------
        # Storytelling
        # ---------------------------------

        story = sum(

            word in lower

            for word in self.STORY_WORDS

        )

        score += story * 5

        if story:

            reasons.append("Storytelling")

        # ---------------------------------
        # Emoção
        # ---------------------------------

        emotion = sum(

            word in lower

            for word in self.EMOTION_WORDS

        )

        score += emotion * 5

        if emotion:

            reasons.append("Emoção")

        # ---------------------------------
        # CTA
        # ---------------------------------

        if any(

            word in lower

            for word in self.CTA_WORDS

        ):

            score += 8

            reasons.append("CTA")

        # ---------------------------------
        # Perguntas
        # ---------------------------------

        questions = text.count("?")

        score += min(

            questions * 5,

            10

        )

        if questions:

            reasons.append("Pergunta")

        # ---------------------------------
        # Exclamações
        # ---------------------------------

        exclamations = text.count("!")

        score += min(

            exclamations * 3,

            9

        )

        # ---------------------------------
        # Números
        # ---------------------------------

        if re.search(r"\d+", text):

            score += 5

            reasons.append("Números")

        # ---------------------------------
        # Finalização
        # ---------------------------------

        if score >= 80:

            reasons.append("Elevado potencial viral")

        score = max(

            0,

            min(

                score,

                100

            )

        )

        return score, reasons
