from core.job import ProcessingJob


class ViralScorer:

    def score(self, job: ProcessingJob):

        scored_segments = []

        for segment in job.segments:

            score = 0
            reasons = []

            duration = segment["end"] - segment["start"]

            # Duração ideal
            if 20 <= duration <= 45:
                score += 20
                reasons.append("Boa duração")

            # Texto suficientemente longo
            words = segment["text"].split()

            if len(words) > 50:
                score += 20
                reasons.append("Conteúdo rico")

            # Hook inicial
            hook_words = [
                "imagina",
                "sabias",
                "nunca",
                "erro",
                "segredo",
                "atenção",
                "porque",
                "como"
            ]

            text = segment["text"].lower()

            if any(word in text for word in hook_words):
                score += 30
                reasons.append("Possível hook")

            # Perguntas prendem atenção
            if "?" in segment["text"]:
                score += 15
                reasons.append("Pergunta")

            # Exclamações
            if "!" in segment["text"]:
                score += 15
                reasons.append("Ênfase")

            scored_segments.append({

                "start": segment["start"],

                "end": segment["end"],

                "text": segment["text"],

                "score": score,

                "reasons": reasons

            })

        scored_segments.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        job.best_clips = scored_segments
