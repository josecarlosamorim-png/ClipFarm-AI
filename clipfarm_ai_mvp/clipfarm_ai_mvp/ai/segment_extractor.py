from core.job import ProcessingJob


class SegmentExtractor:

    MIN_DURATION = 15
    MAX_DURATION = 45

    HOOKS = {

        "imagine",
        "imagina",
        "sabias",
        "nunca",
        "porque",
        "erro",
        "segredo",
        "atenção",
        "listen",
        "wait",
        "top",
        "best"

    }

    def process(self, job: ProcessingJob):

        transcript = job.transcript

        segments = []

        current = []

        start = None

        for sentence in transcript:

            if start is None:

                start = sentence["start"]

            current.append(sentence)

            duration = sentence["end"] - start

            score = self._segment_score(current)

            should_close = False

            if duration >= self.MAX_DURATION:

                should_close = True

            elif duration >= self.MIN_DURATION and score >= 40:

                should_close = True

            if should_close:

                segments.append(

                    self._build_segment(current)

                )

                current = []

                start = None

        if current:

            segments.append(

                self._build_segment(current)

            )

        job.segments = segments

    # ---------------------------------------

    def _segment_score(self, current):

        score = 0

        text = " ".join(

            s["text"]

            for s in current

        ).lower()

        if any(

            h in text

            for h in self.HOOKS

        ):

            score += 20

        score += text.count("?") * 5

        score += text.count("!") * 3

        score += min(

            len(text.split()) // 10,

            20

        )

        return score

    # ---------------------------------------

    def _build_segment(self, sentences):

        text = " ".join(

            s["text"]

            for s in sentences

        )

        return {

            "start": sentences[0]["start"],

            "end": sentences[-1]["end"],

            "duration": sentences[-1]["end"] - sentences[0]["start"],

            "text": text,

            "sentences": sentences

        }