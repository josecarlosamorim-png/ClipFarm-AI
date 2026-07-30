from typing import Tuple


class ScoringRules:

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
        "descobre"
    }

    def score(self, segment: dict) -> Tuple[int, list]:

        score = 0
        reasons = []

        duration = segment["end"] - segment["start"]

        if 20 <= duration <= 45:
            score += 20
            reasons.append("Boa duração")

        words = segment["text"].split()

        if len(words) >= 60:
            score += 20
            reasons.append("Muito conteúdo")

        text = segment["text"].lower()

        if any(word in text for word in self.HOOK_WORDS):
            score += 25
            reasons.append("Hook inicial")

        if "?" in text:
            score += 15
            reasons.append("Pergunta")

        if "!" in text:
            score += 10
            reasons.append("Ênfase")

        return score, reasons
