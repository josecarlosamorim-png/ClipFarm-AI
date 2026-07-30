from pathlib import Path
import time

from core.job import ProcessingJob
from core.logger import logger

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

    def _execute_step(
        self,
        job: ProcessingJob,
        name: str,
        progress: int,
        func,
    ):

        logger.info("=" * 60)
        logger.info(name)

        job.current_stage = name
        job.progress = progress
        job.status = "running"

        start = time.time()

        try:

            func(job)

            elapsed = time.time() - start

            logger.info(
                "%s concluído em %.2fs",
                name,
                elapsed
            )

            job.add_log(
                f"{name} ({elapsed:.2f}s)"
            )

        except Exception as e:

            logger.exception(e)

            job.add_error(
                f"{name}: {str(e)}"
            )

            raise

    def run(self, video: Path):

        job = ProcessingJob(video_path=video)

        logger.info("")
        logger.info("========== NOVO PROCESSAMENTO ==========")
        logger.info(video)

        self._execute_step(
            job,
            "Video Loader",
            5,
            self.loader.load,
        )

        self._execute_step(
            job,
            "Scene Detection",
            15,
            self.detector.detect,
        )

        logger.info(
            "Scenes: %d",
            len(job.scenes)
        )

        self._execute_step(
            job,
            "Audio Extraction",
            25,
            self.audio.extract,
        )

        self._execute_step(
            job,
            "Whisper",
            45,
            self.whisper.transcribe,
        )

        logger.info(
            "Transcript: %d",
            len(job.transcript)
        )

        self._execute_step(
            job,
            "Segment Extractor",
            60,
            self.segment_extractor.extract,
        )

        logger.info(
            "Segments: %d",
            len(job.segments)
        )

        self._execute_step(
            job,
            "Viral Scorer",
            75,
            self.viral.score,
        )

        logger.info(
            "Best Clips: %d",
            len(job.best_clips)
        )

        self._execute_step(
            job,
            "Clip Generator",
            90,
            self.clip_generator.generate,
        )

        self._execute_step(
            job,
            "Subtitle Generator",
            98,
            self.subtitle_generator.generate,
        )

        job.finish()

        logger.info("")
        logger.info("===== PIPELINE TERMINADA =====")
        logger.info("Tempo total: %.2fs", job.elapsed_time)
        logger.info("Clips gerados: %d", len(job.generated_clips))

        return job