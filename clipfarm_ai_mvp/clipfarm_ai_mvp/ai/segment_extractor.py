from core.job import ProcessingJob


class SegmentExtractor:

    MIN_DURATION = 20
    TARGET_DURATION = 30
    MAX_DURATION = 40

    HOOK_WORDS = {
        "imagina",
        "imagine",
        "sabias",
        "segredo",
        "erro",
        "atenção",
        "espera",
        "wait",
        "listen",
        "porque",
        "como",
        "why",
        "how",
        "top",
        "best",
        "viral",
        "nunca"
    }

    END_MARKERS = {
        ".",
        "!",
        "?"
    }

    def extract(self, job: ProcessingJob):

        transcript = job.transcript
        scenes = job.scenes

        if not transcript:
            job.segments = []
            return

        segments = []

        current = []
        start = None

        for sentence in transcript:

            if start is None:
                start = sentence["start"]

            current.append(sentence)

            duration = sentence["end"] - start

            score = self._segment_score(
                current,
                scenes
            )

            close = False

            if duration >= self.MAX_DURATION:

                close = True

            elif duration >= self.MIN_DURATION:

                if score >= 45:
                    close = True

            if close:

                segments.append(

                    self._build_segment(current)

                )

                current = []
                start = None

        if current:

            if segments:

                last = self._build_segment(current)

                if last["duration"] < 10:

                    previous = segments.pop()

                    merged = previous["sentences"] + last["sentences"]

                    segments.append(

                        self._build_segment(merged)

                    )

                else:

                    segments.append(last)

            else:

                segments.append(

                    self._build_segment(current)

                )

        job.segments = segments

    # ---------------------------------------------------

    def _segment_score(self, sentences, scenes):

        score = 0

        text = " ".join(
            s["text"]
            for s in sentences
        ).lower()

        start = sentences[0]["start"]
        end = sentences[-1]["end"]

        duration = end - start

        # ------------------------
        # Duração ideal
        # ------------------------

        if 25 <= duration <= 35:
            score += 20

        elif 20 <= duration <= 40:
            score += 15

        # ------------------------
        # Densidade
        # ------------------------

        words = len(text.split())

        score += min(words // 8, 20)

        # ------------------------
        # Hooks
        # ------------------------

        hooks = sum(

            word in text

            for word in self.HOOK_WORDS

        )

        score += hooks * 8

        # ------------------------
        # Perguntas
        # ------------------------

        score += min(
            text.count("?") * 5,
            15
        )

        # ------------------------
        # Exclamações
        # ------------------------

        score += min(
            text.count("!") * 3,
            9
        )

        # ------------------------
        # Mudança de cena
        # ------------------------

        for scene in scenes:

            if start <= scene <= end:

                score += 8

                break

        # ------------------------
        # Final de frase
        # ------------------------

        if text.strip():

            if text.strip()[-1] in self.END_MARKERS:

                score += 10

        return score

    # ---------------------------------------------------

    def _build_segment(self, sentences):

        text = " ".join(

            s["text"]

            for s in sentences

        )

        start = sentences[0]["start"]
        end = sentences[-1]["end"]

        return {

            "start": start,

            "end": end,

            "duration": end - start,

            "text": text,

            "sentences": sentences

        }