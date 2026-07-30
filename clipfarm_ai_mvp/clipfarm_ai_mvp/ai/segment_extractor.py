from core.job import ProcessingJob


class SegmentExtractor:
    """
    Cria vários segmentos candidatos a clips virais.

    Estratégia:

    - Junta frases consecutivas
    - Respeita duração mínima e máxima
    - Gera janelas deslizantes (sliding windows)
    - Evita segmentos demasiado pequenos
    """

    MIN_DURATION = 15
    MAX_DURATION = 45

    WINDOW_STEP = 5

    def extract(self, job: ProcessingJob):

        transcript = job.transcript

        if not transcript:
            job.segments = []
            return

        segments = []

        n = len(transcript)

        for start_idx in range(n):

            start = transcript[start_idx]["start"]

            text = ""
            end = start

            for end_idx in range(start_idx, n):

                sentence = transcript[end_idx]

                end = sentence["end"]

                duration = end - start

                if duration > self.MAX_DURATION:
                    break

                if text:
                    text += " "

                text += sentence["text"]

                if duration >= self.MIN_DURATION:

                    segments.append({

                        "start": start,

                        "end": end,

                        "duration": duration,

                        "text": text,

                        "num_sentences": end_idx - start_idx + 1

                    })

            # Sliding Window
            if start_idx + self.WINDOW_STEP >= n:
                continue

        # Remover duplicados

        unique = []

        seen = set()

        for segment in segments:

            key = (

                round(segment["start"], 1),

                round(segment["end"], 1)

            )

            if key in seen:
                continue

            seen.add(key)

            unique.append(segment)

        unique.sort(

            key=lambda s: (

                s["start"],

                s["end"]

            )

        )

        job.segments = unique