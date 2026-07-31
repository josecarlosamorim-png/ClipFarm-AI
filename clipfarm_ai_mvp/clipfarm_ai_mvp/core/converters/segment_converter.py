from core.entities.clip import Clip


class SegmentConverter:

    def convert(
        self,
        segment: dict,
    ) -> Clip:

        return Clip(

            start=segment["start"],
            end=segment["end"],
            duration=segment["duration"],
            transcript=segment["text"],

            score=segment.get("score", 0),

            heuristic_score=segment.get("heuristic_score", 0),
            hook_score=segment.get("hook_score", 0),
            llm_score=segment.get("llm_score", 0),

            retention_score=segment.get("retention_score", 0),
            virality_score=segment.get("virality_score", 0),

            confidence=segment.get("confidence", 0),

            title=segment.get("title", ""),
            hook=segment.get("hook", ""),
            category=segment.get("category", ""),
            subcategory=segment.get("subcategory", ""),
            emotion=segment.get("emotion", ""),
            target_audience=segment.get("target_audience", ""),

            keywords=segment.get("keywords", []),

            reason=segment.get("reason", ""),

            heuristic_reasons=segment.get(
                "heuristic_reasons",
                [],
            ),
        )