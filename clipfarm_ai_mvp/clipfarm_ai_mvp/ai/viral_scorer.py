from core.job import ProcessingJob

from ai.scoring_rules import ScoringRules
from ai.openai_client import OpenAIClient
from ai.hook_detector import HookDetector


class ViralScorer:

    TOP_CLIPS = 10

    def __init__(self):

        self.rules = ScoringRules()
        self.llm = OpenAIClient()
        self.hook = HookDetector()

    def score(self, job: ProcessingJob):

        scored_clips = []

        for segment in job.segments:

            # -----------------------------
            # Score heurístico
            # -----------------------------

            heuristic_score, reasons = self.rules.score(segment)

            # -----------------------------
            # Hook Score
            # -----------------------------

            hook_score = self.hook.score(
                segment["text"][:200]
            )

            # -----------------------------
            # Score LLM
            # -----------------------------

            llm_result = self.llm.analyze_segment(segment)

            llm_score = llm_result.get("score", 0)

            # -----------------------------
            # Score Final
            # -----------------------------

            final_score = int(

                heuristic_score * 0.55 +

                hook_score * 0.25 +

                llm_score * 0.20

            )

            final_score = max(0, min(100, final_score))

            clip = {

                **segment,

                "score": final_score,

                "heuristic_score": heuristic_score,

                "hook_score": hook_score,

                "llm_score": llm_score,

                "title": llm_result.get(
                    "title",
                    "Untitled"
                ),

                "category": llm_result.get(
                    "category",
                    "General"
                ),

                "confidence": llm_result.get(
                    "confidence",
                    0
                ),

                "reason": llm_result.get(
                    "reason",
                    ""
                ),

                "heuristic_reasons": reasons

            }

            scored_clips.append(clip)

        # ------------------------------------
        # Ordenação
        # ------------------------------------

        scored_clips.sort(

            key=lambda clip: (

                clip["score"],

                clip["confidence"],

                clip["duration"]

            ),

            reverse=True

        )

        # ------------------------------------
        # Remover clips quase iguais
        # ------------------------------------

        filtered = []

        for clip in scored_clips:

            duplicated = False

            for chosen in filtered:

                overlap = min(

                    clip["end"],

                    chosen["end"]

                ) - max(

                    clip["start"],

                    chosen["start"]

                )

                if overlap <= 0:
                    continue

                shortest = min(

                    clip["duration"],

                    chosen["duration"]

                )

                if shortest > 0 and overlap / shortest > 0.70:

                    duplicated = True
                    break

            if not duplicated:

                filtered.append(clip)

        job.best_clips = filtered[:self.TOP_CLIPS]