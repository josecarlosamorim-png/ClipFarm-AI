from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import time


@dataclass
class ProcessingJob:
    # =====================================================
    # Identificação
    # =====================================================

    job_id: int | None = None

    # =====================================================
    # Entrada
    # =====================================================

    video_path: Path |None = None

    # Campanha atualmente selecionada
    campaign: Any | None = None

    # =====================================================
    # Estado do processamento
    # =====================================================

    status: str = "pending"
    progress: int = 0
    current_stage: str = ""

    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None

    # =====================================================
    # Informação do vídeo
    # =====================================================

    fps: float = 0.0
    duration: float = 0.0
    width: int = 0
    height: int = 0
    total_frames: int = 0

    # =====================================================
    # Áudio
    # =====================================================

    audio_path: Path | None = None

    # =====================================================
    # Dados produzidos
    # =====================================================

    scenes: list = field(default_factory=list)

    transcript: list = field(default_factory=list)

    segments: list = field(default_factory=list)

    best_clips: list = field(default_factory=list)

    generated_clips: list = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    # =====================================================
    # Logs / erros
    # =====================================================

    logs: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    # =====================================================
    # Utilitários
    # =====================================================

    def update_progress(self, progress: int, stage: str):
        self.progress = progress
        self.current_stage = stage

    def add_log(self, message: str):
        self.logs.append(message)

    def add_error(self, message: str):
        self.errors.append(message)
        self.status = "failed"

    def finish(self):
        self.progress = 100
        self.status = "completed"
        self.finished_at = time.time()

    @property
    def elapsed_time(self):
        end = self.finished_at or time.time()
        return end - self.started_at