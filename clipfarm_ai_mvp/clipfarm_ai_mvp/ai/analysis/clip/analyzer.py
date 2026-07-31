from .transcript import TranscriptAnalyzer

from .vision import VisionAnalyzer

from .audio import AudioAnalyzer


class ClipAnalyzer:

    def __init__(self):

        self.transcript = TranscriptAnalyzer()

        self.vision = VisionAnalyzer()

        self.audio = AudioAnalyzer()

    def analyze(
        self,
        segment: dict,
    ):

        analysis = self.transcript.analyze(segment)

        analysis = self.vision.analyze(analysis)

        analysis = self.audio.analyze(analysis)

        return analysis