from core.job import ProcessingJob


class SegmentExtractor:

    MIN_DURATION = 15      # segundos
    MAX_DURATION = 45      # segundos
    PAUSE_THRESHOLD = 1.5  # pausa entre frases


    def extract(self, job: ProcessingJob):

        transcript = job.transcript

        if not transcript:
            job.segments = []
            return

        segments = []

        current = {
            "start": transcript[0]["start"],
            "end": transcript[0]["end"],
            "text": transcript[0]["text"]
        }

        for sentence in transcript[1:]:

            pause = sentence["start"] - current["end"]
            duration = current["end"] - current["start"]

            if (
                pause > self.PAUSE_THRESHOLD
                or duration >= self.MAX_DURATION
            ):

                if duration >= self.MIN_DURATION:
                    segments.append(current)

                current = {
                    "start": sentence["start"],
                    "end": sentence["end"],
                    "text": sentence["text"]
                }

            else:

                current["end"] = sentence["end"]
                current["text"] += " " + sentence["text"]

        duration = current["end"] - current["start"]

        if duration >= self.MIN_DURATION:
            segments.append(current)

        job.segments = segments
