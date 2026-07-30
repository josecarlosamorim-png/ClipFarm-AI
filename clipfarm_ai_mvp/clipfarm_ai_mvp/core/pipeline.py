from pathlib import Path
import time

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

    def _step(self, name, func, job):

        print(f"\n========== {name} ==========")

        t0 = time.time()

        func(job)

        print(f"{name} concluído em {time.time()-t0:.2f}s")

        print("--------------------------------")

    def run(self, video: Path):

        job = ProcessingJob(video)

        self._step("Video Loader", self.loader.load, job)

        self._step("Scene Detection", self.detector.detect, job)
        print("Scenes:", len(job.scenes))

        self._step("Audio Extraction", self.audio.extract, job)

        self._step("Whisper", self.whisper.transcribe, job)

        print("Transcript:", len(job.transcript))

        self._step(
            "Segment Extractor",
            self.segment_extractor.extract,
            job
        )

        print("Segments:", len(job.segments))

        self._step("Viral Scorer", self.viral.score, job)


        print("Best clips:", len(job.best_clips))

        self._step(
            "Clip Generator",
            self.clip_generator.generate,
            job
        )

        self._step(
            "Subtitle Generator",
            self.subtitle_generator.generate,
            job
        )

        print("\n===== PIPELINE TERMINADA =====")


        print("Best clips:", len(job.best_clips))

        self._step(
            "Clip Generator",
            self.clip_generator.generate,
            job
        )

        self._step(
            "Subtitle Generator",
            self.subtitle_generator.generate,
            job
        )

        print("\n===== PIPELINE TERMINADA =====")

        return job