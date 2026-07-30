import re


class HookDetector:

    QUESTIONS = {
        "porque",
        "porquê",
        "como",
        "what",
        "why",
        "how",
        "quando",
        "quem"
    }

    HOOK_WORDS = {

        "imagina",
        "sabias",
        "segredo",
        "erro",

        "ninguém",

        "nunca",

        "atenção",

        "espera",

        "wait",

        "listen",

        "stop",

        "warning",

        "crazy",

        "insane",

        "viral"

    }

    NUMBERS = re.compile(r"\d+")

    def score(self, text):

        score = 0

        t = text.lower()

        if any(w in t for w in self.HOOK_WORDS):
            score += 35

        if any(q in t for q in self.QUESTIONS):
            score += 20

        if self.NUMBERS.search(t):
            score += 15

        score += min(
            text.count("!"),
            3
        ) * 5

        score += min(
            text.count("?"),
            2
        ) * 10

        if len(text.split()) < 12:
            score += 10

        return min(score, 100)