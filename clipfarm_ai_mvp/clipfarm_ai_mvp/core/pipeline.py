from pathlib import Path

from core.job import ProcessingJob

from video.loader import VideoLoader
from video.scene_detector import SceneDetector
from video.clip_generator import ClipGenerator

from audio.extractor import AudioExtractor

from transcription.whisper_engine import WhisperEngine

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

    def run(self, video: Path):

        job = ProcessingJob(video)

        # 1. Carrega metadados do vídeo
        self.loader.load(job)

        # 2. Deteta mudanças de cena
        self.detector.detect(job)

        # 3. Extrai o áudio
        self.audio.extract(job)

        # 4. Transcreve o áudio
        self.whisper.transcribe(job)

        # 5. Cria segmentos
        self.segment_extractor.extract(job)

        # 6. Classifica os segmentos
        self.viral.score(job)

        # 7. Gera automaticamente os melhores clips
        self.clip_generator.generate(job)

        return job
