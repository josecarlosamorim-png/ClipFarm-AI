from pathlib import Path

from core.job import ProcessingJob
from transcription.whisper_engine import WhisperEngine
from video.loader import VideoLoader
from video.scene_detector import SceneDetector
from audio.extractor import AudioExtractor


class Pipeline:

    def __init__(self):

        self.loader = VideoLoader()

        self.detector = SceneDetector()

        self.audio = AudioExtractor()
        
        self.whisper = WhisperEngine()

    def run(self, video: Path):

        job = ProcessingJob(video)

        self.loader.load(job)

        self.detector.detect(job)

        self.audio.extract(job)

        self.whisper.transcribe(job)

        return job
