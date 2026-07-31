from .models import ClipAnalysis


class TranscriptAnalyzer:

    def analyze(
        self,
        segment: dict,
    ) -> ClipAnalysis:

        analysis = ClipAnalysis()

        analysis.start = segment["start"]

        analysis.end = segment["end"]

        analysis.duration = segment["duration"]

        analysis.transcript = segment["text"]

        return analysis