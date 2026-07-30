from core.job import ProcessingJob

from ai.scoring_rules import ScoringRules
from ai.openai_client import OpenAIClient


class ViralScorer:

    def __init__(self):

        self.rules = ScoringRules()
        self.llm = OpenAIClient()

    def score(self, job: ProcessingJob):

        clips = []

        for segment in job.segments:

            # Pontuação heurística
            heuristic_score, reasons = self.rules.score(segment)

            # Análise do LLM (atualmente simulada)
            llm_result = self.llm.analyze_segment(segment)

            # Combinação das pontuações
            final_score = int(
                heuristic_score * 0.4 +
                llm_result["score"] * 0.6
            )

            clips.append({

                **segment,

                "score": final_score,

                "heuristic_score": heuristic_score,

                "llm_score": llm_result["score"],

                "title": llm_result["title"],

                "category": llm_result["category"],

                "confidence": llm_result["confidence"],

                "reason": llm_result["reason"],

                "reasons": reasons

            })

        clips.sort(
            key=lambda clip: clip["score"],
            reverse=True
        )

        job.best_clips = clips
