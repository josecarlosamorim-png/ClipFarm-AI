from pathlib import Path

from core.job import ProcessingJob

from video.loader import VideoLoader
from video.scene_detector import SceneDetector
from video.clip_generator import ClipGenerator

from audio.extractor import AudioExtractor

from transcription.whisper_engine import WhisperEngine

from subtitle.generator import SubtitleGenerator

from ai.segment_extractor import SegmentExtractor
from ai.viral_scorer import ViralScorer


class Pipeline:

    def __init__(self):

        self.loader = VideoLoader()

        self.detector = SceneDetector()

        self.audio = AudioExtractor()

        self.whisper = WhisperEngine()

        self.segment_extractor = SegmentExtractor()

        self.viral = ViralScorer()

        self.clip_generator = ClipGenerator()

        self.subtitle_generator = SubtitleGenerator()

    def run(self, video: Path):

        job = ProcessingJob(video)

        self.loader.load(job)

        self.detector.detect(job)

        self.audio.extract(job)

        self.whisper.transcribe(job)

        self.segment_extractor.extract(job)

        self.viral.score(job)

        self.clip_generator.generate(job)

        self.subtitle_generator.generate(job)

        return job
