from core.job import ProcessingJob

from ai.scoring_rules import ScoringRules
from ai.openai_client import OpenAIClient
from ai.hook_detector import HookDetector
from ai.analysis.clip.analyzer import ClipAnalyzer
from core.converters.segment_converter import SegmentConverter
from ai.campaign.validator.validator import CampaignValidator


class ViralScorer:

    TOP_CLIPS = 10

    def __init__(self):

        self.rules = ScoringRules()
        self.llm = OpenAIClient()
        self.hook = HookDetector()
        self.converter = SegmentConverter()
        self.campaign_validator = CampaignValidator()

        self.clip_analyzer = ClipAnalyzer()

    def score(self, job: ProcessingJob):

        scored = []

        for segment in job.segments:

            analysis = self.clip_analyzer.analyze(segment)
            heuristic_score, reasons = self.rules.score(segment)

            hook_score = self.hook.score(
                analysis.transcript[:250]
            )

            llm = self.llm.analyze_segment(segment)

            llm_score = llm.get("score", 50)

            retention = llm.get(
                "retention_score",
                llm_score
            )

            virality = llm.get(
                "virality_score",
                llm_score
            )

            confidence = llm.get(
                "confidence",
                0.6
            )

            # ------------------------
            # Bónus de emoção
            # ------------------------

            emotion_bonus = 0

            if llm.get("emotion"):
                emotion_bonus = 5

            # ------------------------
            # Bónus de keywords
            # ------------------------

            keyword_bonus = min(
                len(llm.get("keywords", [])),
                5
            )

            # ------------------------
            # Fórmula principal
            # ------------------------

            final_score = (

                heuristic_score * 0.35 +

                hook_score * 0.20 +

                llm_score * 0.20 +

                retention * 0.15 +

                virality * 0.10 +

                emotion_bonus +

                keyword_bonus

            )

            # ------------------------
            # Ajuste pela confiança
            # ------------------------

            final_score *= (
                0.75 +
                confidence * 0.25
            )

            final_score = int(
                max(
                    0,
                    min(
                        final_score,
                        100
                    )
                )
            )

            # ------------------------
            # Criar dicionário do clip
            # ------------------------

            clip = {

                **segment,

                "score": final_score,

                "heuristic_score": heuristic_score,

                "hook_score": hook_score,

                "llm_score": llm_score,

                "retention_score": retention,

                "virality_score": virality,

                "title": llm.get("title"),

                "hook": llm.get("hook"),

                "category": llm.get("category"),

                "subcategory": llm.get("subcategory"),

                "emotion": llm.get("emotion"),

                "target_audience": llm.get("target_audience"),

                "keywords": llm.get("keywords", []),

                "confidence": confidence,

                "reason": llm.get("reason"),

                "heuristic_reasons": reasons

            }

            # ------------------------
            # Converter para objeto Clip
            # ------------------------

            clip_obj = self.converter.convert(clip)

            clip_obj.analysis = analysis
            if hasattr(job, "campaign") and job.campaign:

              clip_obj.campaign = self.campaign_validator.validate(
                  job.campaign,
                  clip_obj,
              )
 
            scored.append(clip_obj)

        # ------------------------
        # Ordenar clips
        # ------------------------

        scored.sort(

            key=lambda c: (
                c.score,
                c.retention_score,
                c.virality_score,
                c.confidence,
            ),

            reverse=True

        )

        # ------------------------
        # Remover duplicados
        # ------------------------

        filtered = []

        for clip in scored:

            duplicate = False

            for chosen in filtered:

                overlap = min(
                    clip.end,
                    chosen.end
                ) - max(
                    clip.start,
                    chosen.start
                )

                if overlap <= 0:
                    continue

                shortest = min(
                    clip.duration,
                    chosen.duration
                )

                if shortest > 0:

                    if overlap / shortest > 0.70:

                        duplicate = True
                        break

            if not duplicate:
                filtered.append(clip)

        job.best_clips = filtered[:self.TOP_CLIPS]