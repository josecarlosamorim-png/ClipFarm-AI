import re


class HookDetector:

    QUESTIONS = {
        "porque",
        "porquê",
        "como",
        "qual",
        "quem",
        "quando",
        "what",
        "why",
        "how",
        "who",
        "when"
    }

    HOOK_WORDS = {

        "imagina",
        "sabias",
        "segredo",
        "erro",
        "nunca",
        "atenção",
        "espera",
        "stop",
        "wait",
        "listen",
        "warning",
        "viral",
        "chocante",
        "incrível",
        "impossível",
        "ridículo",
        "insano",
        "crazy",
        "insane",
        "truth",
        "verdade"
    }

    CTA_WORDS = {

        "segue",
        "follow",
        "subscribe",
        "partilha",
        "share",
        "comenta",
        "comment",
        "like"
    }

    STORY_WORDS = {

        "um dia",
        "aconteceu",
        "história",
        "story",
        "de repente",
        "então",
        "mas"
    }

    CONTRAST_WORDS = {

        "mas",

        "porém",

        "no entanto",

        "however",

        "instead",

        "excepto"

    }

    LIST_PATTERN = re.compile(

        r"\b(\d+)\s+(formas|razões|erros|dicas|ways|reasons|tips)\b",

        re.IGNORECASE

    )

    NUMBER_PATTERN = re.compile(r"\d+")

    MONEY_PATTERN = re.compile(r"[€$£]\s?\d+")

    PERCENT_PATTERN = re.compile(r"\d+\s?%")

    def score(self, text):

        text = text.strip()

        lower = text.lower()

        score = 0

        # ---------------------
        # Hook words
        # ---------------------

        hits = sum(

            word in lower

            for word in self.HOOK_WORDS

        )

        score += min(hits * 10, 35)

        # ---------------------
        # Perguntas
        # ---------------------

        if any(

            q in lower

            for q in self.QUESTIONS

        ):

            score += 15

        score += min(

            text.count("?") * 5,

            10

        )

        # ---------------------
        # Storytelling
        # ---------------------

        story_hits = sum(

            s in lower

            for s in self.STORY_WORDS

        )

        score += story_hits * 6

        # ---------------------
        # Contraste
        # ---------------------

        if any(

            c in lower

            for c in self.CONTRAST_WORDS

        ):

            score += 8

        # ---------------------
        # CTA
        # ---------------------

        if any(

            c in lower

            for c in self.CTA_WORDS

        ):

            score += 8

        # ---------------------
        # Listas
        # ---------------------

        if self.LIST_PATTERN.search(lower):

            score += 15

        # ---------------------
        # Valores
        # ---------------------

        if self.NUMBER_PATTERN.search(lower):

            score += 8

        if self.PERCENT_PATTERN.search(lower):

            score += 8

        if self.MONEY_PATTERN.search(lower):

            score += 10

        # ---------------------
        # Exclamações
        # ---------------------

        score += min(

            text.count("!") * 3,

            9

        )

        # ---------------------
        # Frases curtas
        # ---------------------

        words = len(text.split())

        if 8 <= words <= 20:

            score += 10

        elif words < 8:

            score += 5

        # ---------------------
        # Primeiras palavras
        # ---------------------

        first = lower.split()[:4]

        if any(

            w in first

            for w in {

                "imagina",

                "sabias",

                "espera",

                "wait",

                "stop",

                "listen"

            }

        ):

            score += 12

        return max(

            0,

            min(

                score,

                100

            )

        )