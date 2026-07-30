from core.job import ProcessingJob

from ai.scoring_rules import ScoringRules


class ViralScorer:

    def __init__(self):

        self.rules = ScoringRules()

    def score(self, job: ProcessingJob):

        clips = []

        for segment in job.segments:

            score, reasons = self.rules.score(segment)

            clips.append({

                **segment,

                "score": score,

                "reasons": reasons,

                "title": None,

                "category": None,

                "confidence": None

            })

        clips.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        job.best_clips = clips
